'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function AGB() {
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
                <h1 className="text-3xl font-bold text-slate-900 mb-8">Allgemeine Geschäftsbedingungen</h1>

                <div className="prose prose-slate max-w-none space-y-8">

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 1 Geltungsbereich</h2>
                        <p className="text-slate-700 leading-relaxed">
                            (1) Diese Allgemeinen Geschäftsbedingungen (AGB) gelten für alle Verträge zwischen
                            Stephan Ochmann, c/o Postflex #586, Emsdettener Straße 10, D-48268 Greven
                            (nachfolgend &quot;Anbieter&quot;) und dem Nutzer (nachfolgend &quot;Kunde&quot;) über die Nutzung
                            des Dienstes &quot;FlurPilot&quot;.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (2) FlurPilot richtet sich ausschließlich an Unternehmer im Sinne des § 14 BGB.
                            Verbraucher im Sinne des § 13 BGB sind von der Nutzung ausgeschlossen.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (3) <strong>Dual-Use & Compliance:</strong> Der Kunde versichert, die Software nicht für militärische Zwecke,
                            zur Entwicklung von Waffensystemen oder für Maßnahmen zu nutzen, die der internen Repression oder der
                            Verletzung von Menschenrechten dienen. Der Kunde bestätigt, dass er nicht auf Sanktionslisten der EU
                            oder der Vereinten Nationen geführt wird.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 2 Leistungsbeschreibung</h2>
                        <p className="text-slate-700 leading-relaxed">
                            (1) FlurPilot stellt mit der &quot;First-Mover Map&quot; beispielhafte Informationen zu potenziellen Flächen für Erneuerbare-Energien-Projekte bereit.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (2) Die kostenlose &quot;First-Mover Map&quot; umfasst:<br />
                            • Eine interaktive Karte zur Visualisierung von Geodaten (als HTML-Datei)<br />
                            • Exemplarische Informationen zu Flurstücken und Beschlüssen<br />
                            • Die Datei ist zur lokalen Nutzung im Browser bestimmt
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (3) Der Anbieter gewährleistet keine Vollständigkeit, Richtigkeit oder Aktualität
                            der durch den Dienst bereitgestellten Informationen. Der Kunde ist verpflichtet,
                            die bereitgestellten Informationen vor einer geschäftlichen Entscheidung eigenverantwortlich
                            zu überprüfen. Eine Verwendung ungeprüfter Daten erfolgt auf eigene Verantwortung.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 3 Kostenlose Inhalte (Freebie)</h2>
                        <p className="text-slate-700 leading-relaxed">
                            (1) Die First-Mover Map wird kostenlos zur Verfügung gestellt.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (2) Mit der Angabe Ihrer E-Mail-Adresse willigen Sie ein, Informationen über
                            FlurPilot und verwandte Produkte zu erhalten. Diese Einwilligung können Sie
                            jederzeit widerrufen.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (3) Ein Anspruch auf dauerhaften Zugang zur First-Mover Map besteht nicht. Der
                            Anbieter behält sich vor, das Angebot jederzeit zu ändern oder einzustellen.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 4 Geistiges Eigentum</h2>
                        <p className="text-slate-700 leading-relaxed">
                            (1) Alle Inhalte der First-Mover Map (Texte, Grafiken, Datenstrukturen) sind
                            urheberrechtlich geschützt.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (2) Der Kunde erhält ein einfaches, nicht übertragbares Nutzungsrecht für den
                            eigenen Geschäftsbetrieb. Eine Weitergabe an Dritte oder kommerzielle
                            Weiterverwendung ist ohne schriftliche Genehmigung untersagt.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 5 Haftung</h2>
                        <p className="text-slate-700 leading-relaxed">
                            (1) Der Anbieter haftet unbeschränkt für Schäden aus der Verletzung des Lebens,
                            des Körpers oder der Gesundheit sowie bei Vorsatz und grober Fahrlässigkeit.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (2) Bei leichter Fahrlässigkeit haftet der Anbieter nur bei Verletzung
                            wesentlicher Vertragspflichten (Kardinalpflichten), deren Erfüllung die
                            ordnungsgemäße Durchführung des Vertrages erst ermöglicht.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (3) Die Haftung für mittelbare Schäden, insbesondere entgangenen Gewinn, ist
                            – soweit gesetzlich zulässig – ausgeschlossen.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (4) Der Anbieter übernimmt keine Haftung für Entscheidungen, die auf Basis
                            der durch FlurPilot bereitgestellten Informationen getroffen werden.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (5) Die Haftung nach dem Produkthaftungsgesetz bleibt von den vorstehenden
                            Regelungen unberührt.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 6 Datenschutz</h2>
                        <p className="text-slate-700 leading-relaxed">
                            Die Erhebung und Verarbeitung personenbezogener Daten erfolgt gemäß unserer{' '}
                            <Link href="/datenschutz" className="text-emerald-600 hover:text-emerald-700 underline">
                                Datenschutzerklärung
                            </Link>.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold mb-4">§ 7 Schlussbestimmungen</h2>
                        <p className="text-slate-700 leading-relaxed">
                            (1) Es gilt das Recht der Bundesrepublik Deutschland unter Ausschluss des
                            UN-Kaufrechts (CISG).
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (2) Gerichtsstand für alle Streitigkeiten ist – soweit gesetzlich zulässig –
                            der Sitz des Anbieters.
                        </p>
                        <p className="text-slate-700 leading-relaxed mt-2">
                            (3) Sollten einzelne Bestimmungen dieser AGB unwirksam sein, bleibt die
                            Wirksamkeit der übrigen Bestimmungen unberührt.
                        </p>
                        <p className="text-slate-500 text-sm mt-6">
                            Stand: Januar 2026
                        </p>
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
