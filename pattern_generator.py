#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display Pattern Generator

This module provides a class for generating various test patterns to check display
functionality, appearance, and optical performance characteristics.
"""

import numpy as np
import cv2
import os
import logging
import argparse
from typing import Tuple, List, Dict, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PatternGenerator:
    """
    A class to generate various test patterns for display testing.
    
    This class can generate solid colors, grayscale patterns, crosstalk patterns,
    grid patterns, and more for testing display characteristics.
    """
    
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the PatternGenerator with display dimensions.
        
        Args:
            width: Width of the display in pixels
            height: Height of the display in pixels
            output_dir: Directory to save generated patterns
        """
        self.width = width
        self.height = height
        self.output_dir = "patterns/" + str(width) + "x" + str(height)  
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
        
        # Define common colors (RGB format)
        self.colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray16": (15, 15, 15),
            "gray32": (31, 31, 31),
            "gray64": (63, 63, 63),
            "gray128": (127, 127, 127),
            "yellow": (255, 255, 0),
            "magenta": (255, 0, 255),
            "cyan": (0, 255, 255)
        }
        
        logger.info(f"PatternGenerator initialized with resolution {width}x{height}")
    
    def create_blank(self, rgb_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
        """
        Create a blank image with the specified color.
        
        Args:
            rgb_color: RGB color tuple
            
        Returns:
            A numpy array representing the image
        """
        image = np.zeros((self.height, self.width, 3), np.uint8)
        # OpenCV uses BGR color order
        bgr_color = tuple(reversed(rgb_color))
        image[:] = bgr_color
        return image
    
    def save_image(self, image: np.ndarray, filename: str) -> str:
        """
        Save an image to the output directory.
        
        Args:
            image: The image to save
            filename: The filename to save as
            
        Returns:
            The full path to the saved file
        """
        if not filename.endswith(('.bmp', '.png', '.jpg', '.jpeg', '.tiff')):
            filename += '.bmp'  # Default to BMP format
            
        filepath = os.path.join(self.output_dir, filename)
        cv2.imwrite(filepath, image)
        logger.info(f"Saved image to {filepath}")
        return filepath
    
    def generate_solid_color(self, color_name: str = "white", save: bool = True) -> np.ndarray:
        """
        Generate a solid color pattern.
        
        Args:
            color_name: Name of the color (must be in self.colors)
            save: Whether to save the image
            
        Returns:
            The generated image
        """
        if color_name not in self.colors:
            raise ValueError(f"Color {color_name} not found. Available colors: {list(self.colors.keys())}")
        
        image = self.create_blank(self.colors[color_name])
        
        if save:
            self.save_image(image, f"solid_{color_name}")
        
        return image
    
    def generate_all_solid_colors(self) -> Dict[str, np.ndarray]:
        """
        Generate all solid color patterns.
        
        Returns:
            Dictionary of color names to images
        """
        result = {}
        for color_name in ["red", "green", "blue", "white", "black"]:
            result[color_name] = self.generate_solid_color(color_name)
        return result
    
    def generate_grayscale(self, levels: int = 256, reversed: bool = False, save: bool = True) -> np.ndarray:
        """
        Generate a grayscale gradient pattern.
        
        Args:
            levels: Number of grayscale levels
            reversed: Whether to reverse the gradient (white to black)
            save: Whether to save the image
            
        Returns:
            The generated image
        """
        image = np.zeros((self.height, self.width, 3), np.uint8)
        
        # Create gradient from left to right
        for i in range(self.width):
            value = int(i * 255 / self.width)
            if reversed:
                value = 255 - value
            image[:, i] = (value, value, value)
        
        if save:
            suffix = "_reversed" if reversed else ""
            self.save_image(image, f"grayscale{suffix}")
        
        return image
    
    def generate_grayscale_levels(self, save: bool = True) -> Dict[str, np.ndarray]:
        """
        Generate grayscale level patterns (gray16, gray32, gray64).
        
        Args:
            save: Whether to save the images
            
        Returns:
            Dictionary of level names to images
        """
        result = {}
        for level_name in ["gray16", "gray32", "gray64"]:
            image = self.create_blank(self.colors[level_name])
            if save:
                self.save_image(image, f"img_{level_name}")
            result[level_name] = image
        return result
    
    def generate_crosstalk(self, background_color: str = "white", 
                          box_color: str = "black", save: bool = True) -> np.ndarray:
        """
        Generate a crosstalk test pattern with a centered box.
        
        Args:
            background_color: Color name for the background
            box_color: Color name for the center box
            save: Whether to save the image
            
        Returns:
            The generated image
        """
        if background_color not in self.colors or box_color not in self.colors:
            raise ValueError("Invalid color name")
        
        image = self.create_blank(self.colors[background_color])
        
        # Create a box in the center
        box_width = self.width // 3
        box_height = self.height // 3
        
        x_start = (self.width - box_width) // 2
        y_start = (self.height - box_height) // 2
        
        # Define the box vertices
        pts = np.array([
            [x_start, y_start], 
            [x_start + box_width, y_start], 
            [x_start + box_width, y_start + box_height], 
            [x_start, y_start + box_height]
        ])
        
        # Fill the box with the specified color
        cv2.fillPoly(image, [pts], tuple(reversed(self.colors[box_color])))
        
        if save:
            self.save_image(image, f"crosstalk_{background_color}_{box_color}")
        
        return image
    
    def generate_all_crosstalk(self) -> Dict[str, np.ndarray]:
        """
        Generate all crosstalk test patterns.
        
        Returns:
            Dictionary of pattern names to images
        """
        result = {}
        combinations = [
            ("white", "black"),
            ("gray32", "black"),
            ("black", "blue"),
            ("black", "cyan"),
            ("gray32", "white"),
            ("black", "gray32"),
            ("green", "gray32"),
            ("magenta", "gray32"),
            ("red", "gray32"),
            ("yellow", "gray32")
        ]
        
        for bg, fg in combinations:
            name = f"crosstalk_{bg}_{fg}"
            result[name] = self.generate_crosstalk(bg, fg, save=True)
        
        return result
    
    def generate_grid(self, rows: int, cols: int, 
                     line_color: str = "white", 
                     background_color: str = "black",
                     line_thickness: int = 1,
                     save: bool = True,
                     suffix: str = "A") -> np.ndarray:
        """
        Generate a grid pattern.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            line_color: Color name for the grid lines
            background_color: Color name for the background
            line_thickness: Thickness of grid lines in pixels
            save: Whether to save the image
            suffix: Suffix to add to the filename (A or B)
            
        Returns:
            The generated image
        """
        if line_color not in self.colors or background_color not in self.colors:
            raise ValueError("Invalid color name")
        
        image = self.create_blank(self.colors[background_color])
        
        # Calculate cell dimensions
        cell_width = self.width // cols
        cell_height = self.height // rows
        
        # Draw grid with alternating colors
        for y in range(rows):
            for x in range(cols):
                # Calculate top-left corner of the cell
                top_left_x = x * cell_width
                top_left_y = y * cell_height
                # Calculate bottom-right corner of the cell
                bottom_right_x = (x + 1) * cell_width
                bottom_right_y = (y + 1) * cell_height
                # Determine color based on position
                if (x + y) % 2 == 0:
                    cell_color = self.colors[line_color]
                else:
                    cell_color = self.colors[background_color]
                # Define the vertices of the cell
                pts = np.array([
                    [top_left_x, top_left_y],
                    [bottom_right_x, top_left_y],
                    [bottom_right_x, bottom_right_y],
                    [top_left_x, bottom_right_y]
                ])
                # Fill the cell with the determined color
                cv2.fillPoly(image, [pts], tuple(reversed(cell_color)))
        
        if save:
            self.save_image(image, f"{cols}x{rows}{suffix}")
        
        return image
    
    def generate_all_grids(self) -> Dict[str, np.ndarray]:
        """
        Generate all grid patterns.
        
        Returns:
            Dictionary of pattern names to images
        """
        result = {}
        grid_configs = [
            (1, 2),
            (1, 16),
            (1, self.width),
            (2, 1),
            (3, 32),
            (6, 1),
            (6, 16),
            (6, 32),
            (self.height, 1)
        ]
        
        for rows, cols in grid_configs:
            for suffix in ["A", "B"]:
                bg_color = "black" if suffix == "A" else "white"
                line_color = "white" if suffix == "A" else "black"
                
                name = f"{cols}x{rows}{suffix}"
                result[name] = self.generate_grid(rows, cols, line_color, bg_color, save=True, suffix=suffix)
        
        return result
    
    def generate_skip_one_pixel(self, save: bool = True) -> np.ndarray:
        """
        Generate a skip-one-pixel pattern (checkerboard).
        
        Args:
            save: Whether to save the image
            
        Returns:
            The generated image
        """
        image = np.zeros((self.height, self.width, 3), np.uint8)
        
        # Create checkerboard pattern
        square_size = 2  # 2x2 pixel squares
        
        for y in range(0, self.height, square_size):
            for x in range(0, self.width, square_size):
                if (x // square_size + y // square_size) % 2 == 0:
                    image[y:min(y+square_size, self.height), 
                         x:min(x+square_size, self.width)] = (255, 255, 255)
        
        if save:
            self.save_image(image, "skip_one_pixel")
        
        return image
    
    def generate_all_patterns(self) -> Dict[str, np.ndarray]:
        """
        Generate all test patterns.
        
        Returns:
            Dictionary of all pattern names to images
        """
        result = {}
        
        # Generate solid colors
        result.update(self.generate_all_solid_colors())
        
        # Generate grayscale levels
        result.update(self.generate_grayscale_levels())
        
        # Generate grayscale gradients
        result["grayscale"] = self.generate_grayscale(save=True)
        result["grayscale_reversed"] = self.generate_grayscale(reversed=True, save=True)
        
        # Generate crosstalk patterns
        result.update(self.generate_all_crosstalk())
        
        # Generate grid patterns
        result.update(self.generate_all_grids())
        
        # Generate skip-one-pixel pattern
        result["skip_one_pixel"] = self.generate_skip_one_pixel(save=True)
        
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate display test patterns.')
    parser.add_argument('--width', type=int, default=2560, help='Width of the display in pixels')
    parser.add_argument('--height', type=int, default=1664, help='Height of the display in pixels')
    args = parser.parse_args()

    generator = PatternGenerator(width=args.width, height=args.height)
    generator.generate_all_patterns()