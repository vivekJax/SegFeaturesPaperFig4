# Load required libraries
library(ggplot2)
library(dplyr)
library(scales)  # For log tick formatting

# Read the data
combined_df <- read.csv("combined_df.csv")

# Define color palette for the different feature sets
# These are ordered to match the color_var categories
all_color_vars <- c(
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

# Create a color palette with distinct colors
all_plot_colors <- c(
  "#1f77b4", "#ff7f0e", "#2ca02c",  # JABS, FFT, JAABA for All Keypoints
  "#d62728", "#9467bd", "#8c564b",  # JABS, FFT, JAABA for Segmentation
  "#e377c2", "#7f7f7f", "#bcbd22",  # All Keypoints, MARS, MoSeq
  "#17becf", "#aec7e8", "#ffbb78",  # Mouse Resource, No Ears, No Nose or Tail
  "#98df8a", "#ff9896", "#c5b0d5",  # No Paws, No Tail, Nose and Base Tail
  "#c49c94"                          # Nose and Paws
)

# Prepare GLM predictions for all panels (A, B, and C)
# Get all unique plot groups
all_plot_groups <- unique(combined_df$plot_group)

# Create prediction data frame for all plot groups
all_pred <- data.frame()

# Process each plot group
for (group in all_plot_groups) {
  # Filter data for this plot group
  group_data <- combined_df %>% filter(plot_group == group)
  
  # Create prediction grid for this group
  # Generate sequence of x values on log scale for smooth curves
  x_seq <- seq(min(group_data$train_label_size), max(group_data$train_label_size), length.out = 200)
  
  # Create prediction data frame for each color_var and variable combination
  group_pred <- expand.grid(
    train_label_size = x_seq,
    color_var = unique(group_data$color_var),
    variable = unique(group_data$variable),
    plot_group = group
  )
  
  # Fit GLM models and generate predictions for each group
  group_pred$predicted <- NA
  
  for (var in unique(group_data$variable)) {
    for (color in unique(group_data$color_var)) {
      # Filter data for this combination
      subset_data <- group_data %>% 
        filter(variable == var, color_var == color)
      
      if (nrow(subset_data) > 0) {
        # Fit GLM model (using log scale for x since we have log x-axis)
        # Using Gaussian family for continuous response
        model <- glm(value ~ log10(train_label_size), 
                     data = subset_data, 
                     family = gaussian)
        
        # Generate predictions
        pred_indices <- group_pred$variable == var & group_pred$color_var == color
        group_pred$predicted[pred_indices] <- predict(model, 
          newdata = data.frame(train_label_size = group_pred$train_label_size[pred_indices]))
      }
    }
  }
  
  # Combine with overall prediction data
  all_pred <- rbind(all_pred, group_pred)
}

# Create the plot
plot <- ggplot(combined_df, aes(x = train_label_size, y = value, color = color_var, group = color_var)) +
  # Use GLM for all panels (A, B, and C) - plot fitted lines
  geom_line(data = all_pred, aes(y = predicted), linewidth = 0.8) +
  # Note: If you have original_perf_combined data, uncomment and add this layer:
  # geom_point(data = original_perf_combined, aes(x = train_label_size, y = value),
  #            shape = 8, color = "black", size = 3, fill = NA) +
  facet_grid(plot_group ~ variable, scales = "free_y") +
  scale_y_continuous(breaks = seq(0.4, 1.0, 0.2), limits = c(0.4, 1.0)) +
  scale_x_log10(breaks = c(1e4, 1e5, 1e6),
                labels = expression(10^4, 10^5, 10^6)) +
  annotation_logticks(sides = "b") +
  scale_color_manual(values = setNames(all_plot_colors, all_color_vars)) +
  theme_bw() +
  labs(x = "Annotation Dataset Size", y = "", color = "Feature Set")

# Print the plot (optional)
print(plot)

# Save the plot
# Use scale = 1 for better readability, or adjust as needed
scale <- 1.0

# Save as PNG
ggsave(
  "fig_combined.png", 
  plot = plot, 
  width = 5.5 * scale, 
  height = 8 * scale,
  units = "in",
  dpi = 300
)

# Save as SVG (requires svglite package)
# Install with: install.packages("svglite")
tryCatch({
  ggsave(
    "fig_combined.svg", 
    plot = plot, 
    width = 5.5 * scale, 
    height = 8 * scale,
    units = "in"
  )
  message("Plot saved to fig_combined.svg and fig_combined.png")
}, error = function(e) {
  message("Plot saved to fig_combined.png (SVG requires svglite package)")
})

