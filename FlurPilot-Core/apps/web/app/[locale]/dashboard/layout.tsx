"use client";

import { useState } from 'react';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { useTranslations } from 'next-intl';
import { Menu, X, Bell } from 'lucide-react';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const t = useTranslations('system');

    return (
        <div className="flex h-screen bg-slate-50 text-slate-900 overflow-hidden font-sans">

            {/* Mobile Sidebar Overlay */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 z-40 bg-slate-900/30 backdrop-blur-sm md:hidden"
                    onClick={() => setSidebarOpen(false)}
                />
            )}

            {/* Sidebar — hidden on mobile, visible on md+ */}
            <div className={`
                fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-200 ease-out
                md:relative md:translate-x-0 md:z-auto
                ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
            `}>
                <Sidebar onClose={() => setSidebarOpen(false)} />
            </div>

            <main className="flex-1 relative overflow-hidden flex flex-col min-w-0">
                {/* Header */}
                <header className="flex h-14 items-center border-b border-slate-200 bg-white px-4 md:px-6 justify-between shadow-sm flex-shrink-0">
                    <div className="flex items-center gap-3">
                        {/* Mobile hamburger */}
                        <button
                            onClick={() => setSidebarOpen(true)}
                            className="p-1.5 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700 transition-colors md:hidden"
                            aria-label={t('openMenu')}
                        >
                            <Menu size={20} />
                        </button>
                        <h1 className="text-sm font-bold text-slate-800 tracking-tight">{t('operationsCenter')}</h1>
                    </div>
                    <div className="flex items-center gap-3">
                        <button className="relative p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors">
                            <Bell size={18} />
                            <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-emerald-500 rounded-full" />
                        </button>
                        <div className="h-8 w-8 rounded-full bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-sm flex items-center justify-center text-white text-xs font-bold">
                            FP
                        </div>
                    </div>
                </header>

                {/* Content */}
                <div className="flex-1 overflow-auto bg-slate-50">
                    {children}
                </div>
            </main>
        </div>
    );
}
