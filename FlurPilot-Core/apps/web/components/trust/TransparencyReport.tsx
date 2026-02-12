"use client";

import { useTranslations } from 'next-intl';
import { Shield, Lock, Eye, AlertOctagon, FileCheck, Server, Globe, Hash } from 'lucide-react';
import { VerifiedSources } from './VerifiedSources';

export default function TransparencyReport() {
    const t = useTranslations('trust');

    // Mock Data for "Abwehr-Metriken" (Defense Metrics)
    const metrics = [
        {
            id: 'pii_redacted',
            label: t('metrics.piiRedacted'),
            value: '14,203',
            icon: Eye,
            color: 'text-emerald-500',
            bg: 'bg-emerald-500/10',
            desc: t('metrics.piiDesc')
        },
        {
            id: 'threats_blocked',
            label: t('metrics.threatsBlocked'),
            value: '842',
            icon: AlertOctagon,
            color: 'text-amber-500',
            bg: 'bg-amber-500/10',
            desc: t('metrics.threatsDesc')
        },
        {
            id: 'uptime',
            label: t('metrics.uptime'),
            value: '99.99%',
            icon: Server,
            color: 'text-indigo-500',
            bg: 'bg-indigo-500/10',
            desc: t('metrics.uptimeDesc')
        },
        {
            id: 'audits',
            label: t('metrics.auditsPassed'),
            value: '12',
            icon: FileCheck,
            color: 'text-blue-500',
            bg: 'bg-blue-500/10',
            desc: t('metrics.auditsDesc')
        }
    ];

    const logs = [
        { id: 1, action: 'ACCESS_DENIED', ip: '192.168.x.x', reason: 'Rate Limit Exceeded', time: '10:42:05', hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' },
        { id: 2, action: 'PII_REDACTION', doc: 'Flur_292_BPlan.pdf', entities: 3, time: '10:41:12', hash: '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92' },
        { id: 3, action: 'ENCRYPTION', asset: 'Internal_Memo.txt', method: 'AES-256', time: '10:38:55', hash: '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b' },
        { id: 4, action: 'ACCESS_GRANTED', user: 'Admin', scope: 'AuditLog', time: '10:35:20', hash: 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35' }
    ];

    return (
        <div className="space-y-6">
            {/* Header / Hero */}
            <div className="bg-slate-900 rounded-2xl p-6 text-white shadow-xl border border-slate-700">
                <div className="flex items-center gap-4 mb-4">
                    <div className="p-3 bg-emerald-500/20 rounded-xl border border-emerald-500/30">
                        <Shield className="w-8 h-8 text-emerald-400" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold tracking-tight">{t('reportTitle')}</h2>
                        <p className="text-slate-400 text-sm">{t('reportSubtitle')}</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
                    {metrics.map(m => (
                        <div key={m.id} className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
                            <div className="flex justify-between items-start mb-2">
                                <div className={`p-2 rounded-lg ${m.bg}`}>
                                    <m.icon size={18} className={m.color} />
                                </div>
                                <span className={`text-xl font-mono font-bold ${m.color}`}>{m.value}</span>
                            </div>
                            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wide">{m.label}</h3>
                            <p className="text-[10px] text-slate-500 mt-1">{m.desc}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Column 1: Verified Sources (New) */}
                <div className="lg:col-span-1">
                    <VerifiedSources />
                </div>

                {/* Column 2 & 3: Logs & Certs */}
                <div className="lg:col-span-2 space-y-6">

                    {/* Live Architecture Logs */}
                    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 flex items-center gap-2 mb-4">
                            <Server size={18} className="text-slate-400" />
                            {t('systemLogs')}
                            <span className="ml-auto flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-emerald-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                            </span>
                        </h3>
                        <div className="space-y-0">
                            {logs.map((log, i) => (
                                <div key={i} className="flex items-center justify-between text-xs py-3 border-b border-slate-50 last:border-0 font-mono hover:bg-slate-50 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <span className="text-slate-400">{log.time}</span>
                                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${log.action.includes('DENIED') ? 'bg-red-50 text-red-600' :
                                            log.action.includes('REDACTION') ? 'bg-amber-50 text-amber-600' :
                                                'bg-emerald-50 text-emerald-600'
                                            }`}>
                                            {log.action}
                                        </span>
                                        <span className="text-slate-600 truncate max-w-[150px]">
                                            {log.reason || log.doc || log.asset || log.user}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-1 text-slate-300" title="Merkle Hash">
                                        <Hash size={10} />
                                        <span className="text-[10px] truncate w-16">{log.hash.substring(0, 10)}...</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Compliance & Certs */}
                    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 flex items-center gap-2 mb-4">
                            <Lock size={18} className="text-slate-400" />
                            {t('compliance')}
                        </h3>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 flex items-center gap-3">
                                <div className="bg-white p-2 rounded-lg shadow-sm border border-slate-100">
                                    <Globe size={20} className="text-blue-500" />
                                </div>
                                <div>
                                    <div className="font-bold text-slate-700 text-sm">GDPR / DSGVO</div>
                                    <div className="text-[10px] text-emerald-600 font-semibold">{t('compliant')}</div>
                                </div>
                            </div>
                            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 flex items-center gap-3">
                                <div className="bg-white p-2 rounded-lg shadow-sm border border-slate-100">
                                    <Server size={20} className="text-purple-500" />
                                </div>
                                <div>
                                    <div className="font-bold text-slate-700 text-sm">ISO 27001</div>
                                    <div className="text-[10px] text-slate-500 font-semibold">{t('aligned')}</div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-6 p-4 bg-amber-50 rounded-xl border border-amber-100 text-xs text-amber-800">
                            <strong>{t('transparencyNote')}:</strong> {t('transparencyBody')}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
}
