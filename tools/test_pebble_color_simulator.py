#!/usr/bin/env python3
"""
Test script for the Pebble color simulator.
Validates that the simulator generates the correct color palette and produces valid output.
"""

import os
import sys
import tempfile
import unittest

# Add tools directory to path so we can import the simulator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

try:
    from pebble_color_simulator import get_pebble64_palette, create_simulator
    from PIL import Image
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please install required packages: pip3 install pillow")
    sys.exit(1)


class TestPebbleColorSimulator(unittest.TestCase):
    
    def test_color_palette_size(self):
        """Test that the palette contains exactly 64 colors."""
        palette = get_pebble64_palette()
        self.assertEqual(len(palette), 64)
    
    def test_color_levels(self):
        """Test that each channel uses only the expected 4 levels."""
        palette = get_pebble64_palette()
        expected_levels = {0, 85, 170, 255}
        
        r_values = {color[0] for color in palette}
        g_values = {color[1] for color in palette}
        b_values = {color[2] for color in palette}
        
        self.assertEqual(r_values, expected_levels)
        self.assertEqual(g_values, expected_levels)
        self.assertEqual(b_values, expected_levels)
    
    def test_specific_colors(self):
        """Test that specific expected colors are in the palette."""
        palette = get_pebble64_palette()
        
        # Test corner colors
        self.assertIn((0, 0, 0), palette)        # Black
        self.assertIn((255, 255, 255), palette)  # White
        self.assertIn((255, 0, 0), palette)      # Red
        self.assertIn((0, 255, 0), palette)      # Green
        self.assertIn((0, 0, 255), palette)      # Blue
        self.assertIn((255, 255, 0), palette)    # Yellow
        self.assertIn((255, 0, 255), palette)    # Magenta
        self.assertIn((0, 255, 255), palette)    # Cyan
    
    def test_color_uniqueness(self):
        """Test that all colors in the palette are unique."""
        palette = get_pebble64_palette()
        unique_colors = set(palette)
        self.assertEqual(len(palette), len(unique_colors))
    
    def test_simulator_grid_output(self):
        """Test that the simulator generates valid PNG output with grid layout."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            try:
                img = create_simulator(layout="grid", output_file=tmp_file.name)
                
                # Check that file was created
                self.assertTrue(os.path.exists(tmp_file.name))
                
                # Check image properties
                self.assertEqual(img.size, (280, 280))
                self.assertEqual(img.mode, 'RGB')
                
                # Verify file is a valid PNG
                with Image.open(tmp_file.name) as test_img:
                    self.assertEqual(test_img.size, (280, 280))
                    self.assertEqual(test_img.mode, 'RGB')
                    
            finally:
                # Clean up
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_simulator_circles_output(self):
        """Test that the simulator generates valid PNG output with circles layout."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            try:
                img = create_simulator(layout="circles", output_file=tmp_file.name)
                
                # Check that file was created
                self.assertTrue(os.path.exists(tmp_file.name))
                
                # Check image properties
                self.assertEqual(img.size, (280, 280))
                self.assertEqual(img.mode, 'RGB')
                
            finally:
                # Clean up
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)


if __name__ == '__main__':
    unittest.main()