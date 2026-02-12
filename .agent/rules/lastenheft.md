---
trigger: always_on
---

Lastenheft
1. PROJEKT-SCOPE & VERTRAGSGEGENSTAND
Leistungsbeschreibung (ehem. Elevator Pitch): Bereitstellung einer forensischen Intelligence-Plattform (SaaS & API) zur Aggregation öffentlich zugänglicher Daten ("Open Source Intelligence") und geometrischen Berechnung von Flächenpotenzialen. Rechtlicher Hinweis: Die Software dient ausschließlich der Informationsgewinnung. Sie ersetzt keine amtliche Auskunft aus dem Liegenschaftskataster.
Internationalisierung (i18n):
Constraint: Architektur ist i18n-strict.
Abnahmekriterium: Quellcode enthält keine hartkodierten Strings in UI-Komponenten (Prüfung via Static Code Analysis).
Default: de-DE, en-US.
Logic: Cross-Border Semantic Mapping.
In-Scope (Geschuldete Funktionalität):
Hybrid Acquisition Engine: Paralleles Harvesting. [LEGAL UPDATE] Disclaimer: Die Funktionsfähigkeit ist abhängig von der Erreichbarkeit der Drittquellen (Bing/RIS). Ausfälle Dritter stellen keinen Mangel der Software dar.
Virtual Parcel Engine (VPE): PostGIS-Pipeline. Async Materialization.
AI Intelligence Layer: Gemini 2.0 Pro. [LEGAL UPDATE] Liability Shield: KI-Ergebnisse werden als "Wahrscheinlichkeitsaussage" gekennzeichnet. Keine Haftung für inhaltliche Richtigkeit ("Halluzinationen").
Trust Dashboard: Split-View UI mit kryptografischem Audit-Trail.
Werner's "Digital Sticky Note": Client-Side Encryption. [LEGAL UPDATE] Key Liability: Verlust des privaten Schlüssels durch den Nutzer führt zu unwiderruflichem Datenverlust. Der Anbieter besitzt keinen "Master Key" (Zero Knowledge).
Logic Addition: Temporal Versioning.
Anti-Scope (Leistungsausschluss):
No CRM / Marketplace / Social / AI Slop.
No Serverless Cold Starts (Critical Path).
No Shared Secrets.
[LEGAL INJECTION] Keine Rechtsberatung: Das System gibt keine baurechtlichen Einschätzungen ab, sondern indiziert lediglich Dokumente.
Sicherheits-Philosophie (Vertragliche Zusicherung):
Zero Trust / Privacy by Architecture.
Sicherheitsstandard: Orientierung am BSI IT-Grundschutz (Baustein APP.3).
Verfügbarkeit: Fail Closed (Sicherheit vor Verfügbarkeit).

2. FUNKTIONALE ANFORDERUNGEN & RECHTSKONFORMITÄT
F-01: Hybrid Acquisition Engine (The Crawler)
Funktion: Indizierung von PDF-Protokollen.
Logik: Scheduler -> SourceSelector -> Fetcher -> Hash -> Dedup -> Queueing.
Technical Constraints: Memory Safety, Concurrency Semaphores.
Isolation: gVisor Sandbox.
[LEGAL HARDENING] Störerhaftung:
Der Crawler beachtet strikt robots.txt (Standard-Konformität).
Bei IP-Blockaden durch Zielserver ("Ban") greift der Circuit Breaker. Dies gilt als systemkonformes Verhalten, nicht als Fehler.
Abuse Cases: DDoS-Trap, Zip Bombs.
F-02: Virtual Parcel Engine (The Bavarian Bypass)
Funktion: Berechnung von Flurstücksgrenzen mittels Differenzoperation.
Logik: Trigger -> Worker -> PostGIS -> Materialization -> Serve.
[LEGAL HARDENING] Urheberrecht & Datennutzung:
Die Quelldaten (InVeKoS/Hausumringe) werden nicht permanent gespeichert, sondern nur zur Berechnung der Differenzgeometrie ("Werk") genutzt, sofern lizenzrechtlich zulässig (Open Data DE).
Das Output-Format ist ein abgeleitetes Werk.
Prevention: SQL Injection via Prepared Statements.
F-03: Privacy Pipeline (NER & Anonymization)
Funktion: Schwärzung von Personennamen (PII).
Logik: OCR -> NER (Local) -> Whitelisting -> Redaction -> Persist.
[LEGAL HARDENING] DSGVO-Compliance (Art. 32):
Das System garantiert "State of the Art" Anonymisierung.
Restrisiko-Klausel: Sollte trotz NER-Pipeline ein Name lesbar bleiben (z.B. durch handschriftliche Notizen im PDF), haftet der Anbieter nur bei grober Fahrlässigkeit oder Vorsatz in der Programmierung der Pipeline.

3. DATEN-ARCHITEKTUR & HAFTPFLICHT (THE TRUTH)
Schema-Definition: (Siehe v1.1.0)
Kryptografie & Schlüsselverwaltung:
Strategie: Envelope Encryption.
Haftungsausschluss: Für die Sicherheit der Endgeräte (Browser, OS), auf denen die Entschlüsselung der "Sticky Notes" stattfindet, ist der Kunde verantwortlich.
DB-Strategie:
Database: Supabase (PostgreSQL 16).
Network: Private Isolation.
Audit-Logs (Rechtssicherheit):
Einsatz von Merkle Trees zur Beweissicherung.
Die Logs dienen als gerichtsfester Nachweis dafür, wer wann welches Dokument eingesehen hat.

4. API & SCHNITTSTELLEN
Endpunkte: SSE, Signierte PDFs. Auth: FIDO2 (Zwingend für Administratoren). Observability: Honeytokens (Detektion von unbefugtem Zugriff).
[LEGAL HARDENING] SLA-Definitionen:
Rate Limiting: Das System drosselt Anfragen aggressiv zum Selbstschutz (Token Bucket). Drosselung ist kein Mangel.
Identity: Einsatz von mTLS für M2M-Kommunikation.

5. TECH STACK & LIZENZ-COMPLIANCE
Core Stack:
Frontend: Next.js 16, React 19.
Backend: Python 3.12, Node.js.
[LEGAL HARDENING] Third-Party License Audit:
Es dürfen ausschließlich Bibliotheken mit Permissive Licenses (MIT, Apache 2.0, BSD) verwendet werden.
Verbot: Keine Copyleft-Lizenzen (GPL, AGPL) im distribuierbaren Code, um eine "Infektion" des proprietären Quellcodes zu verhindern.
Nachweis: Automatisierter Lizenz-Scan im Build-Prozess (Blocker bei Verstoß).
Supply Chain Security:
SBOM, Dependency Pinning, Cosign, Distroless Images.

6. DESIGN SYSTEM & BARRIEREFREIHEIT (BITV 2.0)
Typografie / Farben: (Siehe v1.4.0).
[LEGAL HARDENING] Barrierefreiheit & Usability:
Anforderung: Die Software muss die Anforderungen der BITV 2.0 / WCAG 2.1 Level AA erfüllen.
Konkretisierung:
Kontrastverhältnis Text/Hintergrund mind. 4.5:1.
Tastaturbedienbarkeit aller interaktiven Elemente.
Keine Inhalte, die schneller als 3-mal pro Sekunde blinken (Vermeidung photosensitiver Anfälle).
UX Signals: Sudo-Mode für kritische Aktionen, Watermarking für Screenshots.

7. VIEW-SPEZIFIKATIONEN
7.1 Search & Import:
Client-Side Validation.
Feedback: Ampel + Details.
7.2 Forensics Interface:
List + Map (Pinned Mode).
Wasserzeichen: User-ID + Timestamp (sichtbar & steganografisch) zur Rückverfolgung von Datenlecks.
7.3 Trust Center & Transparenz:
Transparency Report: Automatisierte Offenlegung von Abwehr-Metriken.
Export: PDF-Dossier.
Disclaimer im Footer jeder PDF-Seite: "Automatisch generiertes Dokument. Angaben ohne Gewähr. Rechtsverbindlich ist nur das Originaldokument der Behörde."

8. DEFINITION OF DONE (DoD) – Das Abnahmeprotokoll
Die Abnahme erfolgt ausschließlich bei Erfüllung folgender, objektiver Kriterien:
Rechtliche Code-Hygiene: Lizenz-Scan (FOSSA/Snyk) bestätigt 100% Kompatibilität (Keine GPL).
Sicherheit: Penetration Test Report bestätigt Abwesenheit von Vulnerabilities gemäß CVSS Score >= 7.0.
Datenschutz: Nachweis, dass "Sticky Notes" serverseitig nicht entschlüsselbar sind (Code Review des Encryption-Moduls).
Funktionalität: Alle Gherkin-Testfälle (F-01 bis F-03) sind "Passed".
Performance: API-Latenz P95 < 200ms (gemessen unter Laborbedingungen, exklusive externer Latenzen).
Barrierefreiheit: Automatisierter Lighthouse-Test "Accessibility" Score > 90.
Supply Chain: Vollständige SBOM liegt vor, alle Container sind signiert.



