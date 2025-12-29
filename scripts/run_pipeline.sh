#!/bin/bash
# ============================================================================
# Complete Figure Generation Pipeline
# ============================================================================
# This script runs the complete pipeline from input data to final figure:
# Step 1: Export plotnine GAM fits (Python)
# Step 2: Generate plot from fits (R)
# Step 3: Combine plot and table (LaTeX)
# ============================================================================
# Note: This script should be run from the project root directory
# ============================================================================

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

echo "============================================================================"
echo "Figure Generation Pipeline"
echo "============================================================================"
echo ""

# Check for required input file
if [ ! -f "data/combined_df.csv" ]; then
    echo "ERROR: data/combined_df.csv not found!"
    echo "Please ensure the input data file exists."
    exit 1
fi

# Step 1: Export plotnine GAM fits
echo "STEP 1: Exporting plotnine GAM fits..."
echo "----------------------------------------------------------------------------"
cd "$SCRIPT_DIR"
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    python export_plotnine_fits.py
    deactivate
else
    echo "WARNING: venv not found, using system Python"
    python export_plotnine_fits.py
fi

if [ ! -f "$PROJECT_ROOT/data/plotnine_gam_predictions.csv" ]; then
    echo "ERROR: Step 1 failed - data/plotnine_gam_predictions.csv not created"
    exit 1
fi

echo ""
echo "STEP 2: Generating plot from fits..."
echo "----------------------------------------------------------------------------"
Rscript plot_from_plotnine_csv.R

if [ ! -f "$PROJECT_ROOT/fig_combined_from_plotnine.pdf" ]; then
    echo "ERROR: Step 2 failed - fig_combined_from_plotnine.pdf not created"
    exit 1
fi

echo ""
echo "STEP 3: Generating LaTeX from config..."
echo "----------------------------------------------------------------------------"
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    python generate_latex_from_config.py
    deactivate
else
    echo "WARNING: venv not found, using system Python"
    python generate_latex_from_config.py
fi

echo ""
echo "STEP 4: Combining plot and table..."
echo "----------------------------------------------------------------------------"
pdflatex -interaction=nonstopmode -output-directory="$PROJECT_ROOT" combined_figure_final.tex > "$PROJECT_ROOT/log/pdflatex.log" 2>&1

# Move LaTeX build artifacts to log directory
mv -f "$PROJECT_ROOT"/*.aux "$PROJECT_ROOT/log/" 2>/dev/null || true
mv -f "$PROJECT_ROOT"/*.log "$PROJECT_ROOT/log/" 2>/dev/null || true
mv -f "$PROJECT_ROOT"/*.fls "$PROJECT_ROOT/log/" 2>/dev/null || true
mv -f "$PROJECT_ROOT"/*.fdb_latexmk "$PROJECT_ROOT/log/" 2>/dev/null || true
mv -f "$PROJECT_ROOT"/*.synctex.gz "$PROJECT_ROOT/log/" 2>/dev/null || true

if [ ! -f "$PROJECT_ROOT/combined_figure_final.pdf" ]; then
    echo "ERROR: Step 3 failed - combined_figure_final.pdf not created"
    exit 1
fi

echo ""
echo "============================================================================"
echo "Pipeline complete!"
echo "============================================================================"
echo ""
echo "Output files:"
echo "  - data/plotnine_gam_predictions.csv (intermediate)"
echo "  - fig_combined_from_plotnine.pdf (plot)"
echo "  - combined_figure_final.pdf (FINAL FIGURE)"
echo ""
