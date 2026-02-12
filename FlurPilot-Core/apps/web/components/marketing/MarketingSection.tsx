import { ReactNode } from 'react';

interface SectionProps {
    children: ReactNode;
    className?: string;
    id?: string;
    dark?: boolean;
}

export function MarketingSection({ children, className = "", id = "", dark = false }: SectionProps) {
    return (
        <section
            id={id}
            className={`py-20 px-4 md:px-8 ${dark ? 'bg-slate-900 text-white' : ''} ${className}`}
        >
            <div className="max-w-6xl mx-auto">
                {children}
            </div>
        </section>
    );
}
