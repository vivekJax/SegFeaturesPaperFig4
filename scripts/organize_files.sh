#!/bin/bash
# ============================================================================
# Organize Files Script
# ============================================================================
# Moves old files and build artifacts to old_files/ directory
# Keeps only essential files for the pipeline
# Note: Run from project root directory
# ============================================================================

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Create directories if they don't exist
mkdir -p old_files log

# Move LaTeX build artifacts to log directory
echo "Moving LaTeX build artifacts to log/..."
mv -f *.aux log/ 2>/dev/null || true
mv -f *.log log/ 2>/dev/null || true
mv -f *.fls log/ 2>/dev/null || true
mv -f *.fdb_latexmk log/ 2>/dev/null || true
mv -f *.synctex.gz log/ 2>/dev/null || true
mv -f *.out log/ 2>/dev/null || true

# Move old PDF figures
echo "Moving old PDF figures to old_files/..."
mv -f combined_figure_1.pdf old_files/ 2>/dev/null || true
mv -f combined_figure_1.txt old_files/ 2>/dev/null || true
mv -f combined_figure.pdf old_files/ 2>/dev/null || true
mv -f combined_figure.tex old_files/ 2>/dev/null || true
mv -f combined_figure5v1.pdf old_files/ 2>/dev/null || true
mv -f combined_figure_final2.0.pdf old_files/ 2>/dev/null || true
mv -f fig_combined2.pdf old_files/ 2>/dev/null || true
mv -f Rplots.pdf old_files/ 2>/dev/null || true

# Move old figure files
echo "Moving old figure files to old_files/..."
mv -f fig_combined.png old_files/ 2>/dev/null || true
mv -f fig_combined.svg old_files/ 2>/dev/null || true

# Move old scripts (if any remain in root)
echo "Moving old scripts to old_files/..."
mv -f plot_figure.R old_files/ 2>/dev/null || true
mv -f plot_figure.py old_files/ 2>/dev/null || true
mv -f Old_Python_Code.txt old_files/ 2>/dev/null || true

# Move old table files
echo "Moving old table files to old_files/..."
mv -f table.latex old_files/ 2>/dev/null || true
mv -f Template_table.tex old_files/ 2>/dev/null || true

# Move font-related files
echo "Moving font-related files to old_files/..."
mv -f download_cm_fonts.py old_files/ 2>/dev/null || true
mv -f fix_font_names.py old_files/ 2>/dev/null || true
mv -f FONT_INSTALLATION_NOTES.md old_files/ 2>/dev/null || true

echo ""
echo "File organization complete!"
echo "Essential files remain in organized directories."
echo "Old files moved to: old_files/"
echo "Log files moved to: log/"
