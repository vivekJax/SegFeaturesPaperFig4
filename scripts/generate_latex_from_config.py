#!/usr/bin/env python3
"""
Generate LaTeX file from config.yaml

This script reads config.yaml and generates the combined_figure_final.tex file
with all settings from the configuration file.

Usage:
    python generate_latex_from_config.py
"""

import yaml
import os

def load_config():
    """Load configuration from config.yaml"""
    config_file = "../config.yaml"
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"config.yaml not found at {config_file}")
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def format_f1_score(f1, bold=False):
    """Format F1 score for LaTeX"""
    if bold:
        return f"\\textbf{{{f1}}}"
    return str(f1)

def generate_table_rows(config):
    """Generate LaTeX table rows from config"""
    table_data = config['table_data']
    sections = config['step3_latex']['table_sections']
    color_square_size = config['step3_latex']['color_square_size']
    icon_size = config['step3_latex']['icon_size']
    row_light = config['step3_latex']['table_colors']['row_light']
    
    rows = []
    for section in sections:
        section_key = section.lower().replace(" ", "_")
        rows.append(f"                % ============================================================")
        rows.append(f"                % {section.upper()} SECTION")
        rows.append(f"                % ============================================================")
        rows.append(f"                \\multicolumn{{4}}{{l}}{{\\textit{{{section}}}}} \\\\")
        rows.append(f"                \\midrule")
        
        items = table_data.get(section_key, [])
        for i, item in enumerate(items):
            row_color = "\\rowcolor{rowlight}" if i % 2 == 0 else ""
            color_hex = item['color'].replace('#', '')
            icon_file = item['icon']
            name = item['name']
            f1 = format_f1_score(item['f1'], item.get('bold', False))
            
            rows.append(f"                {row_color}")
            rows.append(f"                \\textcolor[HTML]{{{color_hex}}}{{\\rule{{{color_square_size}}}{{{color_square_size}}}}} & \\includegraphics[width={icon_size}]{{../icons/{icon_file}}} & {name} & {f1} \\\\")
        
        if section != sections[-1]:  # Not the last section
            rows.append(f"                \\midrule")
            rows.append("")
    
    return "\n".join(rows)

def generate_latex(config):
    """Generate LaTeX document from config"""
    
    # Extract settings
    paths = config['paths']
    step3 = config['step3_latex']
    panel_a = step3['panel_a']
    panel_b = step3['panel_b']
    
    # Get horizontal offset for labels (default to 0 if not specified)
    panel_a_horizontal = panel_a.get('label_horizontal', '0cm')
    panel_b_horizontal = panel_b.get('label_horizontal', '0cm')
    page = step3['page']
    
    # Generate table rows
    table_rows = generate_table_rows(config)
    
    latex_template = f"""% ============================================================================
% LaTeX Document: Combined Figure with Plot (Panel A) and Table (Panel B)
% ============================================================================
% 
% PIPELINE STEP: 3 of 3
% INPUT:  {paths['plot_pdf']} (from Step 2)
%         {paths['icons_dir']}/ (directory with PDF icons)
% OUTPUT: {paths['final_figure']} (FINAL FIGURE)
%
% This document is AUTO-GENERATED from config.yaml
% To modify, edit config.yaml and regenerate this file
%
% Usage:
%     python generate_latex_from_config.py
%     pdflatex -output-directory=.. combined_figure_final.tex
%
% ============================================================================

\\documentclass{{article}}

% ============================================================================
% PACKAGES
% ============================================================================
\\usepackage[utf8]{{inputenc}}      % Enable UTF-8 character encoding
\\usepackage{{graphicx}}            % For including images (includegraphics)
\\usepackage{{xcolor}}              % For color definitions and text coloring
\\usepackage{{colortbl}}            % For colored table rows and cells
\\usepackage{{array}}                % Extended column types for tables
\\usepackage{{float}}                % Better float positioning (H option)
\\usepackage{{cite}}                 % Citation management
\\usepackage{{booktabs}}             % Professional table rules (toprule, midrule, etc.)
\\usepackage{{tabularx}}             % Extended table functionality
\\usepackage{{multirow}}             % Multi-row cells in tables
\\usepackage{{geometry}}             % Page layout control
\\usepackage{{subcaption}}           % Subfigures and subcaptions
\\usepackage{{adjustbox}}            % Box adjustment (scaling, alignment)

% ============================================================================
% PAGE GEOMETRY
% ============================================================================
\\geometry{{
    paperwidth={page['width']}in,             % Page width
    paperheight={page['height']}in,              % Page height
    margin={page['margin']}in,                  % Margins
    headheight=0pt,                            % No header space
    footskip=0pt                                % No footer space
}}
\\pagestyle{{empty}}                           % Remove page numbers and headers

% ============================================================================
% COLOR DEFINITIONS
% ============================================================================

% Table styling colors
\\definecolor{{headerbg}}{{HTML}}{{{step3['table_colors']['header_bg']}}}    % Header background
\\definecolor{{rowlight}}{{HTML}}{{{step3['table_colors']['row_light']}}}   % Alternating row color

% ============================================================================
% DOCUMENT BODY
% ============================================================================
\\begin{{document}}
\\thispagestyle{{empty}}                       % No page number on this page
\\setlength{{\\topskip}}{{0pt}}                % Remove top skip
\\setlength{{\\parskip}}{{0pt}}                % Remove paragraph spacing
\\vspace*{{0pt}}                                % No negative spacing to keep labels visible
\\hspace*{{-1cm}}                               % Move both panels 1cm to the left to center them
\\noindent
    % Panel A: Combined plot from R
    \\begin{{minipage}}[t]{{{panel_a['width_fraction']}\\textwidth}}
        \\vspace{{0pt}}
        \\sffamily\\hspace{{{panel_a_horizontal}}}\\textbf{{\\{panel_a['label_size']} {panel_a['label']}}}\\\\[{panel_a.get('label_spacing', '0.05cm')}]
        \\adjustbox{{width=\\textwidth,height={panel_a['height']}in,{'keepaspectratio,' if panel_a['keep_aspect_ratio'] else ''}center}}{{
            \\includegraphics[width=\\textwidth, {'keepaspectratio' if panel_a['keep_aspect_ratio'] else ''}]{{../{paths['plot_pdf']}}}%
        }}
    \\end{{minipage}}%
    \\hfill
    % Panel B: Summary table with color column
    \\begin{{minipage}}[t]{{{panel_b['width_fraction']}\\textwidth}}
        \\vspace{{0pt}}
        \\sffamily\\hspace*{{-1cm}}\\hspace{{{panel_b_horizontal}}}\\textbf{{\\{panel_b['label_size']} {panel_b['label']}}}\\\\[{panel_b.get('label_spacing', '0.05cm')}]
        
        \\hspace*{{-1cm}}                       % Move table 1cm to the left (label stays in place)
        \\adjustbox{{height={panel_b['height']}in,valign=f,center}}{{
            \\sffamily
            \\{panel_b['font_size']}
            \\renewcommand{{\\arraystretch}}{{{panel_b['row_stretch']}}}
            \\setlength{{\\tabcolsep}}{{{panel_b['col_sep']}}}
            
            % ================================================================
            % TABLE DEFINITION
            % ================================================================
            \\begin{{tabular}}{{>{{\\centering\\arraybackslash}}p{{{step3['color_square_size']}}} c l c}}
                \\toprule
                \\rowcolor{{headerbg}}
                \\textbf{{Color}} & \\textbf{{Icon}} & \\textbf{{Feature Set}} & \\textbf{{F1}} \\\\
                \\midrule
                
{table_rows}
                
                \\bottomrule
            \\end{{tabular}}%
        }}
    \\end{{minipage}}

\\end{{document}}
"""
    
    return latex_template

def main():
    """Main function"""
    print("=" * 70)
    print("Generating LaTeX from config.yaml")
    print("=" * 70)
    
    # Load config
    config = load_config()
    print("✓ Loaded config.yaml")
    
    # Generate LaTeX
    latex_content = generate_latex(config)
    print("✓ Generated LaTeX content")
    
    # Write to file
    output_file = "combined_figure_final.tex"
    with open(output_file, 'w') as f:
        f.write(latex_content)
    
    print(f"✓ Written to {output_file}")
    print("=" * 70)
    print("Done! You can now compile with:")
    print(f"  pdflatex -output-directory=.. {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()

