import pandas as pd
from fpdf import FPDF

# Functie voor het inleiden van het Excel bestand
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        print(f"Bestand {file_path} succesvol ingelezen.")
        return df
    except Exception as e:
        print(f"Fout bij het inlezen van het bestand: {e}")
        return None

# Bestandspad van het Excel bestand om in te lezen
input_file_path = 'Excel storage\Solar_Data_2022_to_Today.xlsx'  # Vul hier het volledige bestandspad in

# Inleiden van de data uit het opgegeven bestand
df = read_excel_file(input_file_path)

# Controleer of het bestand succesvol is ingelezen
if df is not None:
    # Zorg ervoor dat de kolommen 'validfrom' en 'validto' in datetime-formaat zijn
    df['validfrom'] = pd.to_datetime(df['validfrom'], errors='coerce')
    df['validto'] = pd.to_datetime(df['validto'], errors='coerce')
    
    # Verwijder eventuele tijdzone-informatie van de datums (tijdzone-onafhankelijk maken)
    df['validfrom'] = df['validfrom'].dt.tz_localize(None)
    df['validto'] = df['validto'].dt.tz_localize(None)
    
    # Bepaal de startdatum (minimale datum) van het bestand en de einddatum (vandaag)
    start_date = df['validfrom'].min()
    today = pd.to_datetime('today')

    # Functie om de data op te schonen
    def clean_data(df, start_date, today):
        # Completeness (Volledigheid): Vul missende waarden in
        df.fillna({
            'classification': 2,  # Default geldige classificatie
            'granularity': 5,  # Default geldige granulariteit
            'activity': 1,  # Default activiteit
        }, inplace=True)

        # Vul missende tijdstempels met logische waarden (bijvoorbeeld min/max van de kolom)
        if 'validfrom' in df.columns:
            df['validfrom'].fillna(df['validfrom'].min(), inplace=True)
        if 'validto' in df.columns:
            df['validto'].fillna(df['validto'].max(), inplace=True)

        # Uniqueness (Uniciteit): Verwijder duplicaten
        df.drop_duplicates(inplace=True)

        # Timeliness (Actualiteit): Filter rijen buiten de gewenste datumbereik
        df = df[(df['validfrom'] >= start_date) & (df['validfrom'] <= today)]

        # Validity (Validiteit): Filter of corrigeer ongeldige waarden
        valid_classifications = [1, 2, 3]
        valid_granularities = [3, 4, 5, 6, 7, 8]
        valid_activities = [1, 2]

        df = df[df['classification'].isin(valid_classifications)]
        df = df[df['granularity'].isin(valid_granularities)]
        df = df[df['activity'].isin(valid_activities)]

        # Consistency (Consistentie): Corrigeer validto minder dan validfrom
        df.loc[df['validto'] < df['validfrom'], 'validto'] = df['validfrom'] + pd.Timedelta(hours=1)

        return df

    # Pas de opschoning toe op de ingelezen data
    df_cleaned = clean_data(df, start_date, today)

    # Controleer of de data is opgeschoond
    print(f"Na opschoning zijn er {df_cleaned.shape[0]} rijen over.")

    # Opslaan van de opgeschoonde data in een nieuw Excel-bestand
    excel_file_name = "cleaned_data_solar.xlsx"  # Nieuwe output bestandsnaam
    df_cleaned.to_excel(excel_file_name, index=False)
    print(f"Opgeschoonde data opgeslagen als {excel_file_name}")
    
    # Genereer PDF-rapport
    def generate_pdf_report(df):
        # Initialiseer de PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Titel van het rapport
        title = input_file_path
        pdf.cell(200, 10, txt=title, ln=True, align='C')
        pdf.ln(10)

        # Data kwaliteit dimensies
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

        # Bereken data kwaliteit statistieken
        completeness = df.isnull().sum().sum()
        uniqueness = df.duplicated().sum()
        timeliness = df[df['validfrom'] < start_date].shape[0]
        validity = df.shape[0] - df[df['classification'].isin([1, 2, 3])].shape[0]
        consistency = df[df['validto'] < df['validfrom']].shape[0]

        # Voeg resultaten toe aan de PDF
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(60, 10, 'Data Dimension', border=1, align='C')
        pdf.cell(100, 10, 'Check Result', border=1, align='C')
        pdf.ln(10)

        # Resultaten voor elke dimensie
        pdf.set_font("Arial", size=12)
        pdf.cell(60, 10, "Volledigheid", border=1, align='L')
        pdf.cell(100, 10, f"{completeness} missing values", border=1, align='L')
        pdf.ln(10)

        pdf.cell(60, 10, "Uniciteit", border=1, align='L')
        pdf.cell(100, 10, f"{uniqueness} duplicate rows", border=1, align='L')
        pdf.ln(10)

        pdf.cell(60, 10, "Actualiteit", border=1, align='L')
        pdf.cell(100, 10, f"{timeliness} outdated rows", border=1, align='L')
        pdf.ln(10)

        pdf.cell(60, 10, "Validiteit", border=1, align='L')
        pdf.cell(100, 10, f"{validity} invalid classifications", border=1, align='L')
        pdf.ln(10)

        pdf.cell(60, 10, "Consistentie", border=1, align='L')
        pdf.cell(100, 10, f"{consistency} inconsistent rows (validto < validfrom)", border=1, align='L')
        pdf.ln(10)

        # Bestandsnaam voor het PDF-rapport
        pdf_file_name = "Solar_data_quality_report.pdf"
        pdf.output(pdf_file_name)
        print(f"PDF-rapport opgeslagen als {pdf_file_name}")

    # Genereer en sla het PDF-rapport op
    generate_pdf_report(df_cleaned)

else:
    print("Geen geldige data gevonden. Zorg ervoor dat het bestand goed is en probeer opnieuw.")
