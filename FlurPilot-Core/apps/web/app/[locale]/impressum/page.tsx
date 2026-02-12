'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function Impressum() {
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
                <h1 className="text-3xl font-bold text-slate-900 mb-8">Impressum</h1>

                <div className="prose prose-slate max-w-none">
                    <h2 className="text-xl font-semibold mt-8 mb-4">Angaben gemäß § 5 DDG</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Stephan Ochmann<br />
                        c/o Postflex #586<br />
                        Emsdettener Straße 10<br />
                        D-48268 Greven
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">Kontakt</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Telefon: +49 (0) 2363 8072515<br />
                        E-Mail: info@flurpilot.de
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Stephan Ochmann<br />
                        c/o Postflex #586<br />
                        Emsdettener Straße 10<br />
                        D-48268 Greven
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">EU-Streitschlichtung</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit:{' '}
                        <a
                            href="https://ec.europa.eu/consumers/odr/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-emerald-600 hover:text-emerald-700 underline"
                        >
                            https://ec.europa.eu/consumers/odr/
                        </a>
                    </p>
                    <p className="text-slate-700 leading-relaxed mt-2">
                        Unsere E-Mail-Adresse finden Sie oben im Impressum.
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">Verbraucherstreitbeilegung / Universalschlichtungsstelle</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer
                        Verbraucherschlichtungsstelle teilzunehmen.
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">Haftung für Inhalte</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten
                        nach den allgemeinen Gesetzen verantwortlich. Wir bemühen uns, die Inhalte unserer Seite aktuell zu halten.
                        Trotz sorgfältiger Bearbeitung bleibt eine Haftung ausgeschlossen. Insbesondere übernehmen wir
                        <strong>keine Garantie für die Richtigkeit, Vollständigkeit und Aktualität</strong> der bereitgestellten Informationen.
                    </p>
                    <p className="text-slate-700 leading-relaxed mt-2">
                        Nach §§ 8 bis 10 DDG sind wir als Diensteanbieter zudem nicht verpflichtet, übermittelte oder gespeicherte fremde
                        Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige
                        Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den
                        allgemeinen Gesetzen bleiben hiervon unberührt.
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">Haftung für Links</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen
                        Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen.
                        Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber
                        der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung
                        auf mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der
                        Verlinkung nicht erkennbar.
                    </p>

                    <h2 className="text-xl font-semibold mt-8 mb-4">Urheberrecht</h2>
                    <p className="text-slate-700 leading-relaxed">
                        Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen
                        dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art
                        der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen
                        Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind
                        nur für den privaten, nicht kommerziellen Gebrauch gestattet.
                    </p>
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
