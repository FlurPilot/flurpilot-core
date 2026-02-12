import TransparencyReport from '@/components/trust/TransparencyReport';
import { useTranslations } from 'next-intl';

export default function TrustPage() {
    const t = useTranslations('trust');

    return (
        <div className="h-[calc(100vh-64px)] p-6 bg-slate-50 overflow-y-auto">
            <header className="mb-6">
                <h1 className="text-xl font-bold text-slate-900 tracking-tight">{t('title')}</h1>
                <p className="text-sm text-slate-500">{t('subtitle')}</p>
            </header>

            <TransparencyReport />
        </div>
    );
}
