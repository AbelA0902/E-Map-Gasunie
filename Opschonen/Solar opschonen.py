import pandas as pd
from fpdf import FPDF

def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        print(f"Bestand {file_path} succesvol ingelezen.")
        return df
    except Exception as e:
        print(f"Fout bij het inlezen van het bestand: {e}")
        return None

input_file_path = 'Excel storage\Solar_Data_2022_to_Today.xlsx'  


df = read_excel_file(input_file_path)

if df is not None:
    df['validfrom'] = pd.to_datetime(df['validfrom'], errors='coerce')
    df['validto'] = pd.to_datetime(df['validto'], errors='coerce')
    
    df['validfrom'] = df['validfrom'].dt.tz_localize(None)
    df['validto'] = df['validto'].dt.tz_localize(None)
    
    start_date = df['validfrom'].min()
    today = pd.to_datetime('today')

    def clean_data(df, start_date, today):
        df.fillna({
            'classification': 2,  
            'granularity': 5,  
            'activity': 1, 
        }, inplace=True)

        if 'validfrom' in df.columns:
            df['validfrom'].fillna(df['validfrom'].min(), inplace=True)
        if 'validto' in df.columns:
            df['validto'].fillna(df['validto'].max(), inplace=True)

       
        df.drop_duplicates(inplace=True)

       
        df = df[(df['validfrom'] >= start_date) & (df['validfrom'] <= today)]

        
        valid_classifications = [1, 2, 3]
        valid_granularities = [3, 4, 5, 6, 7, 8]
        valid_activities = [1, 2]

        df = df[df['classification'].isin(valid_classifications)]
        df = df[df['granularity'].isin(valid_granularities)]
        df = df[df['activity'].isin(valid_activities)]

        
        df.loc[df['validto'] < df['validfrom'], 'validto'] = df['validfrom'] + pd.Timedelta(hours=1)

        return df

   
    df_cleaned = clean_data(df, start_date, today)

    
    print(f"Na opschoning zijn er {df_cleaned.shape[0]} rijen over.")

    excel_file_name = "cleaned_data_solar.xlsx"  
    df_cleaned.to_excel(excel_file_name, index=False)
    print(f"Opgeschoonde data opgeslagen als {excel_file_name}")
    
   
    def generate_pdf_report(df):

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        title = input_file_path
        pdf.cell(200, 10, txt=title, ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="Overview of Data Quality Dimensions", ln=True, align='L')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt="""\
""")
        pdf.ln(10)

        completeness = df.isnull().sum().sum()
        uniqueness = df.duplicated().sum()
        timeliness = df[df['validfrom'] < start_date].shape[0]
        validity = df.shape[0] - df[df['classification'].isin([1, 2, 3])].shape[0]
        consistency = df[df['validto'] < df['validfrom']].shape[0]

        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(60, 10, 'Data Dimension', border=1, align='C')
        pdf.cell(100, 10, 'Check Result', border=1, align='C')
        pdf.ln(10)

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

        pdf_file_name = "Solar_data_quality_report.pdf"
        pdf.output(pdf_file_name)
        print(f"PDF-rapport opgeslagen als {pdf_file_name}")

    generate_pdf_report(df_cleaned)

else:
    print("Geen geldige data gevonden.")
