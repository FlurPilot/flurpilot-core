import subprocess
import sys
import os

# Allow-list (Permissive Licenses)
# Section 5: MIT, Apache, BSD allowed. Copyleft forbidden.
WHITELIST = [
    "MIT License",
    "Apache Software License",
    "BSD License",
    "ISC License (ISCL)",
    "Mozilla Public License 2.0 (MPL 2.0)", # MPL is weak copyleft, usually allowed if file-bound, but let's be strict if needed.
    # Lastenheft says: "Verbot: Keine Copyleft-Lizenzen (GPL, AGPL) im distribuierbaren Code"
    # MPL is border-line, but usually okay for SaaS if not modifying the lib.
    # For now, we allow it, but flag GPL strictly.
]

# Strict Blacklist
BLACKLIST = [
    "GNU General Public License",
    "GPL",
    "AGPL",
    "Affero"
]

def check_licenses():
    print("🔎 Running License Compliance Audit (Python)...")
    
    # Run pip-licenses
    # Format: Package, Version, License
    try:
        result = subprocess.run(
            ["pip-licenses", "--format=markdown", "--with-system"],
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("❌ pip-licenses not found. Please install it (pip install pip-licenses).")
        sys.exit(1)

    output = result.stdout
    lines = output.split('\n')
    
    violations = []
    
    # Simple parsing of markdown table
    # skipped header
    
    print("\n--- License Audit Report ---")
    
    # We also re-run to get JSON for easier parsing if needed, but text scan is fine for "contains" check
    # Let's search for Blacklisted terms in the output
    
    for line in lines:
        lower_line = line.lower()
        for bad in BLACKLIST:
            if bad.lower() in lower_line:
                # Check if it's dual licensed with a permissive one (e.g. "GPL, MIT")
                # If "MIT" is also in the line, we might excuse it, but manual review is safer.
                if "mit" in lower_line or "apache" in lower_line or "bsd" in lower_line:
                     print(f"⚠️ Dual License warning (Manual Check): {line.strip()}")
                else:
                     violations.append(line.strip())

    # Write Report
    with open("license-report.md", "w", encoding="utf-8") as f:
        f.write("# Software Bill of Materials & License Audit\n\n")
        f.write(output)
    
    print("✅ Report generated: license-report.md")

    if violations:
        print("\n❌ CRITICAL: Incompatible Licenses Found!")
        for v in violations:
            print(f"  - {v}")
        print("\nFix: Replace these dependencies or buy a commercial license.")
        sys.exit(1)
    else:
        print("\n✅ Compliance Check Passed. No GPL/AGPL detected.")
        sys.exit(0)

if __name__ == "__main__":
    check_licenses()
