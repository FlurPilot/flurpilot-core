"use client";

import { useState } from 'react';
import ParcelsMap from '@/components/dashboard/ParcelsMap';
import { ParcelDetailPanel } from '@/components/dashboard/ParcelDetailPanel';
import { SearchBar } from '@/components/dashboard/SearchBar';
import ParcelFeed from '@/components/dashboard/ParcelFeed';
import { AnimatePresence } from 'framer-motion';

interface ParcelFeature {
    id: string;
    geometry?: {
        type: string;
        coordinates: unknown;
    };
    properties?: Record<string, unknown>;
}

export default function DashboardPage() {
    const [selectedParcel, setSelectedParcel] = useState<ParcelFeature | null>(null);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleParcelSelect = (feature: any) => {
        console.log("Parcel Selected:", feature);
        const parcelFeature: ParcelFeature = {
            id: String(feature.properties?.id || feature.id || ''),
            geometry: feature.geometry,
            properties: feature.properties
        };
        setSelectedParcel(parcelFeature);
    };

    return (
        <div className="h-full w-full flex flex-col md:flex-row overflow-hidden">
            {/* LEFT PANEL: The Feed (Mobile: Bottom Sheet / Desktop: Left Sidebar) */}
            <div className="w-full h-[40%] md:w-[350px] md:h-full z-20 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] md:shadow-xl flex-shrink-0 relative order-2 md:order-1 border-t md:border-t-0 md:border-r border-slate-200">
                <ParcelFeed onSelect={handleParcelSelect} />

                {/* Mobile Overlay Toggle? (Later) */}
            </div>

            {/* RIGHT PANEL: The Map (Mobile: Top / Desktop: Right) */}
            <div className="flex-1 h-[60%] md:h-full relative z-10 order-1 md:order-2">
                {/* Search Bar Overlay - Moved inside Map Area */}
                <div className="absolute top-4 left-4 right-4 z-30 pointer-events-none flex justify-center">
                    <div className="pointer-events-auto w-full max-w-md">
                        <SearchBar onSearchResult={handleParcelSelect} />
                    </div>
                </div>

                <ParcelsMap
                    onParcelSelect={handleParcelSelect}
                    focusedParcel={selectedParcel as unknown as { geometry: { type: string; coordinates: number[] } }}
                />

                <AnimatePresence>
                    {selectedParcel && (
                        <div className="absolute inset-0 z-40 pointer-events-none">
                            {/* Panel is self-positioning absolute right */}
                            <div className="pointer-events-auto h-full w-full">
                                <ParcelDetailPanel
                                    parcel={selectedParcel}
                                    onClose={() => setSelectedParcel(null)}
                                />
                            </div>
                        </div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
