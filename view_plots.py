#!/usr/bin/env python3
"""
Simple script to view generated plots in Docker environment
"""

import os
import glob
from pathlib import Path

def list_plot_files():
    """List all PNG plot files in the current directory"""
    plot_files = glob.glob("*.png")
    if not plot_files:
        print("No plot files found in current directory.")
        return
    
    print("Generated plot files:")
    for i, file in enumerate(sorted(plot_files), 1):
        file_size = os.path.getsize(file)
        print(f"{i}. {file} ({file_size} bytes)")

def main():
    print("=== Raman ML Classification - Plot Viewer ===")
    print()
    list_plot_files()
    print()
    print("To view plots:")
    print("1. Copy the PNG files to your host machine")
    print("2. Open them with any image viewer")
    print("3. Or use: docker cp <container_name>:/app/<filename>.png .")

if __name__ == "__main__":
    main()
