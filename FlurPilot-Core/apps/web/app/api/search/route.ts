import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/utils/supabase/server'; // Assumes standardized server client creator
import { z } from 'zod';
import { cookies } from 'next/headers';

// --- Configuration ---
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute
const MAX_REQUESTS_PER_WINDOW = 20;
// Simple in-memory rate limit store (Note: In production, use Redis!)
const rateLimitMap = new Map<string, { count: number, resetTime: number }>();

// Honeytoken Data (Fake Records)
const HONEYTOKENS = [
    { type: 'city', id: 'ht_muc_01', name: 'Bielefeld-Süd (Sperrgebiet)', state: 'FakeState' },
    { type: 'parcel', id: 'ht_par_99', alkis_id: 'TEST-FLUR-9999', geom: null, properties: { usage: 'Top Secret' } }
];

// Input Validation Schema
const searchSchema = z.object({
    q: z.string().min(2).max(100).regex(/^[a-zA-Z0-9\s\-\.]+$/),
});

// --- Helper Functions ---

function checkRateLimit(ip: string): boolean {
    const now = Date.now();
    const record = rateLimitMap.get(ip);

    if (!record || now > record.resetTime) {
        rateLimitMap.set(ip, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
        return true;
    }

    if (record.count >= MAX_REQUESTS_PER_WINDOW) {
        return false;
    }

    record.count++;
    return true;
}

async function logSearchAudit(userId: string, query: string, ip: string) {
    // Merkle Tree Logic (Mock for MVP)
    // in production this would push to a tamper-proof append-only log
    const timestamp = new Date().toISOString();
    // const hash = crypto.createHash('sha256').update(userId + query + timestamp).digest('hex');
    console.log(`[AUDIT] User: ${userId} | Query: "${query}" | IP: ${ip} | TS: ${timestamp} | MerkleRoot: <pending>`);
}

// --- API Route Handler ---

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('q');
    const lookupCity = searchParams.get('lookup_city');
    const ip = request.headers.get('x-forwarded-for') || 'unknown';

    // 1. Rate Limiting (Defense Layer 1)
    if (!checkRateLimit(ip)) {
        return NextResponse.json(
            { error: 'Rate limit exceeded.' },
            { status: 429 }
        );
    }

    // 2. Authentication (Zero Trust)
    const cookieStore = await cookies();
    const supabase = await createClient();

    const { data: { user }, error: authError } = await supabase.auth.getUser();

    if (authError || !user) {
        return NextResponse.json(
            { error: 'Unauthorized.' },
            { status: 401 }
        );
    }

    // A. City Lookup Mode (Navigation helper)
    if (lookupCity) {
        try {
            const { data } = await supabase
                .from('geo_parcels')
                .select('id, alkis_id, geom, properties')
                .contains('properties', { municipality: lookupCity })
                .limit(1)
                .single();

            return NextResponse.json(data || null);
        } catch (e) {
            return NextResponse.json({ error: 'Lookup failed' }, { status: 500 });
        }
    }

    // B. Standard Search Mode
    // 3. Input Validation
    const validation = searchSchema.safeParse({ q: query });
    if (!validation.success) {
        return NextResponse.json(
            { error: 'Invalid query. Min 2 chars, alphanumeric only.' },
            { status: 400 }
        );
    }
    const safeQuery = validation.data.q;

    // 4. Audit Logging (Compliance) -- ONLY log actual searches, not internal lookups
    await logSearchAudit(user.id, safeQuery, ip);

    try {
        // 5. Database Queries (Parallel)
        const [cities, parcels] = await Promise.all([
            // Query Municipalities
            supabase
                .from('scout_profiles')
                .select('id, name')
                .ilike('name', `%${safeQuery}%`)
                .limit(3),

            // Query Parcels
            supabase
                .from('geo_parcels')
                .select('id, alkis_id, geom, properties')
                .ilike('alkis_id', `%${safeQuery}%`)
                .limit(5)
        ]);

        const results = [
            ...(cities.data || []).map(c => ({ type: 'city' as const, ...c })),
            ...(parcels.data || []).map(p => ({ type: 'parcel' as const, ...p }))
        ];

        // 6. Honeytoken Injection (Active Defense)
        // Inject a honeytoken if the query looks suspicious or at random (1% chance)
        // "Bielefeld" is a common joke in DE that it doesn't exist, perfect honeytoken trigger
        if (Math.random() < 0.01 || safeQuery.toLowerCase().includes('bielefeld')) {
            results.push(HONEYTOKENS[0]); // Inject fake city
            console.warn(`[DEFENSE] Honeytoken injected for user ${user.id}`);
        }

        return NextResponse.json(results);

    } catch (dbError) {
        console.error('Search API Error:', dbError);
        return NextResponse.json(
            { error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
