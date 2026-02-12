import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./i18n/request.ts');

/** @type {import('next').NextConfig} */
const nextConfig = {
    // Turbopack config (Next.js 16 default)
    turbopack: {
        // Turbopack supports async WASM out of the box
    },
    // Webpack config (fallback for --webpack flag)
    webpack: (config) => {
        config.experiments = {
            ...config.experiments,
            asyncWebAssembly: true,
            layers: true,
        };
        return config;
    },
};

export default withNextIntl(nextConfig);
