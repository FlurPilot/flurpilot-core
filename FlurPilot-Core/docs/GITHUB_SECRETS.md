# GitHub Secrets Konfiguration

Diese Dokumentation beschreibt alle erforderlichen GitHub Secrets für das FlurPilot Projekt.

## Übersicht

| Secret | Service | Verwendung | Kosten |
|--------|---------|------------|--------|
| `BRAVE_API_KEY` | Brave Search API | Dokumenten-Suche (ersetzt Bing) | 2.000 queries/month free |
| `PHOENIX_API_KEY` | Arize Phoenix | AI Observability & Tracing | Free tier |
| `RESEND_API_KEY` | Resend | Transactional Emails | 3.000 emails/month free |
| `INFRACOST_API_KEY` | Infracost | Infrastructure Cost Estimation | Free for OSS |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase | Admin DB Zugriff | - |

---

## Detaillierte Konfiguration

### 1. Brave Search API

**Warum:** Die Bing Search API wurde am 11.08.2025 eingestellt. Brave Search ist der Ersatz.

**Schritte:**
1. Besuche https://brave.com/search/api/
2. Erstelle einen Account
3. Wähle den "Free" oder "Pro" Plan
4. Generiere einen API Key im Dashboard
5. Kopiere den Key

**Verwendung im Code:**
```python
# apps/worker/connectors/brave_search.py
from connectors.brave_search import BraveSearchClient

client = BraveSearchClient()
results = await client.search_pdfs(
    site_domain="stadt-muenchen.de",
    keywords=["Bebauungsplan", "Aufstellungsbeschluss"],
    year=2024
)
```

**Kosten:**
- Free Tier: 2.000 queries/month
- Paid Tier: $3 per 1.000 queries
- Geschätzte Nutzung: ~500 queries/month

---

### 2. Arize Phoenix (AI Observability)

**Warum:** Tracking von AI-Kosten, Hallucinations und Performance für Liability Shield.

**Schritte:**
1. Besuche https://app.phoenix.arize.com
2. Registriere dich mit GitHub oder Email
3. Erstelle ein neues Project namens "FlurPilot"
4. Gehe zu Settings → API Keys
5. Generiere einen neuen API Key
6. Kopiere den Key

**Verwendung im Code:**
```python
# apps/worker/ai_client.py
from ai_client import generate

result = await generate(
    prompt="Analyze this parcel...",
    metadata={
        "parcel_id": "12345",
        "operation": "analyze_parcel",
        "municipality": "muenchen"
    }
)
```

**Features:**
- Automatisches Tracing aller LLM Calls
- Kostenberechnung pro Call
- Hallucination Detection
- Dashboard: https://app.phoenix.arize.com

**Kosten:**
- Free Tier: Verfügbar
- Keine Kreditkarte erforderlich für Start

---

### 3. Resend (Email Service)

**Warum:** Zuverlässiger Versand von System-Alerts und Fehlerbenachrichtigungen.

**Schritte:**
1. Besuche https://resend.com
2. Erstelle einen Account
3. Füge deine Domain hinzu (z.B. flurpilot.de)
4. Verifiziere die Domain (DNS-Einträge)
5. Gehe zu API Keys
6. Generiere einen API Key
7. Kopiere den Key

**Verwendung im Code:**
```python
# apps/worker/services/email_service.py
from services.email_service import send_alert, send_error_alert

# System Alert
await send_alert(
    to="admin@flurpilot.de",
    subject="Daily Summary",
    message="Processing complete...",
    alert_type="info"
)

# Error Alert
await send_error_alert(
    to="admin@flurpilot.de",
    error_message="Failed to process parcel",
    context={"parcel_id": "12345"}
)
```

**Kosten:**
- Free Tier: 3.000 emails/month
- Paid: $1 per 1.000 emails

**Wichtig:**
- Domain muss verifiziert sein für Produktions-E-Mails
- Für Testing kann "onboarding@resend.dev" verwendet werden

---

### 4. Infracost

**Warum:** Automatische Kostenschätzung für Infrastructure-Änderungen in PRs.

**Schritte:**
1. Besuche https://www.infracost.io
2. Registriere dich (kostenlos für Open Source)
3. Gehe zu Organization Settings → API Key
4. Kopiere den API Key

**Verwendung:**
- Automatisch in `.github/workflows/infracost.yml`
- Postet Cost-Estimates als PR Comments
- Verhindert teure Infrastructure-Überraschungen

**Kosten:**
- Free für Open Source Projekte
- Private Repos: Paid Plans verfügbar

---

### 5. Supabase Service Role Key

**Warum:** Admin-Zugriff auf die Datenbank für Edge Functions und Worker.

**Schritte:**
1. Gehe zu deinem Supabase Dashboard
2. Wähle dein FlurPilot Project
3. Gehe zu Project Settings → API
4. Kopiere den "service_role" Key ( NICHT den anon key! )
5. **Wichtig:** Dieser Key hat volle Admin-Rechte!

**Verwendung:**
- Edge Functions
- Worker Background Jobs
- Admin-Operationen

**Sicherheit:**
- **Niemals** im Frontend verwenden!
- Nur in serverseitigem Code
- Rotiere regelmäßig

---

## Installation

### Option A: GitHub Web Interface

1. Öffne https://github.com/FlurPilot/-flurpilot-core
2. Gehe zu **Settings** → **Secrets and variables** → **Actions**
3. Klicke auf **"New repository secret"**
4. Füge Name und Wert ein
5. Wiederhole für alle Secrets

### Option B: GitHub CLI (Empfohlen)

```bash
# Login (falls noch nicht geschehen)
gh auth login

# Repository auswählen
gh repo set-default FlurPilot/-flurpilot-core

# Secrets setzen (ersetze YOUR_*_KEY mit den echten Werten)
gh secret set BRAVE_API_KEY -b"YOUR_BRAVE_KEY"
gh secret set PHOENIX_API_KEY -b"YOUR_PHOENIX_KEY"
gh secret set RESEND_API_KEY -b"YOUR_RESEND_KEY"
gh secret set INFRACOST_API_KEY -b"YOUR_INFRACOST_KEY"
gh secret set SUPABASE_SERVICE_ROLE_KEY -b"YOUR_SUPABASE_KEY"

# Überprüfen
gh secret list
```

---

## Testing

Nach der Konfiguration solltest du die Services testen:

### Brave Search testen:
```bash
cd apps/worker
python tests/test_brave_search.py
```

### Phoenix Observability testen:
```bash
cd apps/worker
python tests/test_phoenix.py
```

### Infracost testen:
- Erstelle einen Test-PR mit Infrastructure-Änderungen
- Infracost sollte automatisch einen Kommentar posten

### Workflows überprüfen:
1. Gehe zu GitHub → Actions
2. Prüfe, ob Workflows ohne Fehler laufen
3. Bei Fehlern: Secrets nochmals überprüfen

---

## Fehlerbehebung

### "Secret not found" Fehler
- Überprüfe Rechtschreibung des Secret-Namens
- Secrets sind case-sensitive
- Überprüfe, ob das Secret im richtigen Repository gesetzt ist

### "Authentication failed"
- API Key könnte ungültig sein
- Key könnte abgelaufen sein
- Für Resend: Domain-Verifizierung prüfen

### Infracost postet keine Kommentare
- Prüfe ob `INFRACOST_API_KEY` gesetzt ist
- Stelle sicher, dass der Workflow `pull-requests: write` hat
- Prüfe ob Infrastructure-Dateien geändert wurden

---

## Sicherheit

⚠️ **Wichtige Sicherheitshinweise:**

1. **Niemals** Secrets in Code committen
2. **Niemals** Secrets in Logs ausgeben
3. Regelmäßige Rotation empfohlen (alle 90 Tage)
4. Verwende unterschiedliche Keys für Dev/Prod
5. Überwache API-Nutzung auf ungewöhnliche Aktivitäten

---

## Support

Bei Problemen mit den Services:

- **Brave Search:** https://brave.com/search/api/docs/
- **Arize Phoenix:** https://docs.arize.com/phoenix
- **Resend:** https://resend.com/docs
- **Infracost:** https://www.infracost.io/docs/
- **Supabase:** https://supabase.com/docs

---

**Letzte Aktualisierung:** 2026-02-13
**Verantwortlich:** DevOps Team
