"""Basic smoke tests for FlurPilot Worker."""


def test_imports():
    """Test that core modules can be imported."""
    import pdf_processor
    import privacy
    assert hasattr(pdf_processor, 'PDFProcessor')
    assert hasattr(privacy, 'PrivacyEngine')


def test_privacy_engine_init():
    """Test that PrivacyEngine can be instantiated."""
    from privacy import PrivacyEngine
    engine = PrivacyEngine()
    assert engine is not None


def test_privacy_engine_clean_empty():
    """Test that PrivacyEngine handles empty input."""
    from privacy import PrivacyEngine
    engine = PrivacyEngine()
    result = engine.clean_text("")
    assert result.sanitized_text == ""
    assert result.redaction_count == 0
