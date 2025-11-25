#!/usr/bin/env python3
"""
Generate Test Images Script
===========================
Creates sample images with different sizes for JMeter performance testing.

Usage:
    python3 generate-test-images.py

Requirements:
    pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random

def create_image_with_size(filename, target_size_kb, image_format='JPEG'):
    """
    Create an image file with approximately the target size in KB.
    
    Args:
        filename (str): Output filename
        target_size_kb (int): Target file size in KB
        image_format (str): Image format (JPEG or PNG)
    """
    # Calculate approximate dimensions based on target size
    # Rough estimation: JPEG ~10KB per 100x100, PNG ~20KB per 100x100
    if image_format == 'JPEG':
        base_ratio = 10  # KB per 100x100 pixels
    else:
        base_ratio = 20
    
    # Calculate dimensions
    dimension = int((target_size_kb / base_ratio) ** 0.5 * 100)
    dimension = max(100, dimension)  # Minimum 100x100
    
    # Create image with random gradient
    img = Image.new('RGB', (dimension, dimension))
    draw = ImageDraw.Draw(img)
    
    # Create colorful gradient
    for x in range(dimension):
        for y in range(dimension):
            r = int((x / dimension) * 255)
            g = int((y / dimension) * 255)
            b = int(((x + y) / (2 * dimension)) * 255)
            img.putpixel((x, y), (r, g, b))
    
    # Add some text and shapes for visual interest
    draw = ImageDraw.Draw(img)
    
    # Draw rectangles
    for i in range(10):
        x1 = random.randint(0, dimension - 50)
        y1 = random.randint(0, dimension - 50)
        x2 = x1 + random.randint(20, 50)
        y2 = y1 + random.randint(20, 50)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
    
    # Draw circles
    for i in range(10):
        x = random.randint(0, dimension - 50)
        y = random.randint(0, dimension - 50)
        r = random.randint(10, 30)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse([x, y, x + r, y + r], outline=color, width=2)
    
    # Add text with background for better visibility
    try:
        # Try to use default font
        font_size = max(30, dimension // 15)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        # Smaller font for additional info
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", max(20, dimension // 25))
    except:
        # Fallback to default font
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Main text
    main_text = f"TEST IMAGE"
    size_text = f"Target: {target_size_kb}KB"
    format_text = f"Format: {image_format}"
    dimension_text = f"{dimension} x {dimension}px"
    
    # Calculate text positions
    main_bbox = draw.textbbox((0, 0), main_text, font=font)
    main_width = main_bbox[2] - main_bbox[0]
    main_height = main_bbox[3] - main_bbox[1]
    
    # Center position for main text
    main_x = (dimension - main_width) // 2
    main_y = (dimension // 2) - main_height - 20
    
    # Draw semi-transparent background rectangle for text area
    padding = 20
    bg_top = main_y - padding
    bg_bottom = main_y + main_height + 100 + padding
    bg_left = main_x - padding - 50
    bg_right = main_x + main_width + padding + 50
    
    # Create a semi-transparent overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([bg_left, bg_top, bg_right, bg_bottom], 
                          fill=(0, 0, 0, 180))
    
    # Convert original image to RGBA and paste overlay
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Draw main text with shadow
    draw.text((main_x + 3, main_y + 3), main_text, fill=(0, 0, 0), font=font)
    draw.text((main_x, main_y), main_text, fill=(255, 255, 0), font=font)
    
    # Draw additional info below main text
    info_y = main_y + main_height + 15
    for info_text in [size_text, format_text, dimension_text]:
        info_bbox = draw.textbbox((0, 0), info_text, font=small_font)
        info_width = info_bbox[2] - info_bbox[0]
        info_x = (dimension - info_width) // 2
        
        # Shadow
        draw.text((info_x + 2, info_y + 2), info_text, fill=(0, 0, 0), font=small_font)
        # Main text
        draw.text((info_x, info_y), info_text, fill=(255, 255, 255), font=small_font)
        info_y += 25
    
    # Save with appropriate quality to achieve target size
    quality = 85
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        img.save(filename, format=image_format, quality=quality if image_format == 'JPEG' else None)
        actual_size_kb = os.path.getsize(filename) / 1024
        
        # Check if size is close enough (within 20% tolerance)
        if abs(actual_size_kb - target_size_kb) / target_size_kb < 0.3:
            break
        
        # Adjust quality or dimensions
        if actual_size_kb > target_size_kb * 1.3:
            quality = max(10, quality - 10)
        elif actual_size_kb < target_size_kb * 0.7:
            quality = min(100, quality + 10)
            dimension = int(dimension * 1.1)
            # Recreate image with new dimensions
            img = Image.new('RGB', (dimension, dimension))
            draw = ImageDraw.Draw(img)
            for x in range(dimension):
                for y in range(dimension):
                    r = int((x / dimension) * 255)
                    g = int((y / dimension) * 255)
                    b = int(((x + y) / (2 * dimension)) * 255)
                    img.putpixel((x, y), (r, g, b))
        
        attempts += 1
    
    actual_size = os.path.getsize(filename) / 1024
    print(f"✓ Created {filename}: {actual_size:.1f} KB (target: {target_size_kb} KB)")


def main():
    """Main function to generate all test images."""
    
    # Create test-images directory if it doesn't exist
    output_dir = 'test-images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}/")
    
    print("\nGenerating test images...")
    print("=" * 60)
    
    # Define images to create
    images_to_create = [
        ('sample-1kb.jpg', 1, 'JPEG'),
        ('sample-100kb.jpg', 100, 'JPEG'),
        ('sample-100kb-2.png', 100, 'PNG'),
        ('sample-1mb.png', 1024, 'PNG'),
        ('sample-5mb.jpg', 5120, 'JPEG'),
    ]
    
    # Create each image
    for filename, size_kb, format in images_to_create:
        filepath = os.path.join(output_dir, filename)
        create_image_with_size(filepath, size_kb, format)
    
    print("=" * 60)
    print("\n✅ All test images generated successfully!")
    print(f"\nImages are located in: {os.path.abspath(output_dir)}/")
    
    # List all created files
    print("\nGenerated files:")
    for file in sorted(os.listdir(output_dir)):
        if file.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(output_dir, file)
            size = os.path.getsize(filepath) / 1024
            print(f"  - {file:25s} {size:10.1f} KB")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have Pillow installed:")
        print("  pip install Pillow")
        exit(1)

