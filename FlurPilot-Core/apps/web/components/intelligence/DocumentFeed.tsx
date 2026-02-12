"use client";

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase';
import { FileText, ExternalLink, Calendar, MapPin, Loader2 } from 'lucide-react';
import { useTranslations } from 'next-intl';

interface EvidenceDoc {
    id: string;
    title?: string;
    url: string;
    published_date?: string;
    doc_type: string;
    scout_profiles?: { name?: string } | null;
}

export default function DocumentFeed() {
    const [docs, setDocs] = useState<EvidenceDoc[]>([]);
    const [loading, setLoading] = useState(true);
    const supabase = createClient();
    const t = useTranslations('intelligence');

    useEffect(() => {
        async function fetchDocs() {
            const { data, error } = await supabase
                .from('evidence_docs')
                .select('*, scout_profiles(name)')
                .order('published_date', { ascending: false })
                .limit(50);

            if (data) setDocs(data as EvidenceDoc[]);
            if (error) console.error("Error fetching docs:", error);
            setLoading(false);
        }

        fetchDocs();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                <Loader2 className="animate-spin" />
                <span className="text-sm">{t('loadingFeed')}</span>
            </div>
        );
    }

    if (docs.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-slate-400 p-8 text-center border-2 border-dashed border-slate-200 rounded-xl">
                <p>{t('noSignals')}</p>
            </div>
        );
    }

    return (
        <div className="space-y-3 h-full overflow-y-auto pr-2">
            {docs.map((doc) => (
                <div key={doc.id} className="bg-white p-3 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-all group">
                    <div className="flex justify-between items-start">
                        <div className="flex items-start gap-3">
                            <div className="p-2 bg-slate-50 rounded-lg group-hover:bg-emerald-50 transition-colors flex-shrink-0">
                                <FileText className="w-4 h-4 text-slate-400 group-hover:text-emerald-600" />
                            </div>
                            <div className="min-w-0">
                                <h3 className="font-semibold text-sm text-slate-900 line-clamp-2 leading-snug group-hover:text-emerald-700 transition-colors">
                                    {doc.title || t('untitled')}
                                </h3>
                                <div className="flex flex-wrap gap-x-3 gap-y-1 mt-1.5 text-xs text-slate-500">
                                    <span className="flex items-center gap-1">
                                        <MapPin className="w-3 h-3" />
                                        {doc.scout_profiles?.name || t('region')}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <Calendar className="w-3 h-3" />
                                        {doc.published_date || t('date')}
                                    </span>
                                    <span className="uppercase tracking-wider font-mono bg-slate-100 px-1.5 py-0.5 rounded-[4px] text-[10px] font-medium">
                                        {doc.doc_type}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <a
                            href={doc.url}
                            target="_blank"
                            rel="noreferrer"
                            className="p-1.5 hover:bg-slate-100 rounded-full transition-colors text-slate-400 hover:text-slate-900"
                        >
                            <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                    </div>
                </div>
            ))}
        </div>
    );
}
