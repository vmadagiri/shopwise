"""Download and verify the original UCI Online Retail workbook."""

from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
DATA_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
WORKBOOK_NAME = "Online Retail.xlsx"
EXPECTED_COLUMNS = {
    "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
    "UnitPrice", "CustomerID", "Country",
}


def download_workbook(force: bool = False) -> Path:
    """Download the UCI zip and extract its unchanged Excel workbook."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    workbook_path = RAW_DIR / WORKBOOK_NAME
    zip_path = RAW_DIR / "online_retail_download.zip"

    if workbook_path.exists() and not force:
        print(f"Workbook already exists: {workbook_path}")
        return workbook_path

    print("Checkpoint 1/3: Downloading the official UCI dataset archive...")
    urlretrieve(DATA_URL, zip_path)

    print("Checkpoint 2/3: Extracting the original workbook...")
    with ZipFile(zip_path) as archive:
        workbook_members = [name for name in archive.namelist() if name.lower().endswith(".xlsx")]
        if len(workbook_members) != 1:
            raise ValueError(f"Expected one Excel workbook in the archive; found {workbook_members}")
        workbook_path.write_bytes(archive.read(workbook_members[0]))
    zip_path.unlink(missing_ok=True)

    print("Checkpoint 3/3: Checking workbook structure...")
    frame = pd.read_excel(workbook_path, nrows=5)
    missing = EXPECTED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"The downloaded file is missing expected columns: {sorted(missing)}")
    print(f"Verified {len(frame.columns)} columns: {', '.join(frame.columns)}")
    print(f"Raw workbook saved without edits at: {workbook_path}")
    return workbook_path


if __name__ == "__main__":
    download_workbook()
