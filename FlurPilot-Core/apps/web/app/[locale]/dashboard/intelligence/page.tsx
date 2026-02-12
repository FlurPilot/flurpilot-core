"use client";

import DocumentFeed from '@/components/intelligence/DocumentFeed';
import AnalystConsole from '@/components/intelligence/AnalystConsole';

export default function IntelligencePage() {
    return (
        <div className="h-[calc(100vh-64px)] p-6 bg-slate-50 overflow-hidden flex flex-col gap-4">
            <header className="flex-shrink-0 flex justify-between items-center">
                <div>
                    <h1 className="text-xl font-bold text-slate-900 tracking-tight">Intelligence Feed</h1>
                    <p className="text-sm text-slate-500">Real-time municipal analysis & decision support</p>
                </div>
                <div className="flex gap-2">
                    <span className="px-2.5 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-semibold border border-emerald-200 flex items-center gap-1.5">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                        </span>
                        Live Connection
                    </span>
                </div>
            </header>

            <div className="flex-1 flex gap-6 min-h-0">
                {/* Left: Document Feed (40%) */}
                <div className="w-[400px] flex-shrink-0 flex flex-col gap-3">
                    <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">Incoming Signals</h2>
                    <DocumentFeed />
                </div>

                {/* Right: Analyst Console (Rest) */}
                <div className="flex-1 flex flex-col gap-3">
                    <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">AI Analyst Console</h2>
                    <AnalystConsole />
                </div>
            </div>
        </div>
    );
}
