'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function Datenschutz() {
    return (
        <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
            {/* Header */}
            <header className="bg-white border-b border-slate-200">
                <div className="max-w-4xl mx-auto px-4 py-5 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2.5">
                        <img src="/logo.png" alt="FlurPilot Logo" className="h-8 w-auto" />
                    </Link>
                    <Link href="/" className="text-sm text-slate-500 hover:text-slate-900 flex items-center gap-1">
                        <ArrowLeft className="w-4 h-4" /> Zurück
                    </Link>
                </div>
            </header>

            {/* Content */}
            <main className="max-w-4xl mx-auto px-4 py-12">
                <h1 className="text-3xl font-bold text-slate-900 mb-8">Datenschutzerklärung</h1>

                <div className="prose prose-slate max-w-none space-y-8">

                    <section>
                        <h2 className="text-xl font-semibold mb-4">1. Datenschutz auf einen Blick</h2>
                        <h3 className="text-lg font-medium mt-4 mb-2">Allgemeine Hinweise</h3>
                        <p className="text-slate-700 leading-relaxed">
                            Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren
                            personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene
                            Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">2. Verantwortliche Stelle</h2>
                        <p className="text-slate-700 leading-relaxed">
                            Stephan Ochmann<br />
                            c/o Postflex #586<br />
                            Emsdettener Straße 10<br />
                            D-48268 Greven<br /><br />
                            Telefon: +49 (0) 2363 8072515<br />
                            E-Mail: info@flurpilot.de
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">3. Datenerfassung auf dieser Website</h2>

                        <h3 className="text-lg font-medium mt-4 mb-2">Newsletter / Freebie-Download</h3>
                        <p className="text-slate-700 leading-relaxed">
                            Wenn Sie die kostenlose &quot;First-Mover Map&quot; herunterladen möchten, benötigen wir Ihre
                            E-Mail-Adresse. Die Angabe ist freiwillig, jedoch für den Erhalt des Downloads
                            erforderlich.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            <strong>Rechtsgrundlage:</strong> Art. 6 Abs. 1 lit. a DSGVO (Einwilligung).<br />
                            <strong>Beweissicherung:</strong> Zum Nachweis Ihrer Einwilligung speichern wir den Zeitpunkt der Anmeldung sowie
                            die IP-Adresse, von der aus die Bestätigung (Double-Opt-In) erfolgte. Dies erfolgt auf Grundlage
                            unseres berechtigten Interesses an der Rechtsverteidigung (Art. 6 Abs. 1 lit. f DSGVO).<br />
                            <strong>Speicherdauer:</strong> Bis zum Widerruf Ihrer Einwilligung (zzgl. Verjährungsfristen für Nachweispflichten).<br />
                            <strong>Widerruf:</strong> Sie können Ihre Einwilligung jederzeit per E-Mail an
                            info@flurpilot.de widerrufen oder den &quot;Austragen&quot;-Link im Newsletter nutzen.
                        </p>

                        <h3 className="text-lg font-medium mt-6 mb-2">Erfolgsmessung (Tracking)</h3>
                        <p className="text-slate-700 leading-relaxed">
                            Die versendeten E-Mails können sogenannte &quot;Web-Beacons&quot; bzw. Zählpixel enthalten.
                            Dies erlaubt uns festzustellen, ob eine E-Mail geöffnet wurde und welche Links geklickt wurden.
                            Dies dient der technischen Optimierung und Verbesserung unseres Angebots.
                            <strong>Rechtsgrundlage:</strong> Art. 6 Abs. 1 lit. f DSGVO (Berechtigtes Interesse).
                            Wenn Sie keine Analyse wünschen, müssen Sie den Newsletter abbestellen.
                        </p>

                        <h3 className="text-lg font-medium mt-6 mb-2">Server-Log-Dateien</h3>
                        <p className="text-slate-700 leading-relaxed">
                            Der Provider dieser Seiten erhebt und speichert automatisch Informationen in
                            sogenannten Server-Log-Dateien, die Ihr Browser automatisch an uns übermittelt:
                        </p>
                        <ul className="list-disc list-inside text-slate-700 mt-2 space-y-1">
                            <li>Browsertyp und Browserversion</li>
                            <li>Verwendetes Betriebssystem</li>
                            <li>Referrer URL</li>
                            <li>Hostname des zugreifenden Rechners</li>
                            <li>Uhrzeit der Serveranfrage</li>
                            <li>IP-Adresse (anonymisiert)</li>
                        </ul>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            <strong>Rechtsgrundlage:</strong> Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse).<br />
                            <strong>Speicherdauer:</strong> 7 Tage.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">4. Hosting & E-Mail</h2>
                        <p className="text-slate-700 leading-relaxed">
                            Wir setzen unterschiedliche Dienstleister für das Webhosting und die E-Mail-Infrastruktur ein.
                        </p>

                        <h3 className="text-lg font-medium mt-4 mb-2">Webhosting (Applikation)</h3>
                        <p className="text-slate-700 leading-relaxed">
                            Die Web-Anwendung wird durch <strong>Vercel Inc.</strong> bereitgestellt:
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA.<br />
                            Serverstandort: Frankfurt (AWS eu-central-1), soweit technisch durch Vercel Edge Network gesteuert.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            <strong>Datentransfer USA:</strong> Vercel ist nach dem EU-US Data Privacy Framework (DPF) zertifiziert.
                            Wir haben zudem einen Vertrag über Auftragsverarbeitung (AVV) abgeschlossen.
                        </p>

                        <h3 className="text-lg font-medium mt-6 mb-2">Domain & E-Mail-Hosting</h3>
                        <p className="text-slate-700 leading-relaxed">
                            Die Domainverwaltung und E-Mail-Postfächer liegen bei <strong>IONOS SE</strong>:
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            IONOS SE<br />
                            Elgendorfer Str. 57<br />
                            56410 Montabaur<br />
                            Deutschland
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            <strong>Rechtsgrundlage:</strong> Art. 6 Abs. 1 lit. f DSGVO. AVV mit IONOS liegt vor.
                        </p>

                        <section>
                            <h2 className="text-xl font-semibold mb-4">5. E-Mail-Versand, Marketing & CRM</h2>
                            <p className="text-slate-700 leading-relaxed">
                                Für den Versand von E-Mails, das Verwalten von Kontakten (CRM) und Marketing nutzen wir <strong>Brevo</strong> (ehemals Sendinblue):
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                Sendinblue GmbH (Brevo)<br />
                                Köpenicker Straße 126<br />
                                10179 Berlin<br />
                                Deutschland
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                Ihre Daten (E-Mail-Adresse, IP, Anmeldezeitpunkt) werden auf den Servern von Brevo in Deutschland gespeichert.
                                Brevo verwendet diese Daten zum Versand und zur Auswertung der Newsletter (Öffnungsrate, Klicks).
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                <strong>Rechtsgrundlage:</strong> Art. 6 Abs. 1 lit. f DSGVO (Berechtigtes Interesse) sowie Art. 28 DSGVO (Auftragsverarbeitung).
                                Wir haben einen AVV mit Brevo abgeschlossen.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-semibold mb-4">6. Datenbank</h2>
                            <p className="text-slate-700 leading-relaxed">
                                Zur Speicherung von E-Mail-Adressen und Status-Updates nutzen wir <strong>Supabase</strong>:
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                Supabase, Inc.<br />
                                970 Toa Payoh North<br />
                                Singapore 318992
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                <strong>Wichtiger Hinweis zum Speicherort:</strong><br />
                                Wir haben unsere Datenbank explizit in der <strong>Region EU (Frankfurt, Deutschland)</strong> konfiguriert
                                (über AWS Europe). Daten verlassen den europäischen Rechtsraum im Regelfall nicht.
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                <strong>Standardvertragsklauseln:</strong> Soweit Daten in ein Drittland übertragen werden, erfolgt dies auf Grundlage
                                der Standardvertragsklauseln der EU-Kommission.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-semibold mb-4">7. Kartendienste (Two-Click-Lösung)</h2>
                            <p className="text-slate-700 leading-relaxed">
                                Wir binden auf unserem &quot;First-Mover Map&quot; Demo-Produkt Landkarten des Dienstes openstreetmap.org (OpenStreetMap Foundation)
                                sowie Tiles von CartoDB ein.
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                <strong>Datenschutz durch Technik:</strong><br />
                                Um Ihre Privatsphäre zu schützen, haben wir eine <strong>Zwei-Klick-Lösung</strong> implementiert.
                                Beim Aufruf der Seite werden <strong>keine</strong> Daten an die Kartenanbieter übertragen.
                                Die Karte (und damit die Verbindung zu den Servern der Anbieter) wird erst geladen, wenn Sie
                                aktiv auf den Button &quot;Karte aktivieren&quot; klicken.
                            </p>
                            <p className="text-slate-700 leading-relaxed mt-2">
                                <strong>Datenübertragung:</strong><br />
                                Mit Klick auf den Button willigen Sie ein (Art. 6 Abs. 1 lit. a DSGVO), dass Ihre IP-Adresse an
                                OpenStreetMap und CartoDB übertragen wird, um die Kartenkacheln abzurufen.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-semibold mb-4">8. Ihre Rechte</h2>
                            <p className="text-slate-700 leading-relaxed">
                                Sie haben jederzeit das Recht:
                            </p>
                            <ul className="list-disc list-inside text-slate-700 mt-2 space-y-1">
                                <li>Auskunft über Ihre gespeicherten Daten zu erhalten (Art. 15 DSGVO)</li>
                                <li>Berichtigung unrichtiger Daten zu verlangen (Art. 16 DSGVO)</li>
                                <li>Löschung Ihrer Daten zu verlangen (Art. 17 DSGVO)</li>
                                <li>Einschränkung der Verarbeitung zu verlangen (Art. 18 DSGVO)</li>
                                <li>Datenübertragbarkeit zu verlangen (Art. 20 DSGVO)</li>
                                <li>Widerspruch gegen die Verarbeitung einzulegen (Art. 21 DSGVO)</li>
                                <li>Sich bei einer Aufsichtsbehörde zu beschweren (Art. 77 DSGVO)</li>
                            </ul>
                            <p className="text-slate-700 leading-relaxed mt-4">
                                <strong>Zuständige Aufsichtsbehörde:</strong><br />
                                Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen<br />
                                Kavalleriestraße 2-4<br />
                                40213 Düsseldorf
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-semibold mb-4">9. Änderungen</h2>
                            <p className="text-slate-700 leading-relaxed">
                                Diese Datenschutzerklärung kann von Zeit zu Zeit aktualisiert werden.
                                Die aktuelle Version ist stets auf dieser Seite verfügbar.
                            </p>
                            <p className="text-slate-500 text-sm mt-4">
                                Stand: Januar 2026
                            </p>
                        </section>

                    </section>
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-white border-t border-slate-900 py-16 mt-12">
                <div className="max-w-6xl mx-auto px-4 text-center">
                    <div className="flex items-center justify-center mb-8">
                        <img src="/logo.png" alt="FlurPilot Logo" className="h-10 w-auto opacity-80 hover:opacity-100 transition-opacity" />
                    </div>

                    <div className="flex justify-center gap-10 mb-10 text-xs font-bold uppercase tracking-widest">
                        <Link href="/impressum" className="text-slate-500 hover:text-slate-900 transition-colors">Impressum</Link>
                        <Link href="/datenschutz" className="text-slate-500 hover:text-slate-900 transition-colors">Datenschutz</Link>
                        <Link href="/agb" className="text-slate-500 hover:text-slate-900 transition-colors">AGB</Link>
                    </div>

                    <p className="text-slate-400 text-xs font-mono">
                        &copy; 2026 FlurPilot. Entwickelt in Deutschland.
                    </p>
                </div>
            </footer>
        </div>
    );
}
