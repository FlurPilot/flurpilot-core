# FlurPilot Landing Page

> Lead-Generierung für automatisierte Aufstellungsbeschluss-Detektion

## Quick Start

```bash
# Dependencies installieren
npm install

# Development Server starten
npm run dev

# Production Build
npm run build
```

## Deployment auf Vercel

### 1. Vercel Setup

```bash
# Vercel CLI installieren (falls nicht vorhanden)
npm i -g vercel

# Deployment starten
vercel
```

### 2. Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

| Variable | Wert | Beschreibung |
|----------|------|--------------|
| `VITE_SUPABASE_URL` | `https://xxx.supabase.co` | Supabase Project URL |
| `VITE_SUPABASE_ANON_KEY` | `eyJ...` | Supabase Anon Key |

### 3. Supabase Setup

1. **Neues Projekt erstellen:** [supabase.com](https://supabase.com)
2. **Schema ausführen:** SQL Editor → `supabase/schema.sql` einfügen
3. **Edge Function deployen:**
   ```bash
   supabase functions deploy send-freebie
   ```
4. **Secrets setzen:** Dashboard → Edge Functions → Secrets
   - `RESEND_API_KEY`
   - `FREEBIE_DOWNLOAD_URL`

### 4. Resend Setup

1. Account erstellen: [resend.com](https://resend.com)
2. Domain verifizieren (flurpilot.de)
3. API Key erstellen und als Supabase Secret speichern

## Projektstruktur

```
FlurPilot/
├── src/
│   ├── App.jsx              # Router Setup
│   ├── lib/
│   │   └── supabase.js      # Supabase Client
│   └── pages/
│       ├── LandingPage.jsx  # Hauptseite
│       ├── Impressum.jsx
│       ├── Datenschutz.jsx
│       └── AGB.jsx
├── supabase/
│   ├── schema.sql           # Datenbank-Schema
│   └── functions/
│       └── send-freebie/    # Edge Function
├── freebie/
│   ├── scouting-kit.md      # PDF-Vorlage
│   ├── keyword-matrix.csv   # Excel-Datei
│   └── muster-datensatz.kml # Google Earth Beispiel
├── vercel.json              # Vercel Config
└── .env.example             # Environment Template
```

## Demo-Modus

Ohne konfiguriertes Supabase läuft die App im Demo-Modus:
- E-Mail-Formular funktioniert (simuliert)
- Keine E-Mails werden versendet
- Für lokale Entwicklung geeignet

## Tech Stack

- **Frontend:** React 19 + Vite
- **Styling:** Tailwind CSS
- **Animationen:** Framer Motion
- **Icons:** Lucide React
- **Backend:** Supabase (PostgreSQL + Edge Functions)
- **E-Mail:** Resend
- **Hosting:** Vercel

---

© 2026 FlurPilot | Stephan Ochmann
