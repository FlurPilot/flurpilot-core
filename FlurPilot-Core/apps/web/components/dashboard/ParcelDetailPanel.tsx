"use client";

import { X, FileText, AlertTriangle, CheckCircle, Ruler, DraftingCompass, Layers, ExternalLink } from 'lucide-react';
import { useTranslations } from 'next-intl';
import { motion } from 'framer-motion';
import StickyNote from './StickyNote';

interface ParcelFeature {
    id: string;
    properties?: {
        type?: string;
        net_area_m2?: number;
        area_sqm?: number;
        source_id?: string;
        source?: string;
        alkis_id?: string;
        risk_score?: number;
        land_use?: string;
        owner_type?: string;
    };
}

interface ParcelDetailPanelProps {
    parcel: ParcelFeature;
    onClose: () => void;
}

const panelSpring = {
    type: "spring" as const,
    stiffness: 300,
    damping: 28,
    mass: 0.8,
};

const staggerChildren = {
    animate: {
        transition: {
            staggerChildren: 0.05,
        },
    },
};

const fadeUp = {
    initial: { opacity: 0, y: 8 },
    animate: { opacity: 1, y: 0 },
};

export function ParcelDetailPanel({ parcel, onClose }: ParcelDetailPanelProps) {
    const t = useTranslations('detail');
    const ts = useTranslations('system');
    if (!parcel) return null;

    const props = parcel.properties || {};
    const isVirtual = props.type === 'virtual';

    const area = props.net_area_m2 || props.area_sqm || 0;
    const titleID = isVirtual ? (props.source_id || props.source || 'Virtual ID') : (props.alkis_id || 'Unknown ID');
    const scoreLabel = isVirtual ? t('algorithmConfidence') : t('acquisitionScore');

    const riskScore = props.risk_score || (isVirtual ? 99 : 0);

    let riskColor = "text-emerald-600";
    let barColor = "bg-emerald-500";

    if (!isVirtual) {
        if (riskScore > 40) { riskColor = "text-amber-500"; barColor = "bg-amber-400"; }
        if (riskScore > 70) { riskColor = "text-red-600"; barColor = "bg-red-500"; }
    }

    return (
        <motion.div
            initial={{ x: 320, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 320, opacity: 0 }}
            transition={panelSpring}
            className="absolute top-3 right-3 bottom-3 z-50 w-80 bg-white border border-slate-200 rounded-2xl shadow-panel flex flex-col overflow-hidden text-slate-900"
        >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-slate-100 flex-shrink-0">
                <div className="min-w-0">
                    <h3 className="font-bold text-base text-slate-900 flex items-center gap-2 truncate">
                        {isVirtual && <DraftingCompass size={16} className="text-emerald-500 flex-shrink-0" />}
                        {isVirtual ? t('virtualAsset') : t('parcelIntelligence')}
                    </h3>
                    <p className="text-[11px] text-slate-400 font-mono truncate mt-0.5" title={titleID}>{titleID}</p>
                </div>
                <button
                    onClick={onClose}
                    className="p-1.5 hover:bg-slate-100 rounded-xl transition-colors flex-shrink-0"
                    aria-label={ts('closePanel')}
                >
                    <X className="w-4 h-4 text-slate-400" />
                </button>
            </div>

            {/* Content */}
            <motion.div
                className="flex-1 overflow-y-auto p-4 space-y-5"
                variants={staggerChildren}
                initial="initial"
                animate="animate"
            >
                {/* Score Card */}
                <motion.div variants={fadeUp} transition={{ duration: 0.2 }} className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-slate-400 font-medium">{scoreLabel}</span>
                        {isVirtual
                            ? <Layers className="w-4 h-4 text-emerald-500" />
                            : <AlertTriangle className="w-4 h-4 text-slate-400" />
                        }
                    </div>
                    <div className="flex items-end gap-1.5">
                        <span className={`text-3xl font-extrabold tracking-tight ${riskColor}`}>{riskScore}</span>
                        <span className="text-sm text-slate-400 mb-0.5">/100</span>
                    </div>
                    <div className="w-full bg-slate-200 h-1.5 mt-3 rounded-full overflow-hidden">
                        <motion.div
                            className={`h-full rounded-full ${barColor}`}
                            initial={{ width: 0 }}
                            animate={{ width: `${riskScore}%` }}
                            transition={{ delay: 0.3, duration: 0.6, ease: "easeOut" }}
                        />
                    </div>
                </motion.div>

                {/* Key Data */}
                <motion.div variants={fadeUp} transition={{ duration: 0.2 }} className="space-y-2">
                    <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{t('propertyData')}</h4>

                    <DataRow icon={<Ruler className="w-4 h-4 text-emerald-500" />} label={isVirtual ? t('netUsableArea') : t('totalArea')}>
                        {Math.round(area).toLocaleString()} m²
                    </DataRow>

                    <DataRow icon={<CheckCircle className="w-4 h-4 text-emerald-500" />} label={t('usage')}>
                        {props.land_use || (isVirtual ? t('calculatedArable') : t('owner'))}
                    </DataRow>

                    <DataRow icon={<FileText className="w-4 h-4 text-emerald-500" />} label={t('owner')}>
                        {props.owner_type || t('privateAssumed')}
                    </DataRow>

                    {/* Evidence Source */}
                    <button className="
                        flex items-center justify-between w-full p-3 bg-emerald-50 rounded-xl border border-emerald-100
                        hover:bg-emerald-100 transition-colors duration-150 group
                    ">
                        <div className="flex items-center gap-2">
                            <ExternalLink size={14} className="text-emerald-600" />
                            <span className="text-sm text-emerald-700 font-medium">{t('evidenceSource')}</span>
                        </div>
                        <span className="text-xs text-emerald-500 group-hover:underline">
                            {isVirtual ? t('calculationLog') : t('risProtocol')}
                        </span>
                    </button>
                </motion.div>

                {/* Secure Notes */}
                <motion.div variants={fadeUp} transition={{ duration: 0.2 }} className="space-y-2">
                    <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Secure Notes</h4>
                    <StickyNote parcelId={parcel.id} />
                </motion.div>

                {/* Actions */}
                <motion.div variants={fadeUp} transition={{ duration: 0.2 }} className="pt-2">
                    <button className="
                        w-full py-2.5 bg-slate-900 hover:bg-slate-800
                        text-white rounded-xl font-semibold text-sm
                        transition-all duration-150 shadow-md
                        active:scale-[0.98]
                    ">
                        {isVirtual ? t('exportShapefile') : t('generateReport')}
                    </button>
                </motion.div>
            </motion.div>
        </motion.div>
    );
}

function DataRow({ icon, label, children }: { icon: React.ReactNode; label: string; children: React.ReactNode }) {
    return (
        <div className="flex items-center justify-between p-3 bg-white rounded-xl border border-slate-100 shadow-card">
            <div className="flex items-center gap-2 min-w-0">
                {icon}
                <span className="text-sm text-slate-500">{label}</span>
            </div>
            <span className="font-mono text-sm font-semibold text-slate-800 truncate ml-2">{children}</span>
        </div>
    );
}
