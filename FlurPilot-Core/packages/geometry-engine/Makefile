.PHONY: help build test install clean fmt lint check wasm benchmark

help:
	@echo "FlurPilot Geometry Engine - Available Commands:"
	@echo ""
	@echo "  make build       - Build Python package with Maturin (release)"
	@echo "  make develop     - Build and install in development mode"
	@echo "  make test        - Run all tests (Rust + Python)"
	@echo "  make test-rust   - Run Rust tests only"
	@echo "  make test-python - Run Python tests only"
	@echo "  make install     - Install Python package"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make fmt         - Format Rust code"
	@echo "  make lint        - Run clippy linter"
	@echo "  make check       - Check code without building"
	@echo "  make wasm        - Build WebAssembly target"
	@echo "  make benchmark   - Run performance benchmarks"
	@echo ""

build:
	maturin build --release

develop:
	maturin develop --release

test: test-rust test-python

test-rust:
	cargo test --all-features

test-python: develop
	pytest tests/ -v

install: build
	pip install target/wheels/geometry_engine*.whl --force-reinstall

clean:
	cargo clean
	rm -rf target/
	rm -rf python/geometry_engine/*.so
	rm -rf python/geometry_engine/*.pyd
	rm -rf python/geometry_engine/__pycache__
	rm -rf .pytest_cache

fmt:
	cargo fmt

lint:
	cargo clippy --all-features -- -D warnings

check:
	cargo check --all-features
	cargo fmt -- --check

wasm:
	cargo build --target wasm32-unknown-unknown --release --no-default-features --features wasm

benchmark: develop
	@echo "Running benchmarks..."
	python scripts/benchmark.py
