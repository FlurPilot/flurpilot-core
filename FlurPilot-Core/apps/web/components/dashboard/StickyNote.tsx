"use client";

import React, { useState, useEffect } from 'react';
import { Lock, Unlock, Save, AlertTriangle, ShieldCheck } from 'lucide-react';
import * as CryptoLib from '@/lib/crypto';
import { createClient } from '@/utils/supabase/client';
import { useTranslations } from 'next-intl';

interface StickyNoteProps {
    parcelId: string;
    initialData?: CryptoLib.EncryptedNotePacket;
    onSave?: (data: CryptoLib.EncryptedNotePacket) => void;
}

export default function StickyNote({ parcelId, initialData, onSave }: StickyNoteProps) {
    const t = useTranslations('note');

    const [isLocked, setIsLocked] = useState<boolean>(true);
    const [password, setPassword] = useState<string>("");
    const [noteText, setNoteText] = useState<string>("");
    const [status, setStatus] = useState<"idle" | "saving" | "error" | "decrypted">("idle");
    const [encryptedData, setEncryptedData] = useState<CryptoLib.EncryptedNotePacket | undefined>(initialData);

    useEffect(() => {
        const cachedPwd = sessionStorage.getItem(`flurpilot_key_${parcelId}`);
        if (cachedPwd) setPassword(cachedPwd);

        const fetchNote = async () => {
            const supabase = createClient();
            const { data } = await supabase
                .from('sticky_notes')
                .select('encrypted_blob')
                .eq('parcel_id', parcelId)
                .single();

            if (data?.encrypted_blob) {
                setEncryptedData(data.encrypted_blob as CryptoLib.EncryptedNotePacket);
                if (cachedPwd) {
                    try {
                        const text = await CryptoLib.decryptNotePacket(data.encrypted_blob as CryptoLib.EncryptedNotePacket, cachedPwd);
                        setNoteText(text);
                        setIsLocked(false);
                        setStatus("decrypted");
                    } catch {
                        // Cached password failed
                    }
                }
            } else if (cachedPwd) {
                setIsLocked(false);
                setStatus("decrypted");
            }
        };

        if (parcelId) fetchNote();
    }, [parcelId]);

    const handleUnlock = async () => {
        if (!encryptedData) {
            setIsLocked(false);
            setStatus("decrypted");
            return;
        }

        try {
            const text = await CryptoLib.decryptNotePacket(encryptedData, password);
            setNoteText(text);
            setIsLocked(false);
            setStatus("decrypted");
            sessionStorage.setItem(`flurpilot_key_${parcelId}`, password);
        } catch {
            setStatus("error");
        }
    };

    const handleSave = async () => {
        if (!password) return;

        setStatus("saving");
        try {
            const noteKey = await CryptoLib.generateNoteKey();
            const { ciphertext, iv } = await CryptoLib.encryptNoteText(noteText, noteKey);
            const saltRaw = CryptoLib.generateSalt();
            const saltBuf = Uint8Array.from(atob(saltRaw), c => c.charCodeAt(0));
            const userKey = await CryptoLib.deriveKeyFromPassword(password, saltBuf);
            const wrappedKeyUser = await CryptoLib.wrapNoteKey(noteKey, userKey);

            const packet: CryptoLib.EncryptedNotePacket = {
                ciphertext, iv, wrappedKeyUser, salt: saltRaw,
            };

            const supabase = createClient();
            const { data: { user } } = await supabase.auth.getUser();
            if (!user) throw new Error("Not authenticated");

            const { data: existing } = await supabase
                .from('sticky_notes')
                .select('id')
                .eq('parcel_id', parcelId)
                .single();

            let error;
            if (existing) {
                const res = await supabase
                    .from('sticky_notes')
                    .update({ encrypted_blob: packet, updated_at: new Date().toISOString() })
                    .eq('id', existing.id);
                error = res.error;
            } else {
                const res = await supabase
                    .from('sticky_notes')
                    .insert({ parcel_id: parcelId, encrypted_blob: packet, user_id: user.id });
                error = res.error;
            }

            if (error) throw error;

            setEncryptedData(packet);
            if (onSave) onSave(packet);
            sessionStorage.setItem(`flurpilot_key_${parcelId}`, password);
            setStatus("decrypted");
        } catch (e) {
            console.error(e);
            setStatus("error");
        }
    };

    return (
        <div className="bg-amber-50 p-3.5 rounded-xl border border-amber-100 shadow-card">
            {/* Header */}
            <div className="flex justify-between items-center mb-2.5">
                <h3 className="font-bold text-sm text-amber-800 flex items-center gap-1.5">
                    <ShieldCheck size={14} className="text-amber-500" />
                    {t('title')}
                    {isLocked
                        ? <Lock size={12} className="text-amber-400" />
                        : <Unlock size={12} className="text-emerald-500" />
                    }
                </h3>
                {status === "error" && <AlertTriangle size={14} className="text-red-500" />}
            </div>

            {isLocked ? (
                <div className="space-y-2">
                    <p className="text-[11px] text-amber-600">{t('encryptedHint')}</p>
                    <input
                        type="password"
                        className="
                            w-full p-2 text-sm border border-amber-200 rounded-lg bg-white
                            placeholder-amber-300 text-slate-800
                            focus:border-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-400/20
                            transition-all duration-150
                        "
                        placeholder={t('decryptionPassword')}
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        onKeyDown={e => { if (e.key === 'Enter') handleUnlock(); }}
                    />
                    <button
                        onClick={handleUnlock}
                        className="
                            w-full bg-amber-500 text-white text-sm py-2 rounded-lg font-medium
                            hover:bg-amber-600 transition-colors duration-150
                            active:scale-[0.98]
                        "
                    >
                        {t('unlock')}
                    </button>
                    {!encryptedData && (
                        <button
                            onClick={() => { setIsLocked(false); setStatus("decrypted"); }}
                            className="w-full text-[11px] text-amber-500 hover:text-amber-600 transition-colors"
                        >
                            {t('createNew')}
                        </button>
                    )}
                </div>
            ) : (
                <div className="space-y-2">
                    <textarea
                        className="
                            w-full h-28 p-2.5 text-sm bg-white rounded-lg border border-amber-100
                            focus:ring-2 focus:ring-amber-400/20 focus:border-amber-300 focus:outline-none
                            resize-none text-slate-700 placeholder-slate-300
                            transition-all duration-150
                        "
                        value={noteText}
                        onChange={e => setNoteText(e.target.value)}
                        placeholder={t('writePlaceholder')}
                    />

                    <div className="flex gap-2">
                        <input
                            type="password"
                            className="
                                flex-1 p-1.5 text-xs border border-amber-200 rounded-lg bg-white
                                focus:border-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-400/20
                                transition-all duration-150
                            "
                            placeholder={t('passwordToLock')}
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />
                        <button
                            onClick={handleSave}
                            disabled={status === "saving"}
                            className="
                                bg-amber-600 text-white p-2 rounded-lg
                                hover:bg-amber-700 transition-colors duration-150
                                disabled:opacity-50
                                active:scale-[0.95]
                            "
                            title="Encrypt & Save"
                        >
                            <Save size={14} />
                        </button>
                    </div>
                    <p className="text-[10px] text-amber-400 leading-relaxed">
                        {t('zeroKnowledge')}
                    </p>
                </div>
            )}
        </div>
    );
}
