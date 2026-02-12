/* eslint-disable @typescript-eslint/no-require-imports */
const ai = require('ai');
console.log('Exports:', JSON.stringify(Object.keys(ai), null, 2));
try {
    const deep = require('ai/rsc');
    console.log('RSC Exports:', JSON.stringify(Object.keys(deep), null, 2));
} catch {
    console.log('No RSC exports');
}
