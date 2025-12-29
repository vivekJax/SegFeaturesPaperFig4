#!/usr/bin/env python3
"""
Fix PostScript names in Computer Modern fonts to match LaTeX naming convention.
LaTeX uses uppercase names like CMR10, but BaKoMa fonts use lowercase like cmr10.
This script creates font copies with uppercase PostScript names.
"""
import os
import shutil
from fontTools.ttLib import TTFont

fonts_dir = os.path.expanduser("~/Library/Fonts")

# Mapping of lowercase to uppercase PostScript names
# This covers the fonts that LaTeX typically uses
font_mapping = {
    # Roman
    'cmr5': 'CMR5', 'cmr6': 'CMR6', 'cmr7': 'CMR7', 'cmr8': 'CMR8', 'cmr9': 'CMR9',
    'cmr10': 'CMR10', 'cmr12': 'CMR12', 'cmr17': 'CMR17',
    # Sans Serif
    'cmss8': 'CMSS8', 'cmss9': 'CMSS9', 'cmss10': 'CMSS10', 
    'cmss12': 'CMSS12', 'cmss17': 'CMSS17',
    # Sans Serif Bold Extended
    'cmssbx10': 'CMSSBX10',
    # Typewriter
    'cmtt8': 'CMTT8', 'cmtt9': 'CMTT9', 'cmtt10': 'CMTT10', 'cmtt12': 'CMTT12',
    # Bold Extended
    'cmbx5': 'CMBX5', 'cmbx6': 'CMBX6', 'cmbx7': 'CMBX7', 'cmbx8': 'CMBX8', 'cmbx9': 'CMBX9',
    'cmbx10': 'CMBX10', 'cmbx12': 'CMBX12',
    # Italic
    'cmti7': 'CMTI7', 'cmti8': 'CMTI8', 'cmti9': 'CMTI9', 'cmti10': 'CMTI10', 'cmti12': 'CMTI12',
    # Slanted
    'cmsl8': 'CMSL8', 'cmsl9': 'CMSL9', 'cmsl10': 'CMSL10', 'cmsl12': 'CMSL12',
    # Bold Italic
    'cmbxti10': 'CMBXTI10',
    # Small Caps
    'cmcsc10': 'CMCSC10',
    # Unslanted Italic
    'cmu10': 'CMU10',
}

def fix_font_postscript_name(font_path, new_ps_name):
    """Modify the PostScript name in a font file"""
    try:
        font = TTFont(font_path)
        
        # Update PostScript name in 'name' table (nameID 6)
        name_table = font['name']
        updated_count = 0
        for record in name_table.names:
            if record.nameID == 6:
                record.string = new_ps_name
                updated_count += 1
        if updated_count > 0:
            print(f"  Updated {updated_count} PostScript name record(s) to: {new_ps_name}")
        
        # Also update in CFF table if present (for OTF fonts)
        # This is critical for OTF fonts as many applications read from CFF
        if 'CFF ' in font:
            try:
                cff_table = font['CFF ']
                # Get the top-level font dictionary
                top_dict = cff_table.cff.topDictIndex[0]
                # Update FontName in CFF
                top_dict.FontName = new_ps_name
                print(f"  Updated CFF FontName to: {new_ps_name}")
            except Exception as e:
                print(f"  Warning: Could not update CFF table: {e}")
                # Continue anyway as name table update is also important
        
        # Save the modified font
        font.save(font_path)
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    print("Fixing PostScript names in Computer Modern fonts...\n")
    
    fixed_count = 0
    not_found = []
    
    for lowercase_name, uppercase_name in font_mapping.items():
        font_file = f"{lowercase_name}.otf"
        font_path = os.path.join(fonts_dir, font_file)
        
        if os.path.exists(font_path):
            print(f"Processing {font_file} -> {uppercase_name}...")
            if fix_font_postscript_name(font_path, uppercase_name):
                fixed_count += 1
        else:
            not_found.append(font_file)
    
    print(f"\n✓ Fixed {fixed_count} fonts")
    if not_found:
        print(f"⚠ Not found: {', '.join(not_found)}")
    print(f"\nFonts are now available with uppercase PostScript names in: {fonts_dir}")

if __name__ == "__main__":
    main()

