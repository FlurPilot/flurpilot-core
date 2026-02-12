import os
import logging
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Phoenix Observability Integration
try:
    from phoenix.otel import register
    from openinference.instrumentation.openai import OpenAIInstrumentor
    PHOENIX_AVAILABLE = True
except ImportError:
    PHOENIX_AVAILABLE = False
    logging.warning("⚠️  Arize Phoenix not installed. Observability disabled.")
    logging.warning("   Install with: pip install arize-phoenix openinference-instrumentation-openai")

logger = logging.getLogger("AIClient")

# Initialize Phoenix if configured
_tracer_provider = None
_phoenix_initialized = False

def _init_phoenix():
    """Initialize Phoenix observability if API key is configured."""
    global _tracer_provider, _phoenix_initialized
    
    if not PHOENIX_AVAILABLE or _phoenix_initialized:
        return
    
    phoenix_api_key = os.getenv("PHOENIX_API_KEY")
    phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "https://app.phoenix.arize.com")
    
    if phoenix_api_key:
        try:
            _tracer_provider = register(
                project_name="flurpilot-ai",
                endpoint=phoenix_endpoint,
                auto_instrument=False  # We'll instrument manually for more control
            )
            
            # Instrument OpenAI client
            OpenAIInstrumentor().instrument(tracer_provider=_tracer_provider)
            
            _phoenix_initialized = True
            logger.info("✅ Arize Phoenix observability initialized")
            logger.info(f"   Project: flurpilot-ai")
            logger.info(f"   Endpoint: {phoenix_endpoint}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Phoenix: {e}")
    else:
        logger.debug("Phoenix API key not configured, skipping observability")

# Initialize on module load
_init_phoenix()


def get_client() -> tuple[AsyncOpenAI, str]:
    """
    Returns a tuple of (AsyncOpenAI client, model_name).
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("AI_MODEL", "anthropic/claude-opus-4.6")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")

    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://flurpilot.de", 
            "X-Title": "FlurPilot Worker",
        }
    )
    
    return client, model


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Estimate the cost of an LLM call based on model pricing.
    
    Pricing in USD per 1M tokens (approximate for OpenRouter):
    - anthropic/claude-opus-4: $15/$75
    - anthropic/claude-sonnet-4: $3/$15
    - anthropic/claude-haiku: $0.25/$1.25
    - openai/gpt-4o: $5/$15
    - openai/gpt-4o-mini: $0.15/$0.60
    
    Args:
        model: Model identifier
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        
    Returns:
        Estimated cost in USD
    """
    # Default pricing (claude-opus-4)
    pricing = {
        "input": 15.0,   # $ per 1M tokens
        "output": 75.0   # $ per 1M tokens
    }
    
    # Model-specific pricing
    if "haiku" in model.lower():
        pricing = {"input": 0.25, "output": 1.25}
    elif "sonnet" in model.lower():
        pricing = {"input": 3.0, "output": 15.0}
    elif "gpt-4o-mini" in model.lower():
        pricing = {"input": 0.15, "output": 0.60}
    elif "gpt-4o" in model.lower():
        pricing = {"input": 5.0, "output": 15.0}
    
    # Calculate cost
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    
    return round(input_cost + output_cost, 6)


async def generate_stream(prompt: str, system_prompt: str = None, metadata: Dict[str, Any] = None):
    """
    Generates a streaming response from the AI model.
    Yields chunks of text.
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        metadata: Optional metadata for tracing (e.g., {"parcel_id": "123", "operation": "analyze"})
    """
    client, model = get_client()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Estimate input tokens (rough approximation: 1 token ≈ 4 characters)
    input_chars = sum(len(m["content"]) for m in messages)
    estimated_input_tokens = input_chars // 4

    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    output_tokens = 0
    output_chars = 0
    
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            output_chars += len(content)
            output_tokens = output_chars // 4
            yield content

    # Log completion with cost estimate
    estimated_output_tokens = output_chars // 4
    cost = estimate_cost(model, estimated_input_tokens, estimated_output_tokens)
    
    logger.info(f"LLM Call Complete - Model: {model}, "
                f"Input: ~{estimated_input_tokens} tokens, "
                f"Output: ~{estimated_output_tokens} tokens, "
                f"Cost: ${cost:.6f}")
    
    # Add custom attributes to Phoenix span if available
    if PHOENIX_AVAILABLE and _phoenix_initialized and metadata:
        try:
            from opentelemetry import trace
            current_span = trace.get_current_span()
            if current_span:
                for key, value in metadata.items():
                    current_span.set_attribute(f"flurpilot.{key}", str(value))
                current_span.set_attribute("flurpilot.estimated_cost_usd", cost)
                current_span.set_attribute("flurpilot.model", model)
        except Exception as e:
            logger.debug(f"Could not add Phoenix attributes: {e}")


async def generate(prompt: str, system_prompt: str = None, metadata: Dict[str, Any] = None) -> str:
    """
    Generates a complete (non-streaming) response from the AI model.
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        metadata: Optional metadata for tracing
        
    Returns:
        Complete response text
    """
    chunks = []
    async for chunk in generate_stream(prompt, system_prompt, metadata):
        chunks.append(chunk)
    return "".join(chunks)


# Backwards compatibility alias
async def generate_text(prompt: str, system_prompt: str = None) -> str:
    """Alias for generate() for backwards compatibility."""
    return await generate(prompt, system_prompt)
