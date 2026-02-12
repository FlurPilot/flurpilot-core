/**
 * Sitemap Generator for FlurPilot pSEO Pages
 * Run: node scripts/generate-sitemap.js
 * Outputs: 
 *   - dist/sitemap.xml (main sitemap with static pages)
 *   - dist/sitemap-loesungen.xml (dynamic pSEO pages)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load keywords data
const keywordsPath = path.join(__dirname, '../src/data/keywords.json');
const keywordsData = JSON.parse(fs.readFileSync(keywordsPath, 'utf-8'));

const DOMAIN = 'https://flurpilot.de';
const TODAY = new Date().toISOString().split('T')[0];

// Static pages for main sitemap
const staticPages = [
    { loc: '/', priority: '1.0', changefreq: 'weekly' },
    { loc: '/impressum', priority: '0.3', changefreq: 'yearly' },
    { loc: '/datenschutz', priority: '0.3', changefreq: 'yearly' },
    { loc: '/agb', priority: '0.3', changefreq: 'yearly' },
];

// Dynamic pSEO pages for loesungen sitemap
const dynamicPages = keywordsData.map(kw => ({
    loc: `/loesungen/${kw.slug}`,
    priority: '0.8',
    changefreq: 'monthly',
}));

// Generate XML sitemap
function generateSitemap(pages) {
    return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(page => `  <url>
    <loc>${DOMAIN}${page.loc}</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;
}

// Determine output directory
const distPath = path.join(__dirname, '../dist');
const publicPath = path.join(__dirname, '../public');
const outputDir = fs.existsSync(distPath) ? distPath : publicPath;

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Write main sitemap (static + dynamic)
const mainSitemap = generateSitemap([...staticPages, ...dynamicPages]);
fs.writeFileSync(path.join(outputDir, 'sitemap.xml'), mainSitemap);

// Write loesungen-specific sitemap (dynamic only)
const loesungenSitemap = generateSitemap(dynamicPages);
fs.writeFileSync(path.join(outputDir, 'sitemap-loesungen.xml'), loesungenSitemap);

console.log(`✅ Sitemaps generated:`);
console.log(`   sitemap.xml: ${staticPages.length + dynamicPages.length} URLs`);
console.log(`   sitemap-loesungen.xml: ${dynamicPages.length} URLs`);
console.log(`   Output: ${outputDir}`);

