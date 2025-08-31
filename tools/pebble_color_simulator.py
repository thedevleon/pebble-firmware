#!/usr/bin/env python3
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pebble Watch Color Simulator

This simulator renders the 64 colors supported by the Pebble watch in a round
display format with 280x280 resolution, matching the actual watch display.
"""

import math
import argparse
from PIL import Image, ImageDraw


def get_pebble64_palette():
    """
    Generate the 64 colors supported by Pebble watches.
    Each color channel uses 2 bits (4 levels: 0, 85, 170, 255).
    
    Returns:
        List of (R, G, B) tuples representing all 64 Pebble colors
    """
    palette = []
    for i in range(64):
        r = ((i >> 4) & 0x3) * 85  # Red: bits 5-4
        g = ((i >> 2) & 0x3) * 85  # Green: bits 3-2  
        b = ((i     ) & 0x3) * 85  # Blue: bits 1-0
        palette.append((r, g, b))
    return palette


def create_round_mask(size):
    """
    Create a circular mask for round display simulation.
    
    Args:
        size: Diameter of the circular mask
        
    Returns:
        PIL Image mask (1-bit) with circular cutout
    """
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw a filled circle (white = visible, black = transparent)
    margin = 2  # Small margin to ensure clean edges
    draw.ellipse([margin, margin, size-margin, size-margin], fill=255)
    
    return mask


def arrange_colors_in_grid(colors, display_size):
    """
    Arrange 64 colors in an 8x8 grid within the circular display.
    
    Args:
        colors: List of (R, G, B) color tuples
        display_size: Size of the display (280x280)
        
    Returns:
        PIL Image with colors arranged in grid
    """
    # Create the base image
    img = Image.new('RGB', (display_size, display_size), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate grid parameters
    grid_size = 8  # 8x8 grid for 64 colors
    
    # Calculate usable area (inscribed square in circle)
    # For a circle with radius R, inscribed square has side length R*sqrt(2)
    radius = display_size // 2
    usable_size = int(radius * math.sqrt(2) * 0.9)  # 90% for margins
    
    # Center the grid
    start_x = (display_size - usable_size) // 2
    start_y = (display_size - usable_size) // 2
    
    # Size of each color cell
    cell_size = usable_size // grid_size
    
    # Draw each color
    for i, color in enumerate(colors):
        row = i // grid_size
        col = i % grid_size
        
        x1 = start_x + col * cell_size
        y1 = start_y + row * cell_size
        x2 = x1 + cell_size - 1  # -1 for small gap between cells
        y2 = y1 + cell_size - 1
        
        draw.rectangle([x1, y1, x2, y2], fill=color)
    
    return img


def arrange_colors_in_circles(colors, display_size):
    """
    Arrange 64 colors in concentric circles for a more watch-like appearance.
    
    Args:
        colors: List of (R, G, B) color tuples
        display_size: Size of the display (280x280)
        
    Returns:
        PIL Image with colors arranged in concentric circles
    """
    img = Image.new('RGB', (display_size, display_size), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = center_y = display_size // 2
    
    # Define rings: center + 3 concentric rings
    # Ring 0: 1 color (center)
    # Ring 1: 7 colors  
    # Ring 2: 14 colors
    # Ring 3: 42 colors (remaining)
    rings = [
        {"count": 1, "radius": 15},
        {"count": 7, "radius": 45}, 
        {"count": 14, "radius": 75},
        {"count": 42, "radius": 110}
    ]
    
    color_index = 0
    
    for ring in rings:
        count = ring["count"]
        radius = ring["radius"]
        
        if count == 1:
            # Center circle
            color = colors[color_index]
            draw.ellipse([center_x - radius, center_y - radius, 
                         center_x + radius, center_y + radius], fill=color)
            color_index += 1
        else:
            # Arrange colors around the ring
            angle_step = 2 * math.pi / count
            cell_radius = ring["radius"] // 4  # Size of each color cell
            
            for i in range(count):
                if color_index >= len(colors):
                    break
                    
                angle = i * angle_step
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                color = colors[color_index]
                draw.ellipse([x - cell_radius, y - cell_radius,
                             x + cell_radius, y + cell_radius], fill=color)
                color_index += 1
    
    return img


def create_simulator(layout="grid", output_file="pebble_colors.png"):
    """
    Create the Pebble color simulator image.
    
    Args:
        layout: "grid" or "circles" - how to arrange the colors
        output_file: Output filename for the generated image
    """
    display_size = 280
    
    # Get the Pebble color palette
    colors = get_pebble64_palette()
    
    print(f"Generating Pebble color simulator with {len(colors)} colors...")
    print(f"Display size: {display_size}x{display_size} (round)")
    print(f"Layout: {layout}")
    
    # Create the image with color arrangement
    if layout == "circles":
        img = arrange_colors_in_circles(colors, display_size)
    else:
        img = arrange_colors_in_grid(colors, display_size)
    
    # Apply circular mask to simulate round display
    mask = create_round_mask(display_size)
    
    # Create final image with black background and masked color display
    final_img = Image.new('RGB', (display_size, display_size), (0, 0, 0))
    final_img.paste(img, mask=mask)
    
    # Save the result
    final_img.save(output_file)
    print(f"Simulator saved as: {output_file}")
    
    # Print some color statistics
    print(f"\nPebble Color Palette Info:")
    print(f"Total colors: {len(colors)}")
    print(f"Color depth: 2 bits per channel (4 levels)")
    print(f"Channel levels: 0, 85, 170, 255")
    print(f"First few colors: {colors[:5]}")
    print(f"Last few colors: {colors[-5:]}")
    
    return final_img


def main():
    parser = argparse.ArgumentParser(description="Pebble Watch Color Simulator")
    parser.add_argument("--layout", choices=["grid", "circles"], default="grid",
                       help="Layout style for color arrangement (default: grid)")
    parser.add_argument("--output", default="pebble_colors.png",
                       help="Output filename (default: pebble_colors.png)")
    
    args = parser.parse_args()
    
    create_simulator(layout=args.layout, output_file=args.output)


if __name__ == "__main__":
    main()