#!/usr/bin/env python3
"""
Export plotnine GAM fitted values to CSV

This script is Step 1 of the figure generation pipeline. It uses plotnine's 
geom_smooth with method='auto' (which uses GAM for larger datasets) to fit smooth 
curves to the data. It then extracts the exact fitted values that plotnine computes 
and exports them to CSV for use in R.

PIPELINE STEP: 1 of 3
INPUT:  combined_df.csv
OUTPUT: plotnine_gam_predictions.csv

The approach:
1. For each combination of plot_group, variable, and color_var:
   - Create a plotnine plot with geom_smooth
   - Draw the plot (which computes the smooth line)
   - Extract the line data from matplotlib
   - Convert log-scale x values back to original scale
2. Combine all predictions and export to CSV

Usage:
    source venv/bin/activate
    python export_plotnine_fits.py

Dependencies:
    - pandas
    - numpy
    - plotnine
    - matplotlib
    See requirements.txt for full list
"""

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import warnings
import yaml
import os
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load configuration from config.yaml
CONFIG_FILE = "../config.yaml"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    DATA_FILE = config['paths']['input_data']
    OUTPUT_FILE = config['paths']['gam_predictions']
    SMOOTHING_METHOD = config['step1_python']['smoothing_method']
    INCLUDE_SE = config['step1_python']['include_se']
else:
    # Fallback to defaults if config.yaml not found
    DATA_FILE = "../data/combined_df.csv"
    OUTPUT_FILE = "../data/plotnine_gam_predictions.csv"
    SMOOTHING_METHOD = "auto"
    INCLUDE_SE = False

# Define color palette for the different feature sets
# These are ordered to match the color_var categories
ALL_COLOR_VARS = [
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
]

# Create a color palette with distinct colors
ALL_PLOT_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c",  # JABS, FFT, JAABA for All Keypoints
    "#d62728", "#9467bd", "#8c564b",  # JABS, FFT, JAABA for Segmentation
    "#e377c2", "#7f7f7f", "#bcbd22",  # All Keypoints, MARS, MoSeq
    "#17becf", "#aec7e8", "#ffbb78",  # Mouse Resource, No Ears, No Nose or Tail
    "#98df8a", "#ff9896", "#c5b0d5",  # No Paws, No Tail, Nose and Base Tail
    "#c49c94"                          # Nose and Paws
]

# Y-axis limits (for filtering predictions)
Y_MIN = 0.4
Y_MAX = 1.0

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def extract_smooth_data(subset_data, color_var, variable, plot_group):
    """
    Extract smooth line data from plotnine for a single data subset.
    
    Parameters:
    -----------
    subset_data : DataFrame
        Data for one combination of plot_group, variable, and color_var
    color_var : str
        Feature set name (for labeling)
    variable : str
        Metric name (Precision, Recall, F1-score)
    plot_group : str
        Panel name (Windows, Named Keypoints, Other Keypoints)
    
    Returns:
    --------
    DataFrame with columns: train_label_size, predicted, color_var, variable, plot_group
    or None if extraction fails
    """
    if len(subset_data) < 3:
        return None
    
    try:
        # Create plotnine plot with geom_smooth (same as Old_Python_Code.txt)
        # This uses GAM smoothing for larger datasets
        p = (ggplot(subset_data, aes(x='train_label_size', y='value'))
             + geom_smooth(alpha=0, method='auto', se=False)
             + scale_x_log10()
             + scale_y_continuous(limits=(Y_MIN, Y_MAX)))
        
        # Draw the plot to compute the smooth line
        fig = p.draw()
        
        # Extract line data from matplotlib
        if len(fig.axes) > 0:
            ax = fig.axes[0]
            lines = ax.get_lines()
            
            for line in lines:
                x_data = line.get_xdata()
                y_data = line.get_ydata()
                
                if len(x_data) > 0 and len(y_data) > 0:
                    # Filter to valid y range
                    valid_mask = (y_data >= Y_MIN) & (y_data <= Y_MAX)
                    
                    if valid_mask.sum() > 0:
                        # Convert x_data back from log scale to original scale
                        # matplotlib stores log-transformed values when using scale_x_log10
                        x_original = 10**x_data[valid_mask]
                        
                        pred_df = pd.DataFrame({
                            'train_label_size': x_original,
                            'predicted': y_data[valid_mask],
                            'color_var': color_var,
                            'variable': variable,
                            'plot_group': plot_group
                        })
                        
                        # Close figure to free memory
                        plt.close(fig)
                        return pred_df
        
        plt.close(fig)
        return None
        
    except Exception as e:
        print(f"  ✗ Error for {plot_group}, {variable}, {color_var}: {e}")
        return None


def main():
    """Main function to export plotnine GAM fits."""
    print("=" * 70)
    print("Exporting plotnine GAM fitted values")
    print("=" * 70)
    
    # Read the data
    print(f"\n1. Reading data from {DATA_FILE}...")
    combined_df = pd.read_csv(DATA_FILE)
    print(f"   Loaded {len(combined_df)} data points")
    
    # Extract fitted values group by group
    print("\n2. Extracting smooth line data from plotnine (group by group)...")
    all_predictions = []
    all_plot_groups = combined_df['plot_group'].unique()
    
    total_combinations = 0
    successful = 0
    
    for group in all_plot_groups:
        group_data = combined_df[combined_df['plot_group'] == group].copy()
        unique_vars = group_data['variable'].unique()
        unique_colors = group_data['color_var'].unique()
        
        for var in unique_vars:
            for color in unique_colors:
                total_combinations += 1
                
                subset_data = group_data[
                    (group_data['variable'] == var) & 
                    (group_data['color_var'] == color)
                ].copy()
                
                pred_df = extract_smooth_data(subset_data, color, var, group)
                
                if pred_df is not None:
                    all_predictions.append(pred_df)
                    successful += 1
                    print(f"   ✓ {group}, {var}, {color}: {len(pred_df)} points")
    
    print(f"\n   Extracted {successful}/{total_combinations} combinations")
    
    # Combine all predictions
    print("\n3. Combining and processing predictions...")
    if all_predictions:
        predictions_df = pd.concat(all_predictions, ignore_index=True)
        
        # Remove duplicates and sort
        predictions_df = predictions_df.drop_duplicates().sort_values(
            ['plot_group', 'variable', 'color_var', 'train_label_size']
        )
        
        # Save to CSV
        print(f"\n4. Saving to {OUTPUT_FILE}...")
        predictions_df.to_csv(OUTPUT_FILE, index=False)
        
        print(f"\n✓ Successfully exported {len(predictions_df)} prediction points")
        print(f"  Columns: {list(predictions_df.columns)}")
        print(f"  Groups: {sorted(predictions_df['plot_group'].unique().tolist())}")
        print(f"  Variables: {sorted(predictions_df['variable'].unique().tolist())}")
        print(f"  File size: {OUTPUT_FILE}")
        
        print(f"\n" + "=" * 70)
        print("Export complete!")
        print("=" * 70)
        
    else:
        print("\n✗ No predictions extracted!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
