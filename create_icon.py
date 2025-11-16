#!/usr/bin/env python3
"""
Icon Generator für myTinyDesk
Erstellt Icons in verschiedenen Formaten für alle Plattformen
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Erstellt ein einfaches PDF-Icon"""
    
    # Icon-Größen für verschiedene Plattformen
    sizes = [
        (16, 16),   # Klein
        (32, 32),   # Standard
        (48, 48),   # Mittel
        (64, 64),   # Groß
        (128, 128), # XL
        (256, 256), # XXL
    ]
    
    # Erstelle Basis-Icon (256x256)
    base_size = 256
    img = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Hintergrund (Dokument)
    margin = 30
    doc_color = (240, 240, 240)
    shadow_color = (100, 100, 100, 100)
    
    # Schatten
    draw.rectangle(
        [margin + 5, margin + 5, base_size - margin + 5, base_size - margin + 5],
        fill=shadow_color
    )
    
    # Dokument
    draw.rectangle(
        [margin, margin, base_size - margin, base_size - margin],
        fill=doc_color,
        outline=(200, 200, 200),
        width=3
    )
    
    # Eselsecke
    fold_size = 40
    points = [
        (base_size - margin, margin),
        (base_size - margin - fold_size, margin),
        (base_size - margin, margin + fold_size)
    ]
    draw.polygon(points, fill=(220, 220, 220))
    draw.line(points, fill=(200, 200, 200), width=3)
    
    # PDF Text
    try:
        # Versuche eine große Schrift zu laden
        font_size = 60
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    text = "PDF"
    
    # Text in der Mitte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (base_size - text_width) // 2
    text_y = (base_size - text_height) // 2 + 10
    
    # Text mit Schatten
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 50), font=font)
    draw.text((text_x, text_y), text, fill=(200, 50, 50), font=font)
    
    # Speichere PNG-Versionen
    print("Erstelle PNG Icons...")
    img.save('icon.png', 'PNG')
    print("  ✓ icon.png (256x256)")
    
    # Erstelle ICO für Windows (mehrere Größen)
    print("\nErstelle Windows ICO...")
    ico_images = []
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    ico_images[0].save('icon.ico', format='ICO', sizes=[s for s in sizes])
    print("  ✓ icon.ico (multi-size)")
    
    # Erstelle auch einzelne PNG-Größen für Linux
    print("\nErstelle zusätzliche PNG-Größen für Linux...")
    for size in [(48, 48), (64, 64), (128, 128)]:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        resized.save(f'icon_{size[0]}x{size[1]}.png', 'PNG')
        print(f"  ✓ icon_{size[0]}x{size[1]}.png")
    
    print("\n✅ Alle Icons erfolgreich erstellt!")
    print("\nVerwendung:")
    print("  - Linux:   icon.png oder icon_48x48.png")
    print("  - Windows: icon.ico")
    print("  - macOS:   icon.png (muss zu .icns konvertiert werden)")


if __name__ == "__main__":
    print("=" * 60)
    print("myTinyDesk Icon Generator".center(60))
    print("=" * 60)
    print()
    
    try:
        create_icon()
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        print("\nStelle sicher, dass Pillow installiert ist:")
        print("  pip install Pillow")
