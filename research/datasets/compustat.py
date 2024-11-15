import os
import gdown
import pandas as pd
from research.datasets.config import DATA_DIR
from research.datasets.dataset import Dataset

RAW_FILE_PATH = DATA_DIR + "/compustat_quarterly_raw.csv"
CLEAN_FILE_PATH = DATA_DIR + "/compustat_quarterly_clean.parquet"


class COMPUSTAT(Dataset):
    """
    Quarterly COMPUSTAT dataset. This class handles the downloading, and cleaning in order to improve the reproducibility of our research.
    """

    def __init__(
        self, RAW_FILE_PATH=RAW_FILE_PATH, CLEAN_FILE_PATH=CLEAN_FILE_PATH
    ) -> None:
        super().__init__(RAW_FILE_PATH, CLEAN_FILE_PATH)

    def download(self):
        file_id = "1GFBzQJKyU4toHRliYtH3yAswAaG9whCd"
        url = f"https://drive.google.com/uc?id={file_id}"

        gdown.download(url, RAW_FILE_PATH, quiet=False)

    def clean(self):
        # Raw file
        df = pd.read_csv(RAW_FILE_PATH)

        # TODO: Add all dataframe cleaning steps

        df["cusip"] = df["cusip"].astype(str)
        df["addzip"] = df["addzip"].astype(str)

        df.to_parquet(CLEAN_FILE_PATH)
