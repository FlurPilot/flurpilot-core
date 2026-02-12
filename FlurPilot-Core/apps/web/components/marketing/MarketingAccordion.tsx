'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

interface AccordionItemProps {
    question: string;
    answer: string;
    defaultOpen?: boolean;
}

export function MarketingAccordion({ question, answer, defaultOpen = false }: AccordionItemProps) {
    const [isOpen, setIsOpen] = useState(defaultOpen);

    return (
        <div className="border-b border-slate-200 last:border-0">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex justify-between items-center w-full py-6 text-left group hover:bg-slate-50 transition-colors px-4 -mx-4"
            >
                <span className="text-slate-900 font-bold pr-4 font-mono text-sm uppercase tracking-wide">{question}</span>
                <motion.div animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.2 }}>
                    <ChevronDown className="w-5 h-5 text-slate-400 flex-shrink-0" />
                </motion.div>
            </button>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.25 }}
                        className="overflow-hidden"
                    >
                        <p className="pb-6 text-slate-600 text-sm leading-relaxed max-w-2xl">{answer}</p>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
