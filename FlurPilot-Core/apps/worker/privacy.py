import spacy
import os
import re
import logging
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger("PrivacyEngine")

@dataclass
class RedactedEntity:
    """Metadata for a single redacted entity."""
    entity_type: str  # PER, EMAIL, PHONE, ADDRESS
    original_length: int
    start_char: int
    end_char: int
    confidence: float  # 0.0 - 1.0 (NER confidence or 1.0 for regex)

@dataclass
class RedactionResult:
    """Structured result of the privacy pipeline."""
    sanitized_text: str
    redaction_count: int
    redacted_entities: List[RedactedEntity] = field(default_factory=list)

class PrivacyEngine:
    """
    Implements F-03: Privacy Pipeline (NER & Anonymization).
    Uses local spaCy model to identify and redact PII.
    DSGVO Art. 32 compliant — Fail Closed design.
    """

    def __init__(self, model_name: str | None = None):
        model_name = model_name or os.getenv("PRIVACY_NER_MODEL", "de_core_news_lg")
        logger.info(f"Loading NER model: {model_name}")

        try:
            if not spacy.util.is_package(model_name):
                logger.info(f"Model '{model_name}' not found. Downloading...")
                from spacy.cli import download
                download(model_name)

            self.nlp = spacy.load(model_name)
            logger.info("NER model loaded successfully.")
        except Exception as e:
            logger.critical(f"Failed to load NER model: {e}")
            raise

        # Whitelist: Public roles that are NOT PII in municipal context
        self.whitelist = {
            "Bürgermeister", "Oberbürgermeister", "Ortsbürgermeister",
            "Gemeinderat", "Stadtrat", "Ausschuss", "Kreistag",
            "Verbandsgemeinde", "Stadt", "Gemeinde", "Kreis", "Landrat",
            "Beigeordneter", "Dezernent", "Ratsherr", "Ratsfrau",
            "Schriftführer", "Schriftführerin", "Protokollant", "Protokollantin",
            "Kämmerer", "Kämmerin", "Bauamtsleiter", "Bauamtsleiterin",
            "Vorsitzender", "Vorsitzende", "Fraktionsvorsitzender",
            "Fachbereichsleiter", "Fachbereichsleiterin", "Bauverwaltung",
            "Architekt", "Planer", "Ingenieur",
        }

        # Regex patterns for PII (high-confidence)
        self.patterns = {
            "EMAIL": re.compile(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ),
            "PHONE": re.compile(
                r'(?:\+49|0)[1-9][0-9 \-\/\(\)]{5,}\d'
            ),
            "ADDRESS": re.compile(
                r'\b[A-ZÄÖÜ][a-zäöüß]+(?:straße|weg|gasse|platz|allee|ring|damm|ufer|chaussee)'
                r'\s+\d+[a-zA-Z]?'
                r'(?:\s*,\s*\d{5}\s+[A-ZÄÖÜ][a-zäöüß]+)?'
            ),
        }

    def clean_text(self, text: str) -> RedactionResult:
        """
        Redacts PER entities, emails, phones, and addresses.
        Returns structured RedactionResult with metadata.
        """
        if not text:
            return RedactionResult(sanitized_text="", redaction_count=0)

        redacted_entities: List[RedactedEntity] = []

        # Phase 1: Regex redaction (deterministic, high confidence)
        for pii_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                redacted_entities.append(RedactedEntity(
                    entity_type=pii_type,
                    original_length=len(match.group()),
                    start_char=match.start(),
                    end_char=match.end(),
                    confidence=1.0,
                ))

        # Phase 2: NER-based PER detection
        doc = self.nlp(text)
        per_entities = [ent for ent in doc.ents if ent.label_ == "PER"]

        for ent in per_entities:
            # Whitelist check: skip if entity text contains a known role
            if any(role.lower() in ent.text.lower() for role in self.whitelist):
                continue

            # Context check: skip if preceded by a whitelisted role
            if ent.start > 0:
                prev_token = doc[ent.start - 1]
                if any(role.lower() in prev_token.text.lower() for role in self.whitelist):
                    continue

            # Check for overlap with regex matches (avoid double redaction)
            overlaps = any(
                e.start_char < ent.end_char and e.end_char > ent.start_char
                for e in redacted_entities
            )
            if overlaps:
                continue

            redacted_entities.append(RedactedEntity(
                entity_type="PER",
                original_length=len(ent.text),
                start_char=ent.start_char,
                end_char=ent.end_char,
                confidence=round(max(
                    (tok.ent_iob_ != "O" and 0.85 or 0.5) for tok in ent
                ), 2),
            ))

        # Phase 3: Apply redactions (reverse order to preserve indices)
        redacted_entities.sort(key=lambda x: x.start_char, reverse=True)
        sanitized = text
        for entity in redacted_entities:
            tag = f"[{entity.entity_type}]"
            sanitized = sanitized[:entity.start_char] + tag + sanitized[entity.end_char:]

        return RedactionResult(
            sanitized_text=sanitized,
            redaction_count=len(redacted_entities),
            redacted_entities=sorted(redacted_entities, key=lambda x: x.start_char),
        )
