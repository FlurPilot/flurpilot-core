'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User, Session } from '@supabase/supabase-js';
import { createClient } from '@/utils/supabase/client';
import { useRouter } from 'next/navigation';

interface AuthContextType {
    user: User | null;
    session: Session | null;
    loading: boolean;
    isAdmin: boolean;
    isMFAVerified: boolean;
    signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
    user: null,
    session: null,
    loading: true,
    isAdmin: false,
    isMFAVerified: false,
    signOut: async () => { },
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState(true);
    const [isAdmin, setIsAdmin] = useState(false);
    const [isMFAVerified, setIsMFAVerified] = useState(false);

    const supabase = createClient();
    const router = useRouter();

    useEffect(() => {
        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            async (event, session) => {
                setSession(session);
                setUser(session?.user ?? null);

                if (session?.user) {
                    // Check Role
                    // Heuristic: Check user metadata or specific DB table
                    // For now, assume 'admin' if email contains specific domain or claim
                    // Or check jwt claims if custom claims set up
                    // For prototype: Check app_metadata
                    const role = session.user.app_metadata.role || 'user';
                    setIsAdmin(role === 'admin' || role === 'service_role');

                    // Check MFA
                    const aal = session.user.app_metadata.aal;
                    setIsMFAVerified(aal === 'aal2');
                } else {
                    setIsAdmin(false);
                    setIsMFAVerified(false);
                }

                setLoading(false);
            }
        );

        return () => {
            subscription.unsubscribe();
        };
    }, []);

    const signOut = async () => {
        await supabase.auth.signOut();
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ user, session, loading, isAdmin, isMFAVerified, signOut }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
