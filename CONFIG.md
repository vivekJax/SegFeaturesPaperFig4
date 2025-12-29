# Configuration Guide

All pipeline parameters are stored in `config.yaml`. This file is the single source of truth - edit it to customize the figure generation process.

## Quick Start

1. **Edit `config.yaml`** to customize any settings
2. **Run the pipeline**:
   ```bash
   ./scripts/run_pipeline.sh
   ```

The pipeline automatically reads from `config.yaml` and applies your changes.

## Configuration Structure

```yaml
paths:              # File paths (all relative to project root)
step1_python:       # Python script settings
step2_r:            # R script settings (plot dimensions, fonts, colors)
step3_latex:        # LaTeX document settings (panel layout, table)
pipeline:           # Pipeline execution settings
table_data:         # Table content (F1 scores, colors, icons)
```

## Common Customizations

### Change Plot Size
```yaml
step2_r:
  figure_width: 7.0   # inches
  figure_height: 8.0  # inches
  figure_dpi: 300     # resolution
```

### Change Font Sizes
```yaml
step2_r:
  font_base_size: 16      # Base font size (pt)
  font_axis_text: 14      # Axis labels (pt)
  font_axis_title: 16     # Axis titles (pt)
  font_strip_text: 14     # Facet labels (pt)
```

### Reorder Plot Groups
```yaml
step2_r:
  plot_group_order:
    - "Windows"           # First row
    - "Named Keypoints"  # Second row
    - "Other Keypoints"   # Third row
```

### Change Colors
```yaml
step2_r:
  colors:
    windows:
      - "#1f77b4"  # Change hex color code
      - "#ff7f0e"
    # ... etc
```

### Adjust Panel Layout
```yaml
step3_latex:
  panel_a:
    width_fraction: 0.60  # Panel A width (60% of page)
    height: 11.0          # Panel A height (inches)
  panel_b:
    width_fraction: 0.38  # Panel B width (38% of page)
    height: 3.0          # Panel B height (inches)
```

### Update Table F1 Scores
```yaml
table_data:
  windows:
    - name: "All Keypoints + FFT"
      f1: 0.920  # Update this value
      bold: true # Make bold or not
```

### Change Table Section Order
```yaml
step3_latex:
  table_sections:
    - "Windows"           # First section
    - "Named Keypoints"  # Second section
    - "Other Keypoints"  # Third section
```

## Script Modification Points

### Python Script (`scripts/export_plotnine_fits.py`)
- Reads: `paths.input_data`, `paths.gam_predictions`
- Reads: `step1_python.smoothing_method`, `step1_python.include_se`

### R Script (`scripts/plot_from_plotnine_csv.R`)
- Reads: All `step2_r` settings via `load_config.R`
- File paths, dimensions, fonts, colors, plot order all from config

### LaTeX Generation (`scripts/generate_latex_from_config.py`)
- Generates `combined_figure_final.tex` from `config.yaml`
- All panel dimensions, table content, colors from config

## Programmatic Access

### Python
```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Access settings
width = config['step2_r']['figure_width']
colors = config['step2_r']['colors']['windows']
```

### R
```r
library(yaml)

config <- yaml::read_yaml("config.yaml")

# Access settings
width <- config$step2_r$figure_width
colors <- config$step2_r$colors$windows
```

## Validation

Validate YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

## Configuration Schema

### Paths
- `input_data`: Path to input CSV (relative to project root)
- `gam_predictions`: Path to intermediate CSV output
- `plot_pdf/png/svg`: Paths to plot outputs
- `final_figure`: Path to final combined figure

### Step 2 R Settings
- `figure_width/height`: Plot dimensions in inches
- `figure_dpi`: Resolution for raster outputs
- `font_*`: Font sizes in points
- `line_width`: Line width for plot lines
- `show_legend`: Boolean to show/hide legend
- `plot_group_order`: Array of plot group names
- `colors`: Nested structure with hex color codes

### Step 3 LaTeX Settings
- `panel_a/b`: Panel dimensions and styling
- `table_sections`: Order of table sections
- `table_colors`: Header and row background colors
- `page`: Page geometry (width, height, margin)
- `table_data`: Complete table content (name, color, icon, f1, bold)

## Data Format Requirements

### Input Data (`data/combined_df.csv`)
Required columns:
- `train_label_size`: Numeric, training dataset size
- `value`: Numeric, performance metric value
- `color_var`: String, feature set name (determines color)
- `variable`: String, metric type ("Precision", "Recall", "F1-score")
- `plot_group`: String, panel category ("Windows", "Named Keypoints", "Other Keypoints")

### Intermediate Data (`data/plotnine_gam_predictions.csv`)
Required columns:
- `train_label_size`: Numeric, x-axis values
- `predicted`: Numeric, fitted y-axis values
- `color_var`: String, feature set name
- `variable`: String, metric type
- `plot_group`: String, panel category

## Examples

### Example 1: Make Plot Larger
```yaml
step2_r:
  figure_width: 8.0
  figure_height: 10.0
```

### Example 2: Increase All Font Sizes
```yaml
step2_r:
  font_base_size: 18
  font_axis_text: 16
  font_axis_title: 18
  font_strip_text: 16
```

### Example 3: Swap Plot Group Order
```yaml
step2_r:
  plot_group_order:
    - "Other Keypoints"
    - "Named Keypoints"
    - "Windows"
```

### Example 4: Update Single F1 Score
```yaml
table_data:
  windows:
    - name: "All Keypoints + FFT"
      f1: 0.925  # Updated from 0.917
```

### Example 5: Make Plot Panel Wider
```yaml
step3_latex:
  panel_a:
    width_fraction: 0.65  # Increased from 0.55
  panel_b:
    width_fraction: 0.33  # Decreased from 0.43
```

