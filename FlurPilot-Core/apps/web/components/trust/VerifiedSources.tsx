"use client";

import { CheckCircle, AlertTriangle, RefreshCw, Server } from 'lucide-react';
import { useTranslations } from 'next-intl';

interface Source {
    id: string;
    name: string;
    region: string;
    status: 'online' | 'maintenance' | 'offline';
    lastCrawled: string;
    latency: number;
}

const mockSources: Source[] = [
    { id: 'ris-muc', name: 'Ratsinfo München (RIS)', region: 'Bayern', status: 'online', lastCrawled: '2 min ago', latency: 45 },
    { id: 'ris-ber', name: 'Berlin Allris', region: 'Berlin', status: 'online', lastCrawled: '5 min ago', latency: 62 },
    { id: 'ris-hbg', name: 'Hamburg Transparenzportal', region: 'Hamburg', status: 'maintenance', lastCrawled: '2h ago', latency: 120 },
    { id: 'ris-stg', name: 'Stuttgart OpenData', region: 'BaWü', status: 'online', lastCrawled: '1 min ago', latency: 38 },
    { id: 'ris-koe', name: 'Köln Ratssystem', region: 'NRW', status: 'offline', lastCrawled: '1d ago', latency: 0 },
];

export function VerifiedSources() {
    const t = useTranslations('trust');

    return (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm h-full">
            <div className="flex items-center justify-between mb-6">
                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                    <Server size={18} className="text-slate-400" />
                    Verified Sources
                </h3>
                <div className="flex items-center gap-2">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span>
                    <span className="text-xs font-mono text-emerald-600 font-bold">LIVE</span>
                </div>
            </div>

            <div className="space-y-3">
                {mockSources.map((source) => (
                    <div key={source.id} className="flex items-center justify-between p-3 bg-slate-50/50 rounded-xl border border-slate-100 hover:border-slate-200 transition-colors">
                        <div className="flex items-center gap-3">
                            <div className={`p-1.5 rounded-full ${source.status === 'online' ? 'bg-emerald-100/50 text-emerald-600' :
                                source.status === 'maintenance' ? 'bg-amber-100/50 text-amber-600' :
                                    'bg-red-100/50 text-red-600'
                                }`}>
                                {source.status === 'online' ? <CheckCircle size={14} /> :
                                    source.status === 'maintenance' ? <RefreshCw size={14} /> :
                                        <AlertTriangle size={14} />}
                            </div>
                            <div>
                                <div className="text-xs font-bold text-slate-700">{source.name}</div>
                                <div className="text-[10px] text-slate-400">{source.region} • {source.lastCrawled}</div>
                            </div>
                        </div>

                        <div className="text-right">
                            {source.status !== 'offline' && (
                                <div className="text-[10px] font-mono text-slate-400">
                                    {source.latency}ms
                                </div>
                            )}
                            <div className={`text-[10px] font-bold ${source.status === 'online' ? 'text-emerald-600' :
                                source.status === 'maintenance' ? 'text-amber-600' :
                                    'text-red-500'
                                }`}>
                                {t(`status.${source.status}`)}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-4 pt-4 border-t border-slate-100 text-center">
                <button className="text-xs text-slate-500 hover:text-emerald-600 font-medium flex items-center justify-center gap-1 w-full">
                    <RefreshCw size={12} />
                    {t('verifiedSources.refresh')}
                </button>
            </div>
        </div>
    );
}
