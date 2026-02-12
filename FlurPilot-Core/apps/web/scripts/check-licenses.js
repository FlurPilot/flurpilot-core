/* eslint-disable @typescript-eslint/no-require-imports */
const checker = require('license-checker');
const fs = require('fs');
const path = require('path');

// Configuration
const ALLOWED_LICENSES = [
    'MIT',
    'Apache-2.0',
    'BSD-3-Clause',
    'BSD-2-Clause',
    'ISC',
    'Unlicense',
    '0BSD',
    'MPL-2.0', // Mozilla Public License 2.0 (Weak Copyleft, usually OK for SaaS)
    'CC0-1.0'
];

const FORBIDDEN_LICENSES = [
    'GPL',
    'AGPL',
    'LGPL' // LGPL is strict for proprietary linking sometimes, let's flag it.
];

console.log('🔎 Running License Compliance Audit (Node)...');

checker.init({
    start: path.join(__dirname, '..'), // Scan app root
    production: true, // Ignore devDependencies (The "Optimized" flag)
    unknown: true,    // Report unknown licenses
    excludePrivatePackages: true,
}, function (err, packages) {
    if (err) {
        console.error('checker error:', err);
        process.exit(1);
    }

    let violations = [];
    let reportLines = ['Package,Version,License,Repository'];

    Object.keys(packages).forEach(pkgName => {
        const pkg = packages[pkgName];
        const license = pkg.licenses ? (Array.isArray(pkg.licenses) ? pkg.licenses.join(' OR ') : pkg.licenses) : 'UNKNOWN';

        // Check Compliance
        let isAllowed = false;

        // 1. Check if ANY allowed license is present (handling dual license "MIT OR GPL")
        // If "MIT" is present, it's compatible.
        for (const allowed of ALLOWED_LICENSES) {
            if (license.includes(allowed)) {
                isAllowed = true;
                break;
            }
        }

        if (!isAllowed) {
            // Double check for Forbidden terms
            for (const forbidden of FORBIDDEN_LICENSES) {
                if (license.includes(forbidden)) {
                    violations.push(`${pkgName} (${license})`);
                    break;
                }
            }
        }

        reportLines.push(`"${pkgName}","${pkg.licenseFile || ''}","${license}","${pkg.repository || ''}"`);
    });

    // Write Report
    fs.writeFileSync(path.join(__dirname, '..', 'license-report.csv'), reportLines.join('\n'));
    console.log('✅ Report generated: license-report.csv');

    if (violations.length > 0) {
        console.error('\n❌ CRITICAL: Incompatible Licenses Found!');
        violations.forEach(v => console.error(`  - ${v}`));
        console.error('\nFix: Replace these dependencies.');
        process.exit(1);
    } else {
        console.log('\n✅ Compliance Check Passed. No GPL/AGPL detected in production build.');
        process.exit(0);
    }
});
