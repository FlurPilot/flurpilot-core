"use client";

import { useState, useEffect } from 'react';
import { Search, Loader2, MapPin, Globe, AlertTriangle } from 'lucide-react';
import { useTranslations } from 'next-intl';

interface GeoJSONFeature {
    type: 'Feature';
    geometry: unknown;
    properties: Record<string, unknown>;
}

interface SearchResult {
    id: string;
    type: 'city' | 'parcel';
    name?: string;
    alkis_id?: string;
    geom?: unknown;
    properties?: Record<string, unknown>;
    area_sqm?: number;
}

interface SearchBarProps {
    onSearchResult: (feature: GeoJSONFeature) => void;
}

export function SearchBar({ onSearchResult }: SearchBarProps) {
    const t = useTranslations('search');
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const timer = setTimeout(async () => {
            if (query.length < 2) {
                setResults([]);
                setOpen(false);
                setError(null);
                return;
            }

            setLoading(true);
            setError(null);

            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

                if (res.status === 429) {
                    setError('Zu viele Anfragen. Bitte warten.');
                    setLoading(false);
                    setOpen(true);
                    return;
                }

                if (!res.ok) throw new Error('Search failed');

                const data = await res.json();

                if (Array.isArray(data) && data.length > 0) {
                    setResults(data);
                    setOpen(true);
                } else {
                    setResults([]);
                    setOpen(false);
                }
            } catch (e) {
                console.error("Search error:", e);
                setResults([]);
                // Silent fail or show simple error?
                // setError('Fehler bei der Suche');
            } finally {
                setLoading(false);
            }
        }, 300);

        return () => clearTimeout(timer);
    }, [query]);

    const handleSelect = async (item: SearchResult) => {
        setLoading(true);
        try {
            if (item.type === 'city' && item.name) {
                // Fetch representative parcel for the city to get location
                const res = await fetch(`/api/search?lookup_city=${encodeURIComponent(item.name)}`);
                if (res.ok) {
                    const target = await res.json() as SearchResult;
                    if (target && target.geom) {
                        const feature: GeoJSONFeature = {
                            type: 'Feature',
                            geometry: target.geom,
                            properties: {
                                id: target.id,
                                alkis_id: target.alkis_id,
                                ...target.properties
                            }
                        };
                        onSearchResult(feature);
                        setQuery(item.name);
                    }
                }
                setOpen(false);
            } else {
                // Direct parcel selection
                const feature: GeoJSONFeature = {
                    type: 'Feature',
                    geometry: item.geom,
                    properties: {
                        id: item.id,
                        alkis_id: item.alkis_id,
                        ...item.properties
                    }
                };
                onSearchResult(feature);
                setQuery(item.alkis_id || '');
                setOpen(false);
            }
        } catch (err) {
            console.error("Selection error:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="relative w-full max-w-sm">
            <div className="relative">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                    type="text"
                    placeholder={t('placeholder')}
                    className="
                        h-10 w-full rounded-xl border border-slate-200 bg-white/90 backdrop-blur-sm
                        pl-10 pr-4 text-sm text-slate-800 placeholder-slate-400
                        shadow-card
                        focus:border-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20
                        transition-all duration-150
                    "
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onFocus={() => { if (results.length > 0 || error) setOpen(true); }}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && results.length > 0) {
                            handleSelect(results[0]);
                        }
                    }}
                />
                {loading && (
                    <Loader2 className="absolute right-3.5 top-1/2 -translate-y-1/2 h-4 w-4 animate-spin text-emerald-500" />
                )}
            </div>

            {open && (results.length > 0 || error) && (
                <div className="absolute mt-2 w-full rounded-xl border border-slate-200 bg-white shadow-panel py-1 z-50 overflow-hidden">
                    {error && (
                        <div className="px-4 py-3 text-xs text-amber-600 bg-amber-50 flex items-center gap-2">
                            <AlertTriangle size={12} />
                            {error}
                        </div>
                    )}

                    {results.map((result) => (
                        <button
                            key={result.id}
                            className="
                                flex w-full items-center gap-3 px-4 py-2.5 text-left text-sm
                                text-slate-600 hover:bg-emerald-50 hover:text-slate-800
                                transition-colors duration-100
                            "
                            onClick={() => handleSelect(result)}
                        >
                            {/* Icon Logic including Honeytoken visualization? No, keep it hidden */}
                            {result.type === 'city'
                                ? <Globe size={14} className="text-emerald-500 flex-shrink-0" />
                                : <MapPin size={14} className="text-slate-400 flex-shrink-0" />
                            }
                            <div className="min-w-0">
                                <span className="font-medium text-slate-800 block truncate">
                                    {result.type === 'city' ? result.name : result.alkis_id}
                                </span>
                                {result.type === 'parcel' && (
                                    <span className="text-xs text-slate-400 block truncate">
                                        {result.properties?.land_use || t('unknown')} • {Math.round(result.area_sqm || 0)} m²
                                    </span>
                                )}
                            </div>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
