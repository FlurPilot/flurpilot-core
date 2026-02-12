import { ReactNode } from 'react';

interface BadgeProps {
    children: ReactNode;
    variant?: "emerald" | "orange" | "slate";
}

export function MarketingBadge({ children, variant = "emerald" }: BadgeProps) {
    const variants = {
        emerald: "bg-emerald-50 text-emerald-700 border-emerald-200",
        orange: "bg-orange-50 text-orange-700 border-orange-200",
        slate: "bg-slate-100 text-slate-600 border-slate-200",
    };

    return (
        <span className={`inline-flex items-center px-2 py-1 border text-[10px] font-bold uppercase tracking-widest font-mono ${variants[variant]}`}>
            {children}
        </span>
    );
}
