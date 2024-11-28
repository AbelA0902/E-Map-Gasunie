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
last_week = today - datetime.timedelta(days=365)

# API parameters
points = [0, 36]  # For the Netherlands and offshore
types = [1]  # Wind (change this to 2 for Solar)
activities = [1]  # Providing
classifications = [2]  # Forecast
granularities = [5]  # Hourly data
granularity_timezones = [0]  # UTC

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

# Initialize quality_checks as an empty list
quality_checks = []

if all_data:
    df = pd.DataFrame(all_data)

    # Convert 'validfrom' and 'validto' to datetime format
    if 'validfrom' in df.columns:
        df['validfrom'] = pd.to_datetime(df['validfrom'], errors='coerce')
    if 'validto' in df.columns:
        df['validto'] = pd.to_datetime(df['validto'], errors='coerce')

    # Completeness (Volledigheid) - Missing Values
    missing_values = df.isnull().sum().sum()

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
    consistency_issues = df[df['validto'] < df['validfrom']].shape[0]

    # Prepare the results for the PDF
    quality_checks.append({
        "Volledigheid (Completeness)": f"{missing_values} missing values",
        "Uniciteit (Uniqueness)": f"{duplicate_rows} duplicate rows",
        "Actualiteit (Timeliness)": f"{outdated_data} outdated rows",
        "Validiteit (Validity)": f"Invalid classifications: {invalid_classifications}, Invalid granularities: {invalid_granularities}, Invalid activities: {invalid_activities}",
        "Consistentie (Consistency)": f"{consistency_issues} rows with invalid validto > validfrom"
    })

    # Ensure timezone-unaware datetimes before saving to Excel
    df['validfrom'] = df['validfrom'].dt.tz_localize(None)
    df['validto'] = df['validto'].dt.tz_localize(None)

# Function to clean data
def clean_data(df, last_week):
    # Completeness (Volledigheid): Fill missing values
    df.fillna({
        'classification': 2,  # Default valid classification
        'granularity': 5,  # Default valid granularity
        'activity': 1,  # Default activity
    }, inplace=True)
    
    # Fill missing timestamps with logical values (e.g., min/max of column)
    if 'validfrom' in df.columns:
        df['validfrom'].fillna(df['validfrom'].min(), inplace=True)
    if 'validto' in df.columns:
        df['validto'].fillna(df['validto'].max(), inplace=True)
    
    # Uniqueness (Uniciteit): Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Timeliness (Actualiteit): Filter rows outside the desired date range
    df = df[(df['validfrom'] >= str(last_week)) & (df['validfrom'] < str(today))]
    
    # Validity (Validiteit): Filter or correct invalid values
    valid_classifications = [1, 2, 3]
    valid_granularities = [3, 4, 5, 6, 7, 8]
    valid_activities = [1, 2]
    
    df = df[df['classification'].isin(valid_classifications)]
    df = df[df['granularity'].isin(valid_granularities)]
    df = df[df['activity'].isin(valid_activities)]
    
    # Consistency (Consistentie): Correct validto less than validfrom
    df.loc[df['validto'] < df['validfrom'], 'validto'] = df['validfrom'] + pd.Timedelta(hours=1)
    
    return df

# Apply the cleaning function
if all_data:
    df = clean_data(df, last_week)

    # Check again after cleaning
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    outdated_data = df[df['validfrom'] < str(last_week)].shape[0]
    consistency_issues = df[df['validto'] < df['validfrom']].shape[0]
    
    print(f"Na opschoning:")
    print(f"- Missende waarden: {missing_values}")
    print(f"- Duplicaten: {duplicate_rows}")
    print(f"- Verouderde data: {outdated_data}")
    print(f"- Inconsistente validto-validfrom: {consistency_issues}")

    # Save cleaned data to Excel
    excel_file_name = f"cleaned_{energy_type_name[0].replace(' ', '_').lower()}_data.xlsx"
    df.to_excel(excel_file_name, index=False)
    print(f"Opgeschoonde data opgeslagen als {excel_file_name}")
else:
    print("Geen geldige data na opschoning.")

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
pdf.multi_cell(0, 10, txt="""\
1. **Volledigheid (Completeness)**: Checks for missing values in the dataset.
2. **Uniciteit (Uniqueness)**: Identifies duplicate rows, and checks for ID and date consistency.
3. **Actualiteit (Timeliness)**: Verifies if the data is up-to-date and within the correct date range.
4. **Validiteit (Validity)**: Checks if the data conforms to predefined valid values for classification, granularity, and activity.
5. **Consistentie (Consistency)**: Ensures temporal consistency between `validfrom` and `validto`.
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

# Dynamically set the file name based on the energy source
energy_source_for_file_name = energy_type_name[0].replace(" ", "_").lower()  # Replace spaces with underscores and make lowercase
pdf_file_name = f"{energy_source_for_file_name}_energy_report.pdf"
pdf.output(pdf_file_name)
print(f"PDF report saved as {pdf_file_name}")
