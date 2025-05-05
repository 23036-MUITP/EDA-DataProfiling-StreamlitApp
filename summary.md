# Data Profiling & EDA App Summary

## Approach
Developed a Streamlit app for CSV analysis and comparison, focusing on modular code and modern UI. Key components:
- **app.py**: App setup, navigation, sidebar, session state.
- **welcome.py**: Login and welcome UI with green Login button.
- **analyse_data.py**: CSV upload, data editing, Plotly charts (histogram, box plot, scatter, bar, line, pie, area, heatmap, donut).
- **compare_CSVs.py**: CSV comparison with metrics and previews.
- **data_utils.py**: DataProfiler class for data processing.
Used session state for persistence, Plotly for interactive charts, and Material Icons for UI. Fixed StreamlitSetPageConfigMustBeFirstCommandError by separating Welcome page.

## Learnings
- Modular programming: Separated UI, logic, and data processing.
- Streamlit navigation: Handled nested navigation and session state.
- UI design: Implemented Manrope font, centered layout, green buttons.
- Error handling: Managed invalid inputs and edge cases.
- Version control: Used Git for clear commit history.

## Challenges
- Fixed configuration error by restructuring app.
- Ensured Material Icons reliability with CDN and Streamlit 1.39.0.
- Optimized charts by removing unused dependencies (matplotlib, seaborn).

## Features
- Login system with session state.
- CSV upload, editing, and download.
- Interactive charts with customization.
- CSV comparison with metrics and previews.
- Modern UI: Manrope font, 300px sidebar, green buttons, Material Icons.