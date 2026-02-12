import createMiddleware from 'next-intl/middleware';
import { type NextRequest, NextResponse } from 'next/server';
import { updateSession } from '@/utils/supabase/middleware';
import { locales, defaultLocale } from '@/i18n/config';

const intlMiddleware = createMiddleware({
    locales,
    defaultLocale,
    localePrefix: 'as-needed',
});

export async function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;

    // Skip locale handling for API routes and static files
    if (
        pathname.startsWith('/_next') ||
        pathname.startsWith('/api') ||
        pathname.includes('.')
    ) {
        return NextResponse.next();
    }

    // 1. Run intl middleware first (handles locale detection & redirect)
    const intlResponse = intlMiddleware(request);

    // 2. Auth checks for protected routes
    const localePattern = `^/(${locales.join('|')})?/?`;
    const pathnameWithoutLocale = pathname.replace(new RegExp(localePattern), '/');

    if (pathnameWithoutLocale.startsWith('/dashboard')) {
        const { user } = await updateSession(request);

        if (!user) {
            const locale = pathname.match(new RegExp(localePattern))?.[1] || defaultLocale;
            const url = request.nextUrl.clone();
            url.pathname = `/${locale}/login`;
            return NextResponse.redirect(url);
        }

        // FIDO2/MFA Enforcement for admins
        const aal = user.app_metadata?.aal || 'aal1';
        const role = user.app_metadata?.role || 'user';

        if (role === 'admin' && aal !== 'aal2') {
            const locale = pathname.match(new RegExp(localePattern))?.[1] || defaultLocale;
            const url = request.nextUrl.clone();
            url.pathname = `/${locale}/auth/mfa`;
            return NextResponse.redirect(url);
        }
    }

    if (pathnameWithoutLocale.startsWith('/login')) {
        const { user } = await updateSession(request);
        if (user) {
            const locale = pathname.match(new RegExp(localePattern))?.[1] || defaultLocale;
            const url = request.nextUrl.clone();
            url.pathname = `/${locale}/dashboard`;
            return NextResponse.redirect(url);
        }
    }

    return intlResponse;
}

export const config = {
    matcher: [
        '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
    ],
};
