import pandas as pd

from analytics.cleaner import clean_dataset


# ---------------------------------------------------------
# Load the Excel file
# ---------------------------------------------------------

file_path = "../data/Untitled spreadsheet.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name=0
)


# ---------------------------------------------------------
# Show original dataset information
# ---------------------------------------------------------

print("\n================ ORIGINAL DATASET ================\n")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())


# ---------------------------------------------------------
# Clean the dataset
# ---------------------------------------------------------

cleaned_df = clean_dataset(df)


# ---------------------------------------------------------
# Show cleaned dataset information
# ---------------------------------------------------------

print("\n================ CLEANED DATASET ================\n")

print("Rows:", len(cleaned_df))
print("Columns:", len(cleaned_df.columns))

print("\nColumn names:")
print(cleaned_df.columns.tolist())


# ---------------------------------------------------------
# Show missing values
# ---------------------------------------------------------

print("\n================ MISSING VALUES ================\n")

print(cleaned_df.isnull().sum())


# ---------------------------------------------------------
# Show complaint categories
# ---------------------------------------------------------

if "Complaint Category" in cleaned_df.columns:

    print("\n================ COMPLAINT CATEGORIES ================\n")

    print(
        cleaned_df["Complaint Category"]
        .value_counts()
    )


# ---------------------------------------------------------
# Show solution categories
# ---------------------------------------------------------

if "Solution Category" in cleaned_df.columns:

    print("\n================ SOLUTION CATEGORIES ================\n")

    print(
        cleaned_df["Solution Category"]
        .value_counts()
    )