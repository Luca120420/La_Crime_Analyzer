# Crime Analyzer and Map Visualizer

Crime Analyzer and Map Visualizer is a Python code that provides a tool for analyzing and visualizing crime data. This code utilizes popular libraries such as pandas, matplotlib, calendar, and folium to process and visualize the data.

## Features

- **Data Retrieval**: The code includes a function to download a CSV file containing crime data from a specified URL and save it locally.
- **Data Processing**: The code reads the downloaded CSV file, cleans the data by removing irrelevant entries, and performs necessary data transformations.
- **Data Analysis**: Several analysis functions are implemented to provide insights into crime frequency, temporal patterns, victim demographics, crime status, premise and weapon distribution, and crime versus age relationships.
- **Map Visualization**: The code utilizes the folium library to plot crime locations on an interactive map using latitude and longitude coordinates.
- **Data Visualization**: The code includes functions to create various visualizations such as bar charts, histograms, and pie charts to present the analyzed crime data.

## Usage

1. Install the required dependencies.
2. Instantiate the `CrimeAnalyzer` class with the URL of the crime data CSV file and the desired path to save the downloaded file.
3. Call the `process_data()` method of the `CrimeAnalyzer` instance to download the CSV file, read and clean the data, perform data analysis, and generate visualizations.
4. The analysis results will be printed to the console, and visualizations will be displayed using matplotlib and folium.

## Example

```python
from CrimeAnalyzer import CrimeAnalyzer

# Instantiate the CrimeAnalyzer class and process the data
url = 'https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD'
path = 'data/crimes.csv'
analyzer = CrimeAnalyzer(url, path)
analyzer.process_data()
```
## Requirements
The code requires the following dependencies:

- pandas
- matplotlib
- calendar
- folium

## License
This code is licensed under the MIT License.