import { createBrowserClient } from '@supabase/ssr'

export const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
export const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export function createClient() {
    if (!supabaseUrl) console.error("FATAL: NEXT_PUBLIC_SUPABASE_URL is missing!");
    if (!supabaseAnonKey) console.error("FATAL: NEXT_PUBLIC_SUPABASE_ANON_KEY is missing!");

    return createBrowserClient(supabaseUrl, supabaseAnonKey)
}

// Function to submit email and trigger freebie
export async function submitEmail(email: string) {
    try {
        // Call the Edge Function
        const response = await fetch(
            `${supabaseUrl}/functions/v1/send-freebie`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${supabaseAnonKey}`,
                },
                body: JSON.stringify({ email }),
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to submit');
        }

        return { success: true };
    } catch (error) {
        console.error('Submission error:', error);
        return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
}
