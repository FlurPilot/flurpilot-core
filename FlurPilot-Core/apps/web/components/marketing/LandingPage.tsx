'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
    CheckCircle2,
    Download,
    AlertTriangle,
    Clock,
    FileSearch,
    Database,
    Map,
    FileText,
    Crosshair,
    Zap,
    Mail,
    ArrowRight,
    TrendingUp
} from 'lucide-react';

import { submitEmail } from '../../lib/supabase';
import { FadeIn } from './FadeIn';
import { MarketingSection } from './MarketingSection';
import { MarketingBadge } from './MarketingBadge';
import { MarketingAccordion } from './MarketingAccordion';

export default function LandingPage() {
    const [email, setEmail] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitted, setSubmitted] = useState(false);
    const [consent, setConsent] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError(null);

        try {
            if (!consent) {
                setError('Bitte stimmen Sie den Datenschutz-Hinweisen zu.');
                setIsSubmitting(false);
                return;
            }

            // Production: Call Supabase Edge Function
            const result = await submitEmail(email);

            if (!result.success) {
                throw new Error(result.error || 'Submission failed');
            }

            setSubmitted(true);
        } catch (err: unknown) {
            console.error('Submission error:', err);
            setError('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
            setIsSubmitting(false);
        }
    };

    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        // Focus the email input for better UX
        setTimeout(() => {
            const input = document.querySelector('input[type="email"]') as HTMLInputElement;
            if (input) input.focus();
        }, 500);
    };

    return (
        <div className="min-h-screen bg-white font-sans text-slate-900 antialiased selection:bg-emerald-100 selection:text-emerald-900">

            {/* ═══════════════════════════════════════════════════════════════════════
          1. HERO SECTION - 100% Freebie Focus
      ═══════════════════════════════════════════════════════════════════════ */}
            <header className="relative bg-white border-b border-slate-900 overflow-hidden">
                {/* Navigation */}
                <nav className="max-w-6xl mx-auto px-4 md:px-8 py-5 flex items-center justify-between border-b border-slate-100">
                    <div className="flex items-center gap-2.5">
                        <img src="/logo.png" alt="FlurPilot Logo" className="h-10 w-auto" />
                    </div>
                    <a href="#faq" className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors uppercase tracking-wide">
                        Häufige Fragen
                    </a>
                </nav>

                {/* Hero Content */}
                <div className="max-w-6xl mx-auto px-4 md:px-8 pt-16 pb-24 md:pt-24 md:pb-32">
                    <FadeIn>
                        <div className="max-w-4xl mx-auto text-center">
                            <MarketingBadge variant="emerald">First-Mover Map 2026</MarketingBadge>

                            <h1 className="mt-8 text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-slate-900 leading-[1.05] max-w-4xl mx-auto text-balance">
                                Finden Sie Solarpark&#8209;Flächen <br className="hidden md:block" />
                                <span className="text-emerald-600">vor dem Wettbewerb.</span>
                            </h1>

                            <p className="mt-8 text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed font-light">
                                Die neue <strong className="text-slate-900 font-semibold">First-Mover Map</strong> zeigt Ihnen interaktiv,
                                wie Sie vor-qualifizierte Leads finden – testen Sie die Demo
                                sofort in Ihrem Browser.
                            </p>

                            {/* Email Capture Form */}
                            <div id="download-form" className="mt-12 max-w-lg mx-auto">
                                {!submitted ? (
                                    <form onSubmit={handleSubmit} className="space-y-4">
                                        <div className="relative">
                                            <div className="relative flex flex-col sm:flex-row border border-slate-900 bg-white h-auto sm:h-14 items-stretch overflow-hidden">
                                                <input
                                                    type="email"
                                                    required
                                                    placeholder="ihre@firmen-email.de"
                                                    value={email}
                                                    onChange={(e) => setEmail(e.target.value)}
                                                    className="flex-1 px-5 h-14 sm:h-full bg-transparent border-none focus:outline-none focus:ring-0 text-slate-900 placeholder:text-slate-400 font-mono text-sm"
                                                />
                                                <motion.button
                                                    type="submit"
                                                    disabled={isSubmitting}
                                                    whileHover={{ scale: 1.01 }}
                                                    whileTap={{ scale: 0.99 }}
                                                    className="px-8 h-14 sm:h-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold uppercase tracking-wider text-sm flex items-center justify-center gap-2 transition-colors whitespace-nowrap"
                                                >
                                                    {isSubmitting ? (
                                                        <motion.div
                                                            className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                                                            animate={{ rotate: 360 }}
                                                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                                        />
                                                    ) : (
                                                        <>
                                                            <Download className="w-5 h-5" strokeWidth={2} />
                                                            Jetzt Map anfordern
                                                        </>
                                                    )}
                                                </motion.button>
                                            </div>
                                        </div>

                                        <div className="flex items-start justify-center gap-3 text-left px-2">
                                            <input
                                                id="consent"
                                                type="checkbox"
                                                checked={consent}
                                                onChange={(e) => setConsent(e.target.checked)}
                                                className="mt-1 h-4 w-4 rounded-none border-slate-300 text-slate-900 focus:ring-slate-900 focus:ring-offset-0 bg-white"
                                            />
                                            <label htmlFor="consent" className="text-sm text-slate-600 leading-snug">
                                                Ja, ich möchte informiert werden, sobald <span className="font-bold text-slate-900">FlurPilot Core</span> fertig ist. (Widerruf jederzeit möglich, siehe <Link href="/datenschutz" target="_blank" className="underline hover:text-slate-900">Datenschutz</Link>)
                                            </label>
                                        </div>
                                        {error && (
                                            <p className="text-red-600 text-sm font-bold text-center animate-pulse">
                                                {error}
                                            </p>
                                        )}

                                    </form>
                                ) : (
                                    <motion.div
                                        initial={{ scale: 0.95, opacity: 0 }}
                                        animate={{ scale: 1, opacity: 1 }}
                                        className="p-8 bg-emerald-50 border border-emerald-900 text-center"
                                    >
                                        <motion.div
                                            initial={{ scale: 0 }}
                                            animate={{ scale: 1 }}
                                            transition={{ type: "spring", stiffness: 200, delay: 0.1 }}
                                        >
                                            <CheckCircle2 className="w-12 h-12 mx-auto mb-4 text-emerald-700" strokeWidth={1.5} />
                                        </motion.div>
                                        <h3 className="font-bold text-lg text-emerald-900 uppercase tracking-wide">Bitte E-Mail bestätigen!</h3>
                                        <p className="text-sm text-emerald-800 mt-2 font-mono">Wir haben Ihnen einen Bestätigungs-Link gesendet. <br />Erst danach erhalten Sie die Map.</p>
                                    </motion.div>
                                )}
                            </div>
                        </div>
                    </FadeIn>
                </div>
            </header >

            {/* ═══════════════════════════════════════════════════════════════════════
          2. DIE DIAGNOSE - Das Problembewusstsein
      ═══════════════════════════════════════════════════════════════════════ */}
            <section className="bg-slate-50 border-b border-slate-900" >
                <MarketingSection>
                    <div className="grid lg:grid-cols-2 gap-16 items-start">
                        <FadeIn>
                            <MarketingBadge variant="slate">Das Problem</MarketingBadge>
                            <h2 className="mt-6 text-3xl md:text-5xl font-bold text-slate-900 leading-tight">
                                Das &quot;Seite 47&quot; Problem der Flächenakquise.
                            </h2>
                            <p className="mt-6 text-slate-600 text-lg leading-relaxed">
                                Der entscheidende Hinweis auf eine verfügbare Fläche – der <strong className="text-slate-900 font-semibold">Aufstellungsbeschluss</strong> –
                                versteckt sich oft auf Seite 47 eines PDF-Anhangs im Ratsinformationssystem einer
                                von 11.000 Kommunen. Monate bevor es in die Zeitung kommt.
                            </p>

                            <ul className="mt-10 space-y-0 border-t border-slate-200">
                                {[
                                    { icon: Clock, text: "Manuelle Recherche verbrennt 20+ Stunden pro Woche.", color: "text-slate-900" },
                                    { icon: AlertTriangle, text: "Wer es in der Zeitung liest, ist zu spät – die Fläche ist weg.", color: "text-slate-900" },
                                    { icon: FileSearch, text: "Relevante Details (Flurnummern) gehen im Amtsdeutsch unter.", color: "text-slate-900" }
                                ].map((item, idx) => (
                                    <li key={idx} className="flex items-center gap-6 py-6 border-b border-slate-200 group hover:bg-white transition-colors px-4 -mx-4">
                                        <div className={`text-slate-400 group-hover:text-emerald-600 transition-colors`}>
                                            <item.icon className="w-6 h-6" strokeWidth={1.5} />
                                        </div>
                                        <span className="text-slate-700 font-medium">{item.text}</span>
                                    </li>
                                ))}
                            </ul>
                        </FadeIn>

                        <FadeIn delay={0.15}>
                            <div className="bg-white border border-slate-900 p-0 relative">
                                <div className="absolute top-0 left-0 w-full h-1 bg-slate-900"></div>
                                <div className="p-8">
                                    <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-4">
                                        <Database className="w-5 h-5 text-emerald-600" strokeWidth={1.5} />
                                        <span className="text-xs font-bold text-slate-900 uppercase tracking-widest">Status Quo Analyse</span>
                                    </div>
                                    <div className="space-y-0 font-mono text-sm">
                                        <div className="flex justify-between py-4 border-b border-slate-100">
                                            <span className="text-slate-500">Kommunen in Deutschland</span>
                                            <span className="text-slate-900 font-bold">~11.000</span>
                                        </div>
                                        <div className="flex justify-between py-4 border-b border-slate-100">
                                            <span className="text-slate-500">RIS-Systeme</span>
                                            <span className="text-slate-900 font-bold">SessionNet, Allris</span>
                                        </div>
                                        <div className="flex justify-between py-4 border-b border-slate-100">
                                            <span className="text-slate-500">Protokolle / Woche</span>
                                            <span className="text-slate-900 font-bold">2.500+</span>
                                        </div>
                                        <div className="flex justify-between py-4 bg-slate-50 -mx-8 px-8 border-b border-slate-100 mt-2">
                                            <span className="text-slate-500">Risiko: Verpasste Chance</span>
                                            <span className="text-red-600 font-bold">95%</span>
                                        </div>
                                    </div>
                                    <p className="mt-8 text-[10px] uppercase tracking-widest text-slate-400">
                                        *Branchenschätzung 2026
                                    </p>
                                </div>
                            </div>
                        </FadeIn>
                    </div>
                </MarketingSection>
            </section >

            {/* ═══════════════════════════════════════════════════════════════════════
          3. DAS FREEBIE IM DETAIL - Die schnelle Lösung
      ═══════════════════════════════════════════════════════════════════════ */}
            <MarketingSection className="bg-white" >
                <FadeIn>
                    <div className="text-left mb-20">
                        <MarketingBadge variant="emerald">First-Mover Map</MarketingBadge>
                        <h2 className="mt-6 text-4xl md:text-5xl font-bold text-slate-900 max-w-2xl leading-tight">
                            Ihr erster Schritt zum Wissensvorsprung.
                        </h2>
                        <p className="mt-6 text-slate-600 text-lg max-w-2xl">
                            Kein langes PDF-Lesen mehr. Die interaktive Map zeigt Ihnen sofort das Ergebnis einer erfolgreichen Recherche.
                        </p>
                    </div>
                </FadeIn>

                <div className="grid md:grid-cols-3 gap-0 border-t border-l border-slate-200">
                    {[
                        {
                            icon: Map,
                            title: "Interaktive Karte",
                            desc: "Zoomen Sie auf die Flurstücke. Sehen Sie die genaue Lage (OpenStreetMap) und die Grenzen.",
                        },
                        {
                            icon: Crosshair,
                            title: "Strukturierte Geodaten",
                            desc: "Detaillierte Polygone statt grober Ortsmarken. Inklusive Flurstücks-Details (sofern verfügbar).",
                        },
                        {
                            icon: FileText,
                            title: "Beschluss-Details",
                            desc: "Alle Metadaten (B-Plan Nr., Datum, Bezeichnung) und direkter Link zur Original-Quelle.",
                        }
                    ].map((card, idx) => (
                        <FadeIn key={idx} delay={idx * 0.1}>
                            <div className="bg-white p-10 border-r border-b border-slate-200 h-full flex flex-col hover:bg-slate-50 transition-colors group">
                                <div className="w-12 h-12 bg-emerald-100 text-emerald-700 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                                    <card.icon className="w-6 h-6" strokeWidth={1.5} />
                                </div>
                                <h3 className="font-bold text-slate-900 text-xl mb-3">{card.title}</h3>
                                <p className="text-slate-500 text-sm leading-relaxed flex-grow">{card.desc}</p>
                            </div>
                        </FadeIn>
                    ))}
                </div>
            </MarketingSection >

            {/* ═══════════════════════════════════════════════════════════════════════
          4. DER "GAP" - Übergang zum Paid Tool
      ═══════════════════════════════════════════════════════════════════════ */}
            <MarketingSection dark className="bg-slate-950 border-t-4 border-emerald-600" >
                <div className="grid lg:grid-cols-2 gap-20 items-center">
                    <FadeIn>
                        <MarketingBadge variant="slate">Der nächste Schritt</MarketingBadge>
                        <h2 className="mt-6 text-4xl md:text-5xl font-bold leading-tight text-white">
                            Ein Lead ist gut. <br />
                            <span className="text-emerald-500">Automatisierung ist besser.</span>
                        </h2>
                        <p className="mt-8 text-slate-400 text-lg leading-relaxed font-light">
                            Die First-Mover Map ist nur ein Beispiel. Aber haben Sie die Ressourcen,
                            dies für 400 Landkreise – jede Woche – manuell zu tun?
                        </p>
                        <p className="mt-6 text-slate-400 text-lg leading-relaxed font-light">
                            <strong className="text-white font-medium">FlurPilot Core</strong> automatisiert exakt diesen Prozess.
                            KI-gestützte Extraktion. Skalierbare Überwachung. KI-geprüfte Geo-Leads direkt in Ihr Postfach.
                        </p>

                        <div className="mt-12 flex flex-col sm:flex-row gap-0">
                            <button
                                onClick={() => document.getElementById('download-form')?.scrollIntoView({ behavior: 'smooth' })}
                                className="px-8 py-4 bg-emerald-600 text-white font-bold uppercase tracking-wider text-sm hover:bg-emerald-500 transition-colors inline-flex items-center justify-center gap-3">
                                <Zap className="w-5 h-5" strokeWidth={2} />
                                Jetzt Map anfordern
                            </button>
                            <span className="px-6 py-4 border border-white/10 text-slate-400 text-xs uppercase tracking-wider flex items-center">
                                Nur für institutionelle Kunden
                            </span>
                        </div>
                    </FadeIn>

                    <FadeIn delay={0.15}>
                        <div className="bg-slate-900 border border-slate-800 p-4 md:p-12 relative overflow-x-auto">

                            <table className="w-full text-left text-sm relative min-w-[300px]">
                                <thead>
                                    <tr className="border-b border-slate-800">
                                        <th className="pb-6 text-slate-500 font-normal uppercase tracking-wider text-xs">Funktion</th>
                                        <th className="pb-6 text-slate-400 font-medium text-center uppercase tracking-wider text-xs">Manuell</th>
                                        <th className="pb-6 text-emerald-500 font-bold text-center uppercase tracking-wider text-xs">FlurPilot</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800">
                                    {[
                                        ["Recherche-Radius", "Lokal", "Deutschlandweit"],
                                        ["Zeitaufwand", "20h / Woche", "0 Std."],
                                        ["Daten-Tiefe", "PDF lesen", "KI-Extraktion"],
                                        ["Geo-Validierung", "Manuell", "Flurstücks-Abgleich"],
                                        ["Output-Format", "Excel / Notizen", "GeoJSON / KML"]
                                    ].map(([feature, manual, auto], i) => (
                                        <tr key={i} className="group hover:bg-slate-800/50 transition-colors">
                                            <td className="py-5 text-slate-300 font-medium">{feature}</td>
                                            <td className="py-5 text-slate-600 text-center font-mono text-xs">{manual}</td>
                                            <td className="py-5 text-white font-bold text-center font-mono text-xs text-slate-200">{auto}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </FadeIn>
                </div>
            </MarketingSection >

            {/* ═══════════════════════════════════════════════════════════════════════
          6. ROI RECHNUNG - Der Wert-Anker
      ═══════════════════════════════════════════════════════════════════════ */}
            <section className="bg-emerald-50 border-b border-slate-900 py-24" >
                <div className="max-w-4xl mx-auto px-4 text-center">
                    <FadeIn>
                        <div className="inline-flex items-center gap-3 mb-6">
                            <TrendingUp className="w-6 h-6 text-slate-900" strokeWidth={1.5} />
                            <span className="font-mono font-bold text-slate-900 text-xl tracking-tighter">WERT-KALKULATION</span>
                        </div>
                        <p className="text-slate-600 mb-10 text-lg">Der Wert der Automatisierung vs. Manuelle Arbeit</p>

                        <div className="bg-white border-2 border-slate-900 text-left w-full max-w-2xl mx-auto">
                            <div className="p-8 space-y-4">
                                <div className="flex justify-between gap-12 text-sm border-b border-slate-100 pb-4">
                                    <span className="text-slate-500 uppercase tracking-wide">Tagessatz Consultant (Recherche)</span>
                                    <span className="text-slate-900 font-mono">1.200,00 €</span>
                                </div>
                                <div className="flex justify-between gap-12 text-sm">
                                    <span className="text-slate-500 uppercase tracking-wide">First-Mover Map (Freebie)</span>
                                    <span className="text-emerald-600 font-bold font-mono">0,00 €</span>
                                </div>
                            </div>
                            <div className="flex justify-between gap-12 text-lg bg-slate-900 text-white px-8 py-6">
                                <span className="font-bold uppercase tracking-wider text-sm sm:text-base">Rechnerischer Gegenwert:</span>
                                <span className="text-emerald-400 font-mono text-xl sm:text-2xl">1.200,00 €</span>
                            </div>
                        </div>

                        <p className="mt-8 text-[10px] uppercase tracking-widest text-slate-400">
                            * Potenzielle Einsparung mit FlurPilot Core: bis zu 50.000 € / Jahr<br />
                            (Basis: Einsparung von ca. 0,5 Personalstellen inkl. Lohnnebenkosten & Lizenzen)
                        </p>
                    </FadeIn>
                </div>
            </section >

            {/* ═══════════════════════════════════════════════════════════════════════
          7. FAQ & FINAL CTA
      ═══════════════════════════════════════════════════════════════════════ */}
            <MarketingSection id="faq" className="bg-white" >
                <FadeIn>
                    <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-16 text-center">Häufige Fragen</h2>

                    <div className="max-w-3xl mx-auto border-t border-slate-200 mb-24">
                        <MarketingAccordion
                            question="Was genau erhalte ich?"
                            answer="Sie erhalten eine interaktive HTML-Datei ('First-Mover Map'). Diese öffnet sich in Ihrem Browser und enthält einen echten, vor-qualifizierten Lead inklusive Flurstücks-Polygonen und Beschlussdaten."
                            defaultOpen
                        />
                        <MarketingAccordion
                            question="Muss ich ein Abo abschließen?"
                            answer="Nein. Es entstehen keine Kosten. Das Dokument dient als Demo für die Datenqualität von FlurPilot."
                        />
                        <MarketingAccordion
                            question="Für wen ist FlurPilot Core gedacht?"
                            answer="FlurPilot Core richtet sich an gewerbliche Projektentwickler (Utility Scale >10MW), EPC-Unternehmen und Infrastruktur-Fonds mit entsprechendem Flächenbedarf. Privatpersonen sind nicht unsere Zielgruppe."
                        />
                        <MarketingAccordion
                            question="Kann ich später auf die Vollversion upgraden?"
                            answer="Ja. Sie werden benachrichtigt, sobald FlurPilot Core verfügbar ist."
                        />
                    </div>
                </FadeIn>

                {/* Final CTA */}
                <FadeIn>
                    <div className="bg-slate-900 p-12 md:p-20 text-center text-white relative overflow-hidden max-w-4xl mx-auto border border-slate-800">

                        <div className="relative z-10">
                            <Mail className="w-12 h-12 mx-auto mb-6 text-emerald-500" strokeWidth={1.5} />
                            <h2 className="text-3xl md:text-5xl font-bold mb-6 tracking-tight">Starten Sie jetzt Ihre Recherche.</h2>
                            <p className="text-slate-400 mb-10 text-lg font-light">Sofort verfügbar. Transparenter Datenschutz.</p>

                            <motion.button
                                onClick={scrollToTop}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                className="inline-flex items-center justify-center gap-3 px-10 py-5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold uppercase tracking-widest text-sm transition-colors"
                            >
                                Jetzt Map anfordern
                                <ArrowRight className="w-5 h-5" strokeWidth={2} />
                            </motion.button>
                        </div>
                    </div>
                </FadeIn>
            </MarketingSection >

            {/* ═══════════════════════════════════════════════════════════════════════
          FOOTER
      ═══════════════════════════════════════════════════════════════════════ */}
            <footer className="bg-white border-t border-slate-900 py-16" >
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
            </footer >
        </div >
    );
}
