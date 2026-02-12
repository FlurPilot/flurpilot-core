import { createOpenAI } from '@ai-sdk/openai';
import { streamText } from 'ai';

// OpenRouter Configuration
const openrouter = createOpenAI({
    baseURL: 'https://openrouter.ai/api/v1',
    apiKey: process.env.OPENROUTER_API_KEY,
    headers: {
        'HTTP-Referer': 'https://flurpilot.de', // Optional. Site URL for rankings on openrouter.ai.
        'X-Title': 'FlurPilot', // Optional. Site title for rankings on openrouter.ai.
    },
});

export const runtime = 'edge';

export async function POST(req: Request) {
    const { messages } = await req.json();

    const result = await streamText({
        model: openrouter(process.env.OPENROUTER_MODEL || 'google/gemini-2.0-pro-exp-02-05:free'),
        messages: messages,
        system:
            `You are FlurPilot, an expert AI assistant for land acquisition and German construction law (BauGB).
            You help project developers identify solar park potential.

            IMPORTANT LEGAL DISCLAIMERS (Haftungsausschluss):
            1. Wahrscheinlichkeitsaussage: This information constitutes a probability assessment, not a definitive statement of fact.
            2. Keine Haftung: The provider assumes no liability for content accuracy ('Keine Haftung für inhaltliche Richtigkeit').
            3. Keine Rechtsberatung: This service does NOT constitute legal advice.

            Answer concisely and professionally in German.`,
    });

    return result.toTextStreamResponse();
}
