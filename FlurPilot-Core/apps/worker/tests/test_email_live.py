#!/usr/bin/env python3
"""
Echter Email-Test für Resend Service
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from services.email_service import EmailService

async def test_real_email():
    """Send a real test email"""
    print("="*60)
    print("RESEND EMAIL SERVICE - ECHTER TEST")
    print("="*60)
    
    service = EmailService()
    
    # Test recipient
    to_email = "alerts@flurpilot.de"
    
    print(f"\nSende Test-Email an: {to_email}")
    print("-" * 60)
    
    try:
        # Test 1: Info Alert
        print("\n[TEST 1] Info Alert...")
        email_id = await service.send_alert(
            to=to_email,
            subject="Test Alert - Stack Optimization",
            message="""Dies ist ein Test der Email-Service Integration.

Alle 4 Phasen der Stack Optimization wurden erfolgreich implementiert:
- Phase 1: Rust/WASM Geometry Engine
- Phase 2: Brave Search API (ersetzt Bing)
- Phase 3: Arize Phoenix Observability
- Phase 4: DevOps Tools (Resend, Infracost, Mintlify)

Tests: Alle bestanden ✓""",
            alert_type="info",
            metadata={
                "test_type": "integration",
                "phase": "Phase 4 - DevOps",
                "timestamp": "2026-02-12",
                "status": "production_ready"
            }
        )
        
        if email_id:
            print(f"[OK] Email gesendet! ID: {email_id}")
        else:
            print("[INFO] Email wurde geloggt (kein API Key oder Resend nicht verfügbar)")
        
        # Test 2: Error Alert
        print("\n[TEST 2] Error Alert...")
        error_id = await service.send_error_alert(
            to=to_email,
            error_message="Test-Fehler für Alert-System",
            context={
                "parcel_id": "TEST-12345",
                "municipality": "Test-Stadt",
                "operation": "test_alert",
                "severity": "low"
            }
        )
        
        if error_id:
            print(f"[OK] Error Alert gesendet! ID: {error_id}")
        
        print("\n" + "="*60)
        print("TEST ABGESCHLOSSEN")
        print("="*60)
        print(f"\nPrüfe Posteingang: {to_email}")
        print("Die Email sollte innerhalb weniger Sekunden ankommen.")
        
    except Exception as e:
        print(f"\n[X] Fehler beim Senden: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_real_email())
