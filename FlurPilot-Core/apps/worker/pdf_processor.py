
import asyncio
import hashlib
import io
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional, Tuple
from pypdf import PdfReader
from privacy import PrivacyEngine, RedactionResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PDFProcessor")

# OCR threshold: if extracted text averages fewer than this many chars per page,
# attempt OCR fallback
OCR_CHARS_PER_PAGE_THRESHOLD = 50

class PDFProcessor:
    """
    Handles secure PDF processing for the Hybrid Acquisition Engine.
    Integrates Privacy Pipeline (F-03) with Fail Closed design.
    Supports text PDFs (pypdf) and scanned PDFs (pymupdf OCR fallback).
    """

    def __init__(self, fetcher=None):
        self.fetcher = fetcher

        # Fail Closed: Cannot start without privacy module
        try:
            self.privacy = PrivacyEngine()
        except Exception as e:
            logger.critical(f"Failed to initialize PrivacyEngine: {e}")
            raise

        # Lazy-load OCR capability
        self._ocr_available: Optional[bool] = None

    def _check_ocr_available(self) -> bool:
        """Check if pymupdf is installed for OCR fallback."""
        if self._ocr_available is None:
            try:
                import pymupdf
                self._ocr_available = True
                logger.info("OCR fallback available (pymupdf).")
            except ImportError:
                self._ocr_available = False
                logger.warning("pymupdf not installed. OCR fallback disabled.")
        return self._ocr_available

    async def process_url(self, url: str) -> Tuple[Optional[str], Optional[bytes], Optional[RedactionResult]]:
        """
        Downloads a PDF, calculates its hash, extracts & sanitizes text.
        Returns: (content_hash, file_bytes, redaction_result)
        """
        if not self.fetcher:
            logger.error("PDFProcessor initialized without a fetcher!")
            return None, None, None

        try:
            logger.info(f"Downloading PDF from: {url}")

            async with await self.fetcher.stream('GET', url) as response:
                if response.status_code != 200:
                    logger.error(f"Failed to download PDF: HTTP {response.status_code}")
                    return None, None, None

                sha256_hash = hashlib.sha256()
                file_buffer = io.BytesIO()

                async for chunk in response.aiter_bytes():
                    sha256_hash.update(chunk)
                    file_buffer.write(chunk)

                content_hash = sha256_hash.hexdigest()
                file_bytes = file_buffer.getvalue()

                logger.info(f"Download complete. Hash: {content_hash}")

                # Extract text (with OCR fallback)
                raw_text = self.extract_text(file_bytes)

                # Privacy Pipeline (Fail Closed)
                try:
                    result = self.privacy.clean_text(raw_text)
                    if not result.sanitized_text and raw_text:
                        logger.warning(f"PrivacyEngine returned empty text for non-empty input from {url}")

                    logger.info(f"Redacted {result.redaction_count} PII entities from {url}")
                    return content_hash, file_bytes, result

                except Exception as pe:
                    logger.critical(f"PrivacyEngine FAILED for {url}: {pe}")
                    # FAIL CLOSED: Do not return raw text
                    return None, None, None

        except Exception as e:
            logger.error(f"Error processing PDF {url}: {e}")
            return None, None, None

    def extract_text(self, file_bytes: bytes) -> str:
        """
        Extracts text from PDF bytes.
        Uses pypdf first, falls back to pymupdf OCR for scanned documents.
        """
        text = self._extract_text_pypdf(file_bytes)

        # Check if text extraction yielded meaningful content
        page_count = max(self._count_pages(file_bytes), 1)
        avg_chars = len(text) / page_count

        if avg_chars < OCR_CHARS_PER_PAGE_THRESHOLD:
            logger.info(f"Low text yield ({avg_chars:.0f} chars/page). Attempting OCR fallback...")
            ocr_text = self._extract_text_ocr(file_bytes)
            if len(ocr_text) > len(text):
                logger.info(f"OCR extracted {len(ocr_text)} chars (vs {len(text)} from pypdf).")
                return ocr_text

        return text

    def _extract_text_pypdf(self, file_bytes: bytes) -> str:
        """Extract text using pypdf. Handles encrypted PDFs gracefully."""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))

            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except Exception:
                    logger.warning("PDF is encrypted and cannot be read.")
                    return ""

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text.strip()

        except Exception as e:
            logger.error(f"pypdf text extraction failed: {e}")
            return ""

    def _extract_text_ocr(self, file_bytes: bytes) -> str:
        """OCR fallback using pymupdf for scanned PDFs."""
        if not self._check_ocr_available():
            return ""

        try:
            import pymupdf

            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            text_parts = []

            for page in doc:
                # Get text blocks (includes OCR if available)
                text = page.get_text("text")
                if text.strip():
                    text_parts.append(text)

            doc.close()
            return "\n".join(text_parts).strip()

        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""

    def _count_pages(self, file_bytes: bytes) -> int:
        """Count pages in PDF for threshold calculation."""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            return len(reader.pages)
        except Exception:
            return 1
