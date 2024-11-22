import requests
import datetime
import pandas as pd
from fpdf import FPDF

# API configuration
url = "https://api.ned.nl/v1/utilizations"
headers = {
    'X-AUTH-TOKEN': '9c99896102ff51d3bf69eca8796b63e2e0a10b9f9e316645e3b80194d041b4a7',
    'accept': 'application/ld+json'
}

# Date range for data retrieval
today = datetime.date.today()
last_week = today - datetime.timedelta(days=10)

# API parameters
points = [0, 36]  # For the Netherlands and offshore
types = [1]  # Wind (change this to 2 for Solar)
activities = [1]  # Providing
classifications = [2]  # Forecast
granularities = [5]  # Hourly data
granularity_timezones = [0, 1]  # All timezones

# Energy source name based on the type
energy_type_names = {
    1: "Wind",
    2: "Solar",
    17: "Offshore Wind"
}

# Determine the energy source name
energy_type_name = [energy_type_names.get(energy, "Unknown") for energy in types]

# Collect data
all_data = []

for point in points:
    for energy_type in types:
        for activity in activities:
            for classification in classifications:
                for granularity in granularities:
                    for timezone in granularity_timezones:
                        params = {
                            'point': point,
                            'type': energy_type,
                            'activity': activity,
                            'granularity': granularity,
                            'granularitytimezone': timezone,
                            'classification': classification,
                            'validfrom[after]': str(last_week),
                            'validfrom[strictly_before]': str(today)
                        }

                        response = requests.get(url, headers=headers, params=params)
                        print(f"Status code: {response.status_code}")
                        data = response.json()

                        if data.get('hydra:totalItems', 0) > 0:
                            for item in data['hydra:member']:
                                item['point'] = point
                                item['type'] = energy_type
                                item['activity'] = activity
                                item['classification'] = classification
                                item['granularity'] = granularity
                                item['timezone'] = timezone

                                all_data.append(item)

print(f"Aantal rijen verzameld: {len(all_data)}")

# Data quality checks
quality_checks = []

if all_data:
    df = pd.DataFrame(all_data)

    # Completeness (Volledigheid) - Missing Values
    missing_values = df.isnull().sum().sum()
    missing_per_column = df.isnull().sum()

    # Uniqueness (Uniciteit) - Duplicate Rows
    duplicate_rows = df.duplicated().sum()

    # Timeliness (Actualiteit) - Check if validfrom is up-to-date
    outdated_data = df[df['validfrom'] < str(last_week)].shape[0]

    # Validity (Validiteit) - Check for valid classification, granularity, activity
    valid_classifications = df['classification'].isin([1, 2, 3]).sum()
    invalid_classifications = df.shape[0] - valid_classifications

    valid_granularities = df['granularity'].isin([3, 4, 5, 6, 7, 8]).sum()
    invalid_granularities = df.shape[0] - valid_granularities

    valid_activities = df['activity'].isin([1, 2]).sum()
    invalid_activities = df.shape[0] - valid_activities

    # Consistency (Consistentie) - Check validto > validfrom
    df['validfrom'] = pd.to_datetime(df['validfrom'])
    df['validto'] = pd.to_datetime(df['validto'])
    consistency_issues = df[df['validto'] < df['validfrom']].shape[0]

    # Prepare the results for the PDF
    quality_checks.append({
        "Volledigheid (Completeness)": f"{missing_values} missing values",
        "Uniciteit (Uniqueness)": f"{duplicate_rows} duplicate rows",
        "Actualiteit (Timeliness)": f"{outdated_data} outdated rows",
        "Validiteit (Validity)": f"Invalid classifications: {invalid_classifications}, Invalid granularities: {invalid_granularities}, Invalid activities: {invalid_activities}",
        "Nauwkeurigheid (Accuracy)": "Not applicable (accuracy cannot be verified without external reference data)",
        "Consistentie (Consistency)": f"{consistency_issues} rows with invalid validto > validfrom"
    })

    # Ensure timezone-unaware datetimes before saving to Excel
    df['validfrom'] = df['validfrom'].dt.tz_localize(None)
    df['validto'] = df['validto'].dt.tz_localize(None)

# Generate PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Dynamic title based on energy source
title = f"{energy_type_name[0]} Energy Data Quality Report"
pdf.cell(200, 10, txt=title, ln=True, align='C')
pdf.ln(10)

# Overview of checks
pdf.set_font("Arial", style='B', size=12)
pdf.cell(200, 10, txt="Overview of Data Quality Dimensions", ln=True, align='L')
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="""
1. **Volledigheid (Completeness)**: Checks for missing values in the dataset.
2. **Uniciteit (Uniqueness)**: Identifies duplicate rows in the dataset.
3. **Actualiteit (Timeliness)**: Verifies if the data is up-to-date and within the correct date range.
4. **Validiteit (Validity)**: Checks if the data conforms to predefined valid values for classification, granularity, and activity.
5. **Nauwkeurigheid (Accuracy)**: Assumes high accuracy if no obvious data errors are found.
6. **Consistentie (Consistency)**: Ensures temporal consistency between `validfrom` and `validto`.
""")
pdf.ln(10)

# Numeric statistics table
pdf.set_font("Arial", style='B', size=12)
pdf.cell(60, 10, 'Data Dimension', border=1, align='C')
pdf.cell(100, 10, 'Check Result', border=1, align='C')
pdf.ln(10)

# Add quality check results to the PDF
pdf.set_font("Arial", size=12)
for dimension, result in quality_checks[0].items():
    pdf.cell(60, 10, dimension, border=1, align='L')
    pdf.multi_cell(100, 10, result, border=1, align='L')  # Use multi_cell for wrapping text
    pdf.ln(10)

# Save the PDF
pdf_file_name = "data_quality_report.pdf"
pdf.output(pdf_file_name)
print(f"PDF report saved as {pdf_file_name}")

# Save data to Excel
if all_data:
    excel_file_name = "energy_data.xlsx"
    df.to_excel(excel_file_name, index=False)
    print(f"Data saved as {excel_file_name}")
else:
    print("No data to save.")
