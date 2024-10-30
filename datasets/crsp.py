import os
import gdown
import pandas as pd

RAW_FILE_PATH = "./data/crsp_monthly_raw.csv"
CLEAN_FILE_PATH = "./data/crsp_monthly_clean.parquet"

class CRSP:
    """
    Monthly dataset for CRSP. This class handles the downloading, and cleaning in order to improve the reproducibility of our research.
    """
    def __init__(self) -> None:
        if not os.path.exists(CLEAN_FILE_PATH):

            if not os.path.exists(RAW_FILE_PATH):
                self.download_raw_crsp_monthly_data()

            self.clean_raw_crsp_monthly_data()
        self.df = pd.read_parquet(CLEAN_FILE_PATH)
        
    def download_raw_crsp_monthly_data(self):
        print("DOWNLOADING RAW FILE")

        file_id = '15E7hEZdUf9nVVzlZokPVkanglF4j_Vni'
        url = f'https://drive.google.com/uc?id={file_id}'

        gdown.download(url, RAW_FILE_PATH, quiet=False)

    def clean_raw_crsp_monthly_data(self):
        print("CLEANING RAW FILE")

        # Raw file
        df = pd.read_csv(RAW_FILE_PATH)

        # Lowercase columns
        df = df.rename(columns={x: x.lower() for x in df.columns})

        # Filters
        df = df.query("10 <= shrcd <= 11") # Stocks
        df = df.query("1 <= exchcd <= 3") # NYSE, AMEX, NASDAQ

        # Keep only necessary columns
        keep_columns = ['permno', 'date', 'cusip', 'shrcd', 'exchcd', 'ticker', 'shrout', 'vol', 'prc', 'ret']
        df = df[keep_columns]

        # Fix ret and prc variables
        df = df[df['ret'] != 'C'] # Not sure what the C in the data represents (IPO?)
        df['prc'] = abs(df['prc']) # Stocks with unavailable prc data are negated (bid-ask spread)

        # Cast types
        df['cusip'] = df['cusip'].astype(str)
        df['ret'] = pd.to_numeric(df['ret'])
        df['date'] = pd.to_datetime(df['date'])

        # Sort values
        df = df.sort_values(by=['permno', 'date'])

        # Reset index
        df = df.reset_index(drop=True)

        df.to_parquet(CLEAN_FILE_PATH)


