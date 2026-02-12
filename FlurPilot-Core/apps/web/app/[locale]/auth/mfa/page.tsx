'use client';

import MFAEnrollment from '@/components/auth/MFAEnrollment';

export default function MFAPage() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50 p-4">
            <MFAEnrollment />
        </div>
    );
}
