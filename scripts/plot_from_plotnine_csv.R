# ============================================================================
# Plot Combined Figure from plotnine GAM Predictions
# ============================================================================
#
# This script is Step 2 of the figure generation pipeline. It reads the fitted 
# values exported from plotnine (Step 1) and creates the final plot using ggplot2. 
# The figure matches the plotnine output exactly since it uses the same fitted values.
#
# PIPELINE STEP: 2 of 3
# INPUT:  plotnine_gam_predictions.csv (from Step 1)
#        combined_df.csv (for reference)
# OUTPUT: fig_combined_from_plotnine.png
#         fig_combined_from_plotnine.pdf (used in Step 3)
#         fig_combined_from_plotnine.svg (optional)
#
# Workflow:
# 1. Read the CSV with plotnine's fitted values
# 2. Read the original data (for reference, though not plotted)
# 3. Create the plot using geom_line with the fitted values
# 4. Apply the same styling, faceting, and colors as the original
# 5. Save as PNG, PDF, and SVG
#
# Usage:
#     Rscript plot_from_plotnine_csv.R
#
# Dependencies:
#     - ggplot2
#     - dplyr
#     - scales
#
# ============================================================================

# Load required libraries
library(ggplot2)
library(dplyr)
library(scales)  # For log tick formatting

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load configuration from config.yaml
# Handle both running from scripts/ directory and project root
if (file.exists("load_config.R")) {
  source("load_config.R")
} else if (file.exists("scripts/load_config.R")) {
  source("scripts/load_config.R")
} else {
  stop("Cannot find load_config.R. Please run from project root or scripts/ directory.")
}

# Define color_var names (these must match the data)
# Colors are loaded from config.yaml via load_config.R
ALL_COLOR_VARS <- c(
  "All Keypoints JABS Window",
  "All Keypoints FFT Window", 
  "All Keypoints JAABA Window",
  "Segmentation JABS Window",
  "Segmentation FFT Window",
  "Segmentation JAABA Window",
  "All Keypoints",
  "MARS Keypoints",
  "MoSeq Keypoints",
  "Mouse Resource",
  "No Ears",
  "No Nose or Tail",
  "No Paws",
  "No Tail",
  "Nose and Base Tail",
  "Nose and Paws"
)

# ALL_PLOT_COLORS is defined in load_config.R from config.yaml

# ============================================================================
# MAIN SCRIPT
# ============================================================================

cat("=", rep("=", 68), "\n", sep = "")
cat("Creating figure from plotnine GAM predictions\n")
cat("=", rep("=", 68), "\n\n", sep = "")

# Step 1: Read the plotnine GAM predictions
cat("1. Reading plotnine GAM predictions from", PREDICTIONS_FILE, "...\n")
predictions_df <- read.csv(PREDICTIONS_FILE)
cat("   Loaded", nrow(predictions_df), "prediction points\n")
cat("   Groups:", paste(unique(predictions_df$plot_group), collapse = ", "), "\n")
cat("   Variables:", paste(unique(predictions_df$variable), collapse = ", "), "\n\n")

# Set factor levels to control plot order (from config.yaml)
predictions_df$plot_group <- factor(predictions_df$plot_group, 
                                     levels = PLOT_GROUP_ORDER)

# Step 2: Read the original data (for reference, though not plotted in final figure)
cat("2. Reading original data from", DATA_FILE, "...\n")
combined_df <- read.csv(DATA_FILE)
cat("   Loaded", nrow(combined_df), "data points\n\n")

# Set factor levels for original data as well (for consistency)
combined_df$plot_group <- factor(combined_df$plot_group, 
                                 levels = PLOT_GROUP_ORDER)

# Step 3: Create the plot
cat("3. Creating plot...\n")
plot <- ggplot(combined_df, aes(x = train_label_size, y = value, color = color_var, group = color_var)) +
  # Plot the exported plotnine GAM fits as lines
  # These are the exact fitted values from plotnine's geom_smooth
  geom_line(data = predictions_df, 
            aes(x = train_label_size, y = predicted, color = color_var, group = color_var), 
            linewidth = LINE_WIDTH) +
  
  # Facet by plot_group (rows) and variable (columns)
  # This creates the three panels (A, B, C) and three metrics
  facet_grid(plot_group ~ variable, scales = "free_y") +
  
  # Y-axis: performance metrics from 0.4 to 1.0
  scale_y_continuous(breaks = seq(0.4, 1.0, 0.2), limits = c(0.4, 1.0)) +
  
  # X-axis: log scale for dataset size
  # Use minor_breaks to create log-spaced grid lines
  scale_x_log10(breaks = c(1e4, 1e5, 1e6),
                labels = expression(10^4, 10^5, 10^6),
                minor_breaks = c(seq(1e4, 1e5, by = 1e4), 
                                 seq(1e5, 1e6, by = 1e5))) +
  
  # Add log tick marks on x-axis
  annotation_logticks(sides = "b") +
  
  # Apply color palette (colors from config.yaml via load_config.R)
  # ALL_PLOT_COLORS from load_config.R contains hex codes in correct order
  # ALL_COLOR_VARS (names) from this script matches the order
  scale_color_manual(values = setNames(ALL_PLOT_COLORS, ALL_COLOR_VARS)) +
  
  # Theme: black and white with clean styling (all settings from config)
  theme_bw(base_size = FONT_BASE_SIZE) +
  theme(
    legend.position = if(SHOW_LEGEND) "right" else "none", # Legend from config
    axis.text = element_text(size = FONT_AXIS_TEXT), # Axis tick labels from config
    axis.title = element_text(size = FONT_AXIS_TITLE), # Axis titles from config
    strip.text = element_text(size = FONT_STRIP_TEXT), # Facet labels from config
    # Ensure grid lines respect log scale on x-axis
    panel.grid.major.x = element_line(color = "grey90", linewidth = 0.5),
    panel.grid.minor.x = element_line(color = "grey95", linewidth = 0.25),
    panel.grid.major.y = element_line(color = "grey90", linewidth = 0.5),
    panel.grid.minor.y = element_blank()
  ) +
  
  # Labels
  labs(x = "Annotation Dataset Size", y = "")

# Step 4: Save the plot
cat("\n4. Saving plot...\n")

# Save as PNG
ggsave(
  OUTPUT_PNG, 
  plot = plot, 
  width = FIGURE_WIDTH, 
  height = FIGURE_HEIGHT,
  units = "in",
  dpi = FIGURE_DPI
)
cat("   ✓ Saved PNG:", OUTPUT_PNG, "\n")

# Save as PDF
ggsave(
  OUTPUT_PDF, 
  plot = plot, 
  width = FIGURE_WIDTH, 
  height = FIGURE_HEIGHT,
  units = "in"
)
cat("   ✓ Saved PDF:", OUTPUT_PDF, "\n")

# Try to save as SVG (requires svglite package)
tryCatch({
  ggsave(
    OUTPUT_SVG, 
    plot = plot, 
    width = FIGURE_WIDTH, 
    height = FIGURE_HEIGHT,
    units = "in"
  )
  cat("   ✓ Saved SVG:", OUTPUT_SVG, "\n")
}, error = function(e) {
  cat("   ⚠ SVG not saved (install svglite package for SVG support)\n")
})

cat("\n", "=", rep("=", 68), "\n", sep = "")
cat("Figure generation complete!\n")
cat("=", rep("=", 68), "\n", sep = "")
