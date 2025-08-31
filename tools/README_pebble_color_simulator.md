# Pebble Watch Color Simulator

This simulator renders the 64 colors supported by the Pebble watch in a round display format with 280x280 resolution, matching the actual watch display characteristics.

## Overview

The Pebble watch uses a 64-color palette with 2 bits per RGB channel, providing 4 intensity levels per channel:
- **Color levels**: 0, 85, 170, 255
- **Total colors**: 4³ = 64 colors
- **Color format**: 2-bit per channel (RRGGBB)

## Usage

```bash
# Generate grid layout (default)
python3 tools/pebble_color_simulator.py

# Generate circular layout
python3 tools/pebble_color_simulator.py --layout circles

# Specify custom output file
python3 tools/pebble_color_simulator.py --output my_colors.png

# Get help
python3 tools/pebble_color_simulator.py --help
```

## Layouts

### Grid Layout (default)
Arranges all 64 colors in an 8×8 grid within the circular display area. This layout provides a systematic view of the color palette, making it easy to see the progression of colors and identify specific color values.

### Circles Layout  
Arranges colors in concentric circles around a center point, creating a more watch-face-like appearance:
- Center: 1 color
- Inner ring: 7 colors
- Middle ring: 14 colors  
- Outer ring: 42 colors

## Features

- **Round display simulation**: Uses a circular mask to simulate the actual round watch display
- **Accurate color palette**: Uses the same color generation algorithm as the Pebble firmware
- **Multiple layouts**: Choose between systematic grid or watch-like circular arrangements
- **280×280 resolution**: Matches actual Pebble watch display size
- **PNG output**: High-quality output suitable for documentation and testing

## Requirements

- Python 3.x
- Pillow (PIL) - for image generation

```bash
pip3 install pillow
```

## Technical Details

The color palette is generated using the same algorithm as the Pebble firmware:

```python
def get_pebble64_palette():
    palette = []
    for i in range(64):
        r = ((i >> 4) & 0x3) * 85  # Red: bits 5-4
        g = ((i >> 2) & 0x3) * 85  # Green: bits 3-2  
        b = ((i     ) & 0x3) * 85  # Blue: bits 1-0
        palette.append((r, g, b))
    return palette
```

This generates exactly the same 64 colors that are supported by the Pebble watch hardware and firmware.