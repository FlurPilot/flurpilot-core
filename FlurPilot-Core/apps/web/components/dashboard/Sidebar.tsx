"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { LayoutDashboard, Map as MapIcon, Settings, ShieldCheck, FileText, X } from 'lucide-react';

const navigationKeys = [
    { key: 'dashboard', href: '/dashboard', icon: LayoutDashboard },
    { key: 'map', href: '/dashboard/map', icon: MapIcon },
    { key: 'intelligence', href: '/dashboard/intelligence', icon: FileText },
    { key: 'trust', href: '/dashboard/trust', icon: ShieldCheck },
    { key: 'settings', href: '/dashboard/settings', icon: Settings },
];

interface SidebarProps {
    onClose?: () => void;
}

export function Sidebar({ onClose }: SidebarProps) {
    const pathname = usePathname();
    const t = useTranslations('nav');
    const ts = useTranslations('system');

    return (
        <div className="flex h-full w-64 flex-col border-r border-slate-200 bg-white text-slate-700">
            <div className="flex h-14 items-center px-5 justify-between border-b border-slate-100">
                <span className="text-lg font-extrabold tracking-tighter text-slate-900">
                    Flur<span className="text-emerald-600">Pilot</span>
                </span>
                {onClose && (
                    <button
                        onClick={onClose}
                        className="p-1 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors md:hidden"
                        aria-label={ts('closeMenu')}
                    >
                        <X size={18} />
                    </button>
                )}
            </div>

            <nav className="flex-1 space-y-0.5 px-3 py-3">
                {navigationKeys.map((item) => {
                    const isActive = pathname === item.href || pathname?.endsWith(item.href);
                    return (
                        <Link
                            key={item.key}
                            href={item.href}
                            aria-current={isActive ? 'page' : undefined}
                            onClick={onClose}
                            className={`
                                group flex items-center px-3 py-2 text-sm font-medium rounded-xl
                                transition-all duration-150 ease-out
                                ${isActive
                                    ? 'bg-emerald-50 text-emerald-700 shadow-sm'
                                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800 active:scale-[0.98]'
                                }
                            `}
                        >
                            <item.icon
                                className={`mr-3 h-[18px] w-[18px] flex-shrink-0 transition-colors duration-150 ${isActive
                                    ? 'text-emerald-600'
                                    : 'text-slate-400 group-hover:text-slate-500'
                                    }`}
                            />
                            {t(item.key)}
                        </Link>
                    );
                })}
            </nav>

            <div className="border-t border-slate-100 p-3 space-y-3">
                <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
                    <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{ts('title')}</p>
                    <div className="mt-1.5 flex items-center text-xs text-emerald-600 font-medium">
                        <span className="mr-2 h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        {ts('workerActive')}
                    </div>
                </div>

                <button
                    onClick={async () => {
                        const { createClient } = await import('@/lib/supabase');
                        const supabase = createClient();
                        await supabase.auth.signOut();
                        window.location.href = '/login';
                    }}
                    className="flex w-full items-center px-3 py-2 text-sm font-medium text-slate-400 rounded-xl hover:bg-slate-50 hover:text-slate-600 transition-all duration-150 active:scale-[0.98]"
                >
                    <svg className="mr-3 h-[18px] w-[18px] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    {t('signOut')}
                </button>
            </div>
        </div>
    );
}
