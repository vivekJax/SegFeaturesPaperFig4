#!/usr/bin/env python3
"""
Download Computer Modern fonts from CTAN and install them on macOS
"""
import urllib.request
import ssl
import re
import os
import shutil

# Create SSL context that doesn't verify certificates (for CTAN)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Base URL
base_url = "https://ctan.org/tex-archive/fonts/cm/ps-type1/bakoma/otf"
fonts_dir = os.path.expanduser("~/Library/Fonts")

def get_font_list():
    """Get list of OTF files from CTAN directory"""
    print("Fetching directory listing...")
    try:
        req = urllib.request.Request(base_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        # Save HTML for debugging (optional)
        # with open('ctan_debug.html', 'w') as f:
        #     f.write(html)
        
        # Try multiple patterns to find .otf files
        patterns = [
            r'href="([^"]+\.otf)"',           # Standard href
            r'href=\'([^\']+\.otf)\'',        # Single quotes
            r'<a[^>]+href="([^"]+\.otf)"',    # Anchor tag with href
            r'<a[^>]+href=\'([^\']+\.otf)\'', # Anchor tag with single quotes
        ]
        
        files = set()
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            files.update(matches)
        
        # Also try to find any .otf filename in the HTML
        all_otf = re.findall(r'([a-zA-Z0-9_\-]+\.otf)', html, re.IGNORECASE)
        files.update(all_otf)
        
        # Filter out any that don't look like font filenames
        font_files = [f for f in files if f.endswith('.otf') and not f.startswith('http') and '/' not in f]
        
        if font_files:
            print(f"Found {len(font_files)} fonts in directory listing")
            return sorted(font_files)
        
        return []
    except Exception as e:
        print(f"Error fetching directory listing: {e}")
        return []

def download_font(filename):
    """Download a single font file"""
    url = f"{base_url}/{filename}"
    local_path = os.path.join(fonts_dir, filename)
    
    # Skip if already exists
    if os.path.exists(local_path):
        print(f"  ✓ {filename} (already exists)")
        return True
    
    try:
        print(f"  Downloading {filename}...")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            with open(local_path, 'wb') as f:
                f.write(response.read())
        print(f"  ✓ {filename}")
        return True
    except Exception as e:
        print(f"  ✗ {filename}: {e}")
        return False

def main():
    # Create fonts directory if it doesn't exist
    os.makedirs(fonts_dir, exist_ok=True)
    print(f"Fonts will be installed to: {fonts_dir}\n")
    
    # Get list of fonts
    font_files = get_font_list()
    
    if not font_files:
        print("No fonts found in directory listing. Trying comprehensive Computer Modern font list...")
        # Comprehensive list of Computer Modern fonts
        font_files = [
            # Roman (cmr)
            "cmr5.otf", "cmr6.otf", "cmr7.otf", "cmr8.otf", "cmr9.otf",
            "cmr10.otf", "cmr12.otf", "cmr17.otf",
            # Sans Serif (cmss)
            "cmss8.otf", "cmss9.otf", "cmss10.otf", "cmss12.otf", "cmss17.otf",
            # Typewriter (cmtt)
            "cmtt8.otf", "cmtt9.otf", "cmtt10.otf", "cmtt12.otf",
            # Bold Extended (cmbx)
            "cmbx5.otf", "cmbx6.otf", "cmbx7.otf", "cmbx8.otf", "cmbx9.otf",
            "cmbx10.otf", "cmbx12.otf", "cmbx17.otf",
            # Italic (cmti)
            "cmti7.otf", "cmti8.otf", "cmti9.otf", "cmti10.otf", "cmti12.otf",
            # Slanted (cmsl)
            "cmsl8.otf", "cmsl9.otf", "cmsl10.otf", "cmsl12.otf",
            # Bold Italic (cmbxti)
            "cmbxti10.otf",
            # Small Caps (cmcsc)
            "cmcsc10.otf",
            # Unslanted Italic (cmu)
            "cmu10.otf",
        ]
    
    print(f"Found {len(font_files)} font files to download\n")
    
    # Download all fonts
    success_count = 0
    for font_file in font_files:
        if download_font(font_file):
            success_count += 1
    
    print(f"\n✓ Successfully installed {success_count}/{len(font_files)} fonts")
    print(f"Fonts are now available in: {fonts_dir}")

if __name__ == "__main__":
    main()

