# ============================================================================
# Configuration Loader for R Scripts
# ============================================================================
# This script loads configuration from config.yaml
# Usage: source("load_config.R")
# ============================================================================

# Check if yaml package is installed
if (!require("yaml", quietly = TRUE)) {
    stop("Please install the 'yaml' package: install.packages('yaml')")
}

# Load configuration
# Try to find config.yaml relative to script location or project root
if (file.exists("../config.yaml")) {
  CONFIG_FILE <- "../config.yaml"
} else if (file.exists("config.yaml")) {
  CONFIG_FILE <- "config.yaml"
} else if (file.exists("../../config.yaml")) {
  CONFIG_FILE <- "../../config.yaml"
} else {
  stop("config.yaml not found! Please ensure it exists in the project root.")
}
if (file.exists(CONFIG_FILE)) {
    config <- yaml::read_yaml(CONFIG_FILE)
    
    # Extract paths
    PREDICTIONS_FILE <- config$paths$gam_predictions
    DATA_FILE <- config$paths$input_data
    OUTPUT_PNG <- config$paths$plot_png
    OUTPUT_SVG <- config$paths$plot_svg
    OUTPUT_PDF <- config$paths$plot_pdf
    
    # Extract Step 2 R settings
    FIGURE_WIDTH <- config$step2_r$figure_width
    FIGURE_HEIGHT <- config$step2_r$figure_height
    FIGURE_DPI <- config$step2_r$figure_dpi
    
    # Extract font sizes
    FONT_BASE_SIZE <- config$step2_r$font_base_size
    FONT_AXIS_TEXT <- config$step2_r$font_axis_text
    FONT_AXIS_TITLE <- config$step2_r$font_axis_title
    FONT_STRIP_TEXT <- config$step2_r$font_strip_text
    
    # Extract plot styling
    LINE_WIDTH <- config$step2_r$line_width
    SHOW_LEGEND <- config$step2_r$show_legend
    
    # Extract plot group order
    PLOT_GROUP_ORDER <- config$step2_r$plot_group_order
    
    # Extract colors (flatten the nested structure)
    colors_windows <- config$step2_r$colors$windows
    colors_named <- config$step2_r$colors$named_keypoints
    colors_other <- config$step2_r$colors$other_keypoints
    ALL_PLOT_COLORS <- c(colors_windows, colors_named, colors_other)
    
    # Note: ALL_PLOT_COLORS contains hex color codes in the order:
    # Windows (6 colors), Named Keypoints (4 colors), Other Keypoints (6 colors)
    # The color_var names are defined in plot_from_plotnine_csv.R and must match this order
    
    cat("Configuration loaded from config.yaml\n")
} else {
    stop("config.yaml not found! Please create it from the template.")
}

