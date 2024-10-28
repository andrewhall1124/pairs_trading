import os
import gdown
import pandas as pd

RAW_FILE_PATH = "./data/compustat_quarterly_raw.csv"
CLEAN_FILE_PATH = "./data/compustat_quarterly_clean.parquet"

class COMPUSTAT:
    """
    Quarterly COMPUSTAT dataset. This class handles the downloading, and cleaning in order to improve the reproducibility of our research.
    """
    def __init__(self) -> None:
        if not os.path.exists(CLEAN_FILE_PATH):

            if not os.path.exists(RAW_FILE_PATH):
                self.download_raw_compustat_quarterly_data()

            self.clean_raw_compustat_quarterly_data()
            os.remove(RAW_FILE_PATH)

        print("LOADING DATAFRAME")
        self.df = pd.read_parquet(CLEAN_FILE_PATH)
        
    def download_raw_compustat_quarterly_data(self):
        print("DOWNLOADING RAW FILE")

        file_id = '1GFBzQJKyU4toHRliYtH3yAswAaG9whCd'
        url = f'https://drive.google.com/uc?id={file_id}'

        gdown.download(url, RAW_FILE_PATH, quiet=False)

    def clean_raw_compustat_quarterly_data(self):
        print("CLEANING RAW FILE")

        # Raw file
        df = pd.read_csv(RAW_FILE_PATH)

        # TODO: Add all dataframe cleaning steps

        df['cusip'] = df['cusip'].astype(str)
        df['addzip'] = df['addzip'].astype(str)

        df.to_parquet(CLEAN_FILE_PATH)


