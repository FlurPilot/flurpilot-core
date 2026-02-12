// Basic server availability check using native fetch
// If this fails on old Node, we'd need http module, but Next 16 implies Node 18+

async function checkServer() {
    console.log("Checking http://localhost:3000 ...");
    try {
        const res = await fetch('http://localhost:3000');
        console.log('Status:', res.status);
        if (res.status >= 200 && res.status < 400) {
            console.log('✅ Server is UP and responding!');
            process.exit(0);
        } else {
            console.log('⚠️ Server returned status:', res.status);
            // 404 is still technically "up", but we expect 200 for root
            if (res.status === 404) console.log("Page not found, but server is listening.");
            process.exit(0);
        }
    } catch (e) {
        console.error('❌ Connection failed:', e.message);
        if (e.cause) console.error('Cause:', e.cause);
        process.exit(1);
    }
}

checkServer();
