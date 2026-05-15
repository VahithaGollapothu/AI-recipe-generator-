#!/usr/bin/env python3
"""Test script to debug recipe generation"""
import sys
sys.path.insert(0, '.')

from utils.api_handler import generate_recipe

print("Testing recipe generation...")
result = generate_recipe(
    ingredients="2 eggs, 100g spinach, butter, salt",
    cuisine="Italian",
    diet_type="High Protein"
)

print("\n=== RESULT ===")
for key, value in result.items():
    if key == "raw_output":
        print(f"\n{key}:\n{value[:500] if value else 'None'}")
    else:
        val_str = str(value)[:100] if value else "None"
        print(f"{key}: {val_str}")
