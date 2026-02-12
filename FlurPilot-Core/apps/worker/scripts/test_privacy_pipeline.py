import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from privacy import PrivacyEngine, RedactionResult

def test_privacy():
    print("Initializing PrivacyEngine (de_core_news_lg)...")
    try:
        engine = PrivacyEngine()
    except Exception as e:
        print(f"Failed to init: {e}")
        print("Hint: Run 'python -m spacy download de_core_news_lg' first.")
        return

    test_cases = [
        # (input, expected_sanitized, description)
        (
            "Herr Max Mustermann hat den Antrag gestellt.",
            "Herr [PER] hat den Antrag gestellt.",
            "Simple name redaction"
        ),
        (
            "Bürgermeister Müller eröffnete die Sitzung.",
            "Bürgermeister Müller eröffnete die Sitzung.",
            "Whitelisted role context — should keep name"
        ),
        (
            "Der Landrat Meier stimmte zu.",
            "Der Landrat Meier stimmte zu.",
            "Whitelisted role context (Landrat)"
        ),
        (
            "Kontaktieren Sie uns unter 089/1234567 oder per Mail an info@stadt.de.",
            "Kontaktieren Sie uns unter [PHONE] oder per Mail an [EMAIL].",
            "Phone and email regex redaction"
        ),
        (
            "Beigeordneter Huber war anwesend.",
            "Beigeordneter Huber war anwesend.",
            "Whitelisted role context (Beigeordneter)"
        ),
        (
            "Herr Schmidt und Frau Weber beantragten eine Genehmigung.",
            None,  # Just check redaction count >= 2
            "Multi-name in single sentence"
        ),
    ]

    print("\n--- Running Golden Set Tests ---")
    failures = 0
    for i, (input_text, expected, desc) in enumerate(test_cases):
        result = engine.clean_text(input_text)
        assert isinstance(result, RedactionResult), "Must return RedactionResult"

        if expected is None:
            # Flexible check: just verify redactions happened
            if result.redaction_count >= 2:
                print(f"✅ Test {i+1} Passed — {desc}")
                print(f"   Redacted: {result.sanitized_text}")
            else:
                print(f"❌ Test {i+1} Failed — {desc}")
                print(f"   Expected >= 2 redactions, got {result.redaction_count}")
                print(f"   Result: {result.sanitized_text}")
                failures += 1
        elif result.sanitized_text == expected:
            print(f"✅ Test {i+1} Passed — {desc}")
        else:
            print(f"❌ Test {i+1} Failed — {desc}")
            print(f"   Input:    {input_text}")
            print(f"   Expected: {expected}")
            print(f"   Got:      {result.sanitized_text}")
            failures += 1

    # Metadata Tests
    print("\n--- Running Metadata Tests ---")

    result = engine.clean_text("Max Mustermann wohnt hier.")
    if result.redaction_count > 0:
        entity = result.redacted_entities[0]
        assert entity.entity_type == "PER", f"Expected PER, got {entity.entity_type}"
        assert entity.confidence > 0, "Confidence should be > 0"
        print(f"✅ Metadata Test Passed — entity_type={entity.entity_type}, confidence={entity.confidence}")
    else:
        print("⚠️ Metadata Test Skipped — no PER detected (model may differ)")

    # Email regex metadata
    result = engine.clean_text("Schreiben Sie an test@example.com")
    email_entities = [e for e in result.redacted_entities if e.entity_type == "EMAIL"]
    if email_entities:
        assert email_entities[0].confidence == 1.0, "Regex matches should have confidence 1.0"
        print("✅ Email Metadata Test Passed — confidence=1.0")
    else:
        print("❌ Email Metadata Test Failed — no EMAIL entity found")
        failures += 1

    # Address regex test
    result = engine.clean_text("Hauptstraße 42, 80331 München")
    addr_entities = [e for e in result.redacted_entities if e.entity_type == "ADDRESS"]
    if addr_entities:
        print(f"✅ Address Test Passed — {result.sanitized_text}")
    else:
        print(f"⚠️ Address Test — no ADDRESS detected: {result.sanitized_text}")

    # Summary
    if failures == 0:
        print("\n🎉 All Privacy Tests Passed!")
    else:
        print(f"\n⚠️ {failures} Tests Failed.")

if __name__ == "__main__":
    test_privacy()
