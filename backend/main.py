from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

from analytics.analyzer import analyze_dataset
from analytics.cleaner import clean_dataset


app = FastAPI(title="Trans Express Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Trans Express Analytics API is running!"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Check that the uploaded file is an Excel file
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Please upload an Excel file (.xlsx or .xls)"
        )

    try:
        # Read the uploaded file
        contents = await file.read()

        # Load Excel file
        excel_file = pd.ExcelFile(
            io.BytesIO(contents)
        )

        # Get sheet names
        sheet_names = excel_file.sheet_names

        # Read the first sheet
        df = pd.read_excel(
            io.BytesIO(contents),
            sheet_name=sheet_names[0]
        )

        # Basic dataset information
        rows = len(df)
        columns = len(df.columns)

        column_names = df.columns.tolist()

        # Data types
        data_types = {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }

        # Missing values
        missing_values = {
            column: int(value)
            for column, value in df.isnull().sum().items()
        }

        # Duplicate rows
        duplicate_rows = int(
            df.duplicated().sum()
        )

        return {
            "filename": file.filename,
            "sheets": sheet_names,
            "active_sheet": sheet_names[0],
            "rows": rows,
            "columns": columns,
            "column_names": column_names,
            "data_types": data_types,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):

    # Check that the uploaded file is an Excel file
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Please upload an Excel file (.xlsx or .xls)"
        )

    try:
        # Read the uploaded file
        contents = await file.read()

        # Read the first sheet
        df = pd.read_excel(
            io.BytesIO(contents),
            sheet_name=0
        )

        # Clean the dataset first
        cleaned_df = clean_dataset(df)

        # Run analytics on the cleaned dataset
        results = analyze_dataset(cleaned_df)

        records = cleaned_df.fillna("").to_dict(orient="records")
        results["records"] = records

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analysing file: {str(e)}"
        )