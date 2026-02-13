"use client";

import { useChat } from '@ai-sdk/react';
import { Send, Bot, User, Sparkles, StopCircle } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { useTranslations } from 'next-intl';

interface ChatMessage {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
}

interface ChatHook {
    messages: ChatMessage[];
    append: (msg: { role: string; content: string }) => Promise<void>;
    isLoading: boolean;
    stop: () => void;
}

export default function AnalystConsole() {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const chat = useChat() as unknown as ChatHook;
    const { messages, append, isLoading, stop } = chat;

    // Manual input state management since useChat helpers might be missing in this version
    const [input, setInput] = useState('');
    const t = useTranslations('intelligence');
    const scrollRef = useRef<HTMLDivElement>(null);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input;
        setInput(''); // Clear immediately

        await append({
            role: 'user',
            content: userMessage,
        });
    };

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="flex flex-col h-full bg-slate-900 text-slate-200 rounded-xl overflow-hidden border border-slate-700 font-mono shadow-2xl">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-slate-800 border-b border-slate-700">
                <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-emerald-400" />
                    <span className="text-sm font-bold tracking-wider uppercase text-emerald-400">{t('consoleTitle')}</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-amber-400 animate-pulse' : 'bg-emerald-500'}`} />
                    <span className="text-xs text-slate-400">{isLoading ? t('processing') : t('ready')}</span>
                </div>
            </div>

            {/* Output / Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth" ref={scrollRef}>
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-slate-600 opacity-50">
                        <Bot size={48} className="mb-4" />
                        <p className="text-sm">{t('initialized')}</p>
                        <p className="text-xs mt-1">{t('readyForQueries')}</p>
                    </div>
                )}

                {messages.map((m: ChatMessage) => (
                    <div key={m.id} className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {m.role === 'assistant' && (
                            <div className="w-8 h-8 rounded-lg bg-emerald-900/30 border border-emerald-500/20 flex items-center justify-center flex-shrink-0">
                                <Bot size={16} className="text-emerald-400" />
                            </div>
                        )}

                        <div className={`
                            max-w-[80%] rounded-lg p-3 text-sm
                            ${m.role === 'user'
                                ? 'bg-slate-800 border border-slate-700 text-slate-200'
                                : 'bg-transparent text-emerald-50/90 leading-relaxed'
                            }
                        `}>
                            {m.content}
                        </div>

                        {m.role === 'user' && (
                            <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center flex-shrink-0">
                                <User size={16} className="text-slate-400" />
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Input Area */}
            <form onSubmit={handleSubmit} className="p-3 bg-slate-800 border-t border-slate-700 flex gap-2">
                <input
                    value={input}
                    onChange={handleInputChange}
                    placeholder={t('inputPlaceholder')}
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors placeholder-slate-600"
                    disabled={isLoading}
                />

                {isLoading ? (
                    <button
                        type="button"
                        onClick={() => stop()}
                        className="p-2.5 bg-red-500/10 text-red-400 border border-red-500/50 rounded-lg hover:bg-red-500/20 transition-colors"
                        title={t('stop')}
                    >
                        <StopCircle size={18} />
                    </button>
                ) : (
                    <button
                        type="submit"
                        disabled={!input.trim()}
                        className="
                            p-2.5 bg-emerald-600 text-white rounded-lg
                            hover:bg-emerald-500 transition-colors
                            disabled:opacity-50 disabled:cursor-not-allowed
                        "
                    >
                        <Send size={18} />
                    </button>
                )}
            </form>
        </div>
    );
}
