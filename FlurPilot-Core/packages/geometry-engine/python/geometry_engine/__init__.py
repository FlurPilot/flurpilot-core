"""
FlurPilot Geometry Engine - High-Performance Rust-Powered Geometric Operations

This module provides Python bindings for the Rust geometry engine,
offering significant performance improvements over pure Python solutions.
"""

from .geometry_engine import (
    calculate_virtual_parcel,
    __version__
)

__all__ = ['calculate_virtual_parcel', '__version__']

# Version is set by Rust
VERSION = __version__
