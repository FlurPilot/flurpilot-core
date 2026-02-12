@echo off
setlocal
cd /d "%~dp0"
echo Setting up Visual Studio Environment...
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (
    call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
) else (
    if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
    ) else (
        echo Error: Could not find Visual Studio Build Tools. Please install "Desktop development with C++" workload.
        exit /b 1
    )
)

echo Building geometry-engine for web...
where wasm-pack >nul 2>nul
if %errorlevel% neq 0 (
    echo Warning: wasm-pack not found. Attempting raw cargo build...
    cargo build --target wasm32-unknown-unknown --no-default-features --features wasm
) else (
    wasm-pack build --target web -- --no-default-features --features wasm
)

echo Build complete.
endlocal
