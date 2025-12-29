# Computer Modern Font Installation - Fixed

## What Was Done

1. **Downloaded 36 Computer Modern fonts** from CTAN (BaKoMa collection)
2. **Fixed PostScript names** from lowercase (e.g., `cmr10`) to uppercase (e.g., `CMR10`) to match LaTeX's naming convention
3. **Installed fonts** to `~/Library/Fonts/`

## Fonts Fixed

All fonts now have uppercase PostScript names that match what LaTeX PDFs expect:
- CMR5, CMR6, CMR7, CMR8, CMR9, CMR10, CMR12, CMR17
- CMSS8, CMSS9, CMSS10, CMSS12, CMSS17
- CMTT8, CMTT9, CMTT10, CMTT12
- CMBX5, CMBX6, CMBX7, CMBX8, CMBX9, CMBX10, CMBX12
- CMTI7, CMTI8, CMTI9, CMTI10, CMTI12
- CMSL8, CMSL9, CMSL10, CMSL12
- CMBXTI10
- CMCSC10
- CMU10

## Important: Clear Font Cache

macOS caches font information. After installing/modifying fonts, you may need to:

1. **Restart applications** (especially Adobe Illustrator)
2. **Clear font cache** (if needed):
   ```bash
   # Remove user font cache
   atsutil databases -removeUser
   
   # Or restart your Mac to clear system font cache
   ```

3. **Verify fonts are recognized**:
   - Open Font Book (Applications > Font Book)
   - Search for "Computer Modern" or "CMR10"
   - The fonts should appear with their uppercase PostScript names

## Testing in Adobe Illustrator

1. Close Adobe Illustrator if it's open
2. Reopen Adobe Illustrator
3. Open your PDF (`combined_figure3.pdf`)
4. The fonts should now be recognized correctly

If fonts are still missing:
- Use Illustrator's "Find Font" feature (Type > Find Font...)
- Check which fonts are marked with an asterisk (*)
- The uppercase PostScript names should now match

## Note

The font `cmssbx10.otf` (CMSSBX10) was not found on CTAN. If your PDF uses this font, you may need to find it from another source or replace it in your LaTeX document.






