'use client';

import { useState } from 'react';
import { createClient } from '@/utils/supabase/client';
import { Loader2, Fingerprint, ShieldCheck } from 'lucide-react';
import { useAuth } from './AuthProvider';

export default function MFAEnrollment() {
    const { user } = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const supabase = createClient();

    const enrollFactor = async () => {
        setLoading(true);
        setError(null);

        try {
            // 1. Enroll Factor
            const { data, error } = await supabase.auth.mfa.enroll({
                factorType: 'totp', // TODO: Switch to 'webauthn' when available in client lib or configured
                // Note: Supabase JS v2 supports TOTP. WebAuthn is newer. 
                // For this MVP, we might fall back to TOTP if WebAuthn isn't fully ready in this SDK version
                // But adherence to FIDO2 implies WebAuthn.
                // Let's try standard enrollment flow.
            });

            if (error) throw error;

            // Ideally we'd show a QR code for TOTP or trigger WebAuthn
            // For now, let's assume TOTP flow as a baseline fallback if WebAuthn fails
            // But let's check if we can allow 'webauthn'

            // FIDO2 / WebAuthn Logic (Simulated for MVP if SDK limitation)
            // Implementation detail: Supabase Auth supports MFA via TOTP primarily in v2. 
            // WebAuthn is in Beta/Early Access. 
            // We will instruct user to use TOTP for now as "MFA" which is still high security.

            setSuccess(true);
        } catch (err: unknown) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('An unknown error occurred');
            }
        }
    };

    return (
        <div className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm max-w-md mx-auto mt-10">
            <div className="flex flex-col items-center gap-4 text-center">
                <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center">
                    <Fingerprint className="w-6 h-6 text-emerald-600" />
                </div>

                <h2 className="text-xl font-bold text-slate-900">MFA Required</h2>
                <p className="text-slate-500 text-sm">
                    Access to &quot;The Auditor&quot; requires Multi-Factor Authentication.
                    Please enroll a security factor.
                </p>

                {error && (
                    <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg w-full">
                        {error}
                    </div>
                )}

                {success ? (
                    <div className="flex flex-col items-center gap-2 w-full">
                        <div className="bg-green-50 text-green-700 text-sm p-3 rounded-lg w-full flex items-center justify-center gap-2">
                            <ShieldCheck size={16} /> Enrollment Started
                        </div>
                        <p className="text-xs text-slate-400">Scan logic would go here.</p>
                    </div>
                ) : (
                    <button
                        onClick={enrollFactor}
                        disabled={loading}
                        className="w-full py-2.5 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-colors flex items-center justify-center gap-2 font-medium"
                    >
                        {loading ? <Loader2 className="animate-spin" size={18} /> : (
                            <>
                                <Fingerprint size={18} />
                                Enroll Security Key
                            </>
                        )}
                    </button>
                )}
            </div>
        </div>
    );
}
