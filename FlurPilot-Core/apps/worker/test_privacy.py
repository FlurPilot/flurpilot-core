from privacy import PrivacyEngine, RedactionResult
import sys

def test_privacy():
    print("Initializing Privacy Engine...")
    try:
        engine = PrivacyEngine()
    except Exception as e:
        print(f"Failed to init: {e}")
        sys.exit(1)

    test_cases = [
        "Der Antrag wurde von Frau Erika Mustermann gestellt.",
        "Bürgermeister Müller hat zugestimmt.",
        "Die Firma SolarTech GmbH plant eine Anlage.",
        "Hier wohnt Max Mustermann in der Hauptstraße.",
    ]

    print("\n--- Running Redaction Tests ---")
    for text in test_cases:
        result = engine.clean_text(text)
        assert isinstance(result, RedactionResult), "Must return RedactionResult"
        print(f"Original: {text}")
        print(f"Cleaned : {result.sanitized_text}")
        print(f"Redacted: {result.redaction_count} entities")
        print("-" * 30)

    # Basic verification
    result = engine.clean_text("Hallo Max Mustermann")
    assert result.redaction_count > 0, "Failed to redact simple name"
    print("\n✅ Privacy Tests Passed. Engine is ready.")

if __name__ == "__main__":
    test_privacy()
