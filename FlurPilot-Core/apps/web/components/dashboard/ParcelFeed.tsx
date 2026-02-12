"use client";

import React, { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase';
import { MapPin, Clock, AlertTriangle, FileText, ChevronRight, DraftingCompass } from 'lucide-react';
import { useTranslations } from 'next-intl';
import { motion, AnimatePresence } from 'framer-motion';

interface GeoJSONFeature {
    type: 'Feature';
    geometry: unknown;
    properties: Record<string, unknown>;
}

interface FeedItem {
    id: string;
    type: 'real' | 'virtual';
    municipality: string;
    address: string;
    score: number;
    timestamp: string;
    raw_timestamp: string;
    status: "new" | "viewed" | "actioned";
    feature: GeoJSONFeature;
}

interface ParcelFeedProps {
    onSelect: (feature: GeoJSONFeature) => void;
}

function FeedSkeleton() {
    return (
        <div className="space-y-2 p-2">
            {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white p-3 rounded-xl border border-slate-100">
                    <div className="flex justify-between items-start mb-2">
                        <div className="skeleton h-4 w-32 rounded" />
                        <div className="skeleton h-3 w-12 rounded" />
                    </div>
                    <div className="skeleton h-3 w-48 rounded mb-3" />
                    <div className="flex justify-between">
                        <div className="skeleton h-6 w-20 rounded" />
                        <div className="skeleton h-4 w-4 rounded" />
                    </div>
                </div>
            ))}
        </div>
    );
}

const springTransition = {
    type: "spring" as const,
    stiffness: 400,
    damping: 30,
    mass: 0.8,
};

export default function ParcelFeed({ onSelect }: ParcelFeedProps) {
    const t = useTranslations('feed');
    const [items, setItems] = useState<FeedItem[]>([]);
    const [loading, setLoading] = useState(true);
    const supabase = createClient();

    const fetchItems = async () => {
        setLoading(true);
        try {
            const { data: realData } = await supabase
                .from('geo_parcels')
                .select('id, alkis_id, municipality, address, risk_score, created_at, geom, properties')
                .order('created_at', { ascending: false })
                .limit(25);

            const { data: virtualData } = await supabase
                .from('virtual_parcels')
                .select('id, source_field_id, last_calculated_at, net_area_m2, geometry')
                .order('last_calculated_at', { ascending: false })
                .limit(25);

            interface RealParcelData {
                id: string;
                municipality?: string;
                address?: string;
                alkis_id: string;
                risk_score?: number;
                created_at: string;
                geom: unknown;
                properties?: Record<string, unknown>;
            }

            interface VirtualParcelData {
                id: string;
                source_field_id: string;
                last_calculated_at: string;
                net_area_m2: number;
                geometry: unknown;
            }

            const mappedReal: FeedItem[] = (realData || []).map((p: RealParcelData) => ({
                id: p.id,
                type: 'real',
                municipality: p.municipality || t('unknownMunicipality'),
                address: p.address || p.alkis_id || t('noAddress'),
                score: p.risk_score || 0,
                timestamp: new Date(p.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                raw_timestamp: p.created_at,
                status: 'new',
                feature: {
                    type: 'Feature',
                    geometry: p.geom,
                    properties: { ...p.properties, id: p.id, risk_score: p.risk_score, type: 'real' }
                }
            }));

            const mappedVirtual: FeedItem[] = (virtualData || []).map((p: VirtualParcelData) => ({
                id: p.id,
                type: 'virtual',
                municipality: t('virtualParcel'),
                address: `Field: ${p.source_field_id?.substring(0, 15)}...`,
                score: 99,
                timestamp: new Date(p.last_calculated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                raw_timestamp: p.last_calculated_at,
                status: 'new',
                feature: {
                    type: 'Feature',
                    geometry: p.geometry,
                    properties: {
                        id: p.id,
                        type: 'virtual',
                        source_id: p.source_field_id,
                        area_sqm: p.net_area_m2
                    }
                }
            }));

            const combined = [...mappedReal, ...mappedVirtual].sort((a, b) =>
                new Date(b.raw_timestamp).getTime() - new Date(a.raw_timestamp).getTime()
            );

            setItems(combined);
        } catch (e) {
            console.error("Feed fetch error:", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchItems();

        const channel = supabase.channel('feed-updates')
            .on(
                'postgres_changes',
                { event: 'INSERT', schema: 'public', table: 'geo_parcels' },
                () => fetchItems()
            )
            .on(
                'postgres_changes',
                { event: 'INSERT', schema: 'public', table: 'virtual_parcels' },
                () => fetchItems()
            )
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const getScoreColor = (item: FeedItem) => {
        if (item.type === 'virtual') return "text-emerald-700 bg-emerald-50 border-emerald-200";
        if (item.score > 80) return "text-emerald-600 bg-emerald-50 border-emerald-200";
        if (item.score > 50) return "text-amber-600 bg-amber-50 border-amber-200";
        return "text-slate-500 bg-slate-50 border-slate-200";
    };

    return (
        <div className="flex flex-col h-full bg-white w-full">
            {/* Header */}
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-white sticky top-0 z-10 flex-shrink-0">
                <div>
                    <h2 className="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-2">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                        </span>
                        {t('title')}
                    </h2>
                    <p className="text-[11px] text-slate-400 mt-0.5">{t('subtitle')}</p>
                </div>
                <div className="bg-slate-50 px-2 py-1 rounded-lg text-xs font-mono text-slate-500 border border-slate-100">
                    {items.length}
                </div>
            </div>

            {/* Feed List */}
            <div className="flex-1 overflow-y-auto p-2 space-y-1.5 bg-slate-50/50">
                {loading ? (
                    <FeedSkeleton />
                ) : (
                    <AnimatePresence initial={false}>
                        {items.map((item, index) => (
                            <motion.div
                                key={`${item.type}-${item.id}`}
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                transition={{
                                    ...springTransition,
                                    delay: index * 0.03,
                                }}
                                onClick={() => onSelect(item.feature)}
                                className={`
                                    group bg-white p-3 rounded-xl border border-slate-100
                                    hover:border-emerald-200 hover:shadow-card-hover
                                    hover:-translate-y-[1px]
                                    transition-all duration-150 ease-out
                                    cursor-pointer relative overflow-hidden
                                    active:scale-[0.98]
                                    ${item.type === 'virtual' ? 'border-l-[3px] border-l-emerald-400' : ''}
                                `}
                            >
                                <div className="flex justify-between items-start mb-1.5">
                                    <h3 className="font-semibold text-slate-800 text-sm truncate flex-1 pr-4 flex items-center gap-1.5">
                                        {item.type === 'virtual' && <DraftingCompass size={13} className="text-emerald-500 flex-shrink-0" />}
                                        {item.municipality}
                                    </h3>
                                    <span className="text-[10px] text-slate-400 font-mono flex items-center gap-1 flex-shrink-0">
                                        <Clock size={10} /> {item.timestamp}
                                    </span>
                                </div>

                                <div className="flex items-center gap-1 text-xs text-slate-400 mb-2.5">
                                    {item.type === 'virtual'
                                        ? <FileText size={11} className="text-slate-300" />
                                        : <MapPin size={11} className="text-slate-300" />
                                    }
                                    <span className="truncate">{item.address}</span>
                                </div>

                                <div className="flex justify-between items-end">
                                    <div className={`px-2 py-0.5 rounded-lg text-[11px] font-bold border ${getScoreColor(item)} flex items-center gap-1`}>
                                        <AlertTriangle size={10} />
                                        {item.type === 'virtual' ? t('automated') : t('score', { value: item.score })}
                                    </div>

                                    <ChevronRight
                                        size={14}
                                        className="text-slate-300 group-hover:text-emerald-500 group-hover:translate-x-0.5 transition-all duration-150"
                                    />
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                )}

                {/* Connection Status */}
                <div className="p-3 text-center">
                    <div className="inline-flex gap-1.5 items-center bg-white rounded-full px-3 py-1.5 text-[11px] text-slate-400 border border-slate-100 shadow-sm">
                        <span className={`w-1.5 h-1.5 rounded-full ${loading ? 'bg-amber-400 animate-pulse' : 'bg-emerald-400'}`} />
                        {loading ? t('refreshing') : t('live')}
                    </div>
                </div>
            </div>
        </div>
    );
}
