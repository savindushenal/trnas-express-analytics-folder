import pandas as pd


def clean_dataset(df):
    """
    Clean and standardize the Trans Express dataset.

    The original dataframe is copied so that the uploaded
    dataset is not modified directly.
    """

    # ---------------------------------------------------------
    # 1. Make a copy of the original dataframe
    # ---------------------------------------------------------

    df = df.copy()

    # ---------------------------------------------------------
    # 2. Clean column names
    # ---------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # ---------------------------------------------------------
    # 3. Clean text columns
    # ---------------------------------------------------------

    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # ---------------------------------------------------------
    # 4. Convert "-" and empty strings into missing values
    # ---------------------------------------------------------

    df = df.replace(
        {
            "-": pd.NA,
            "": pd.NA,
            " ": pd.NA
        }
    )

    # ---------------------------------------------------------
    # 5. Standardize Client Y / N
    # ---------------------------------------------------------

    if "Client Y / N" in df.columns:

        df["Client Y / N"] = (
            df["Client Y / N"]
            .astype("string")
            .str.strip()
            .str.upper()
        )

        df["Client Y / N"] = df["Client Y / N"].replace(
            {
                "YES": "Y",
                "NO": "N"
            }
        )

    # ---------------------------------------------------------
    # 6. Treat Client No as an identifier
    # ---------------------------------------------------------
    # Client numbers should NOT be averaged or mathematically
    # imputed because they are identifiers.

    if "Client No" in df.columns:
        df["Client No"] = (
            df["Client No"]
            .astype("string")
            .str.strip()
        )

    # ---------------------------------------------------------
    # 7. Clean complaint / inquiry text
    # ---------------------------------------------------------

    if "Complaint / Inquiry" in df.columns:

        df["Complaint / Inquiry"] = (
            df["Complaint / Inquiry"]
            .astype("string")
            .str.strip()
        )

    # ---------------------------------------------------------
    # 8. Create Complaint Category
    # ---------------------------------------------------------

    if "Complaint / Inquiry" in df.columns:

        complaint_text = (
            df["Complaint / Inquiry"]
            .fillna("")
            .str.lower()
        )

        conditions = [
            complaint_text.str.contains(
                r"\bre[\s-]*deliver(?:y)?\b",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"return",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"urgent|today|tomorrow|tomarrow",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"order status|tracking|tracking no|way bill|waybill",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"branch.*(no|number|location)|branch number|branch location",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"cod|payment",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"new register|new registration",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"detail",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"tamil",
                regex=True,
                na=False
            ),

            complaint_text.str.contains(
                r"customer refused",
                regex=True,
                na=False
            )
        ]

        categories = [
            "Re-delivery Request",
            "Return Request",
            "Urgent Delivery Request",
            "Tracking / Order Status",
            "Branch Information",
            "COD / Payment Issue",
            "New Registration",
            "Information Request",
            "Language Request",
            "Customer Refused"
        ]

        df["Complaint Category"] = pd.Series(
            pd.NA,
            index=df.index,
            dtype="string"
        )

        for condition, category in zip(conditions, categories):
            df.loc[
                condition & df["Complaint Category"].isna(),
                "Complaint Category"
            ] = category

        # Everything that does not match the rules
        # is kept as Other / Unclassified.

        df["Complaint Category"] = (
            df["Complaint Category"]
            .fillna("Other / Unclassified")
        )

    # ---------------------------------------------------------
    # 9. Standardize common solution descriptions
    # ---------------------------------------------------------

    if "Solution" in df.columns:

        solution_text = (
            df["Solution"]
            .fillna("")
            .str.lower()
        )

        df["Solution Category"] = "Other / Unclassified"

        df.loc[
            solution_text.str.contains(
                r"transfer|tranfer",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Call Transferred"

        df.loc[
            solution_text.str.contains(
                r"informed|info",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Information Provided"

        df.loc[
            solution_text.str.contains(
                r"number|no\.",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Contact Number Provided"

        df.loc[
            solution_text.str.contains(
                r"call back|called back|check.*back",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Call Back / Follow-up"

        df.loc[
            solution_text.str.contains(
                r"return",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Return Processed"

        df.loc[
            solution_text.str.contains(
                r"done|delivered",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Completed"

        df.loc[
            solution_text.str.contains(
                r"disconnect|disconect",
                regex=True,
                na=False
            ),
            "Solution Category"
        ] = "Disconnected"

    # ---------------------------------------------------------
    # 10. Remove completely empty rows
    # ---------------------------------------------------------

    df = df.dropna(
        how="all"
    )

    # ---------------------------------------------------------
    # 11. Remove exact duplicate rows
    # ---------------------------------------------------------

    df = df.drop_duplicates()

    # ---------------------------------------------------------
    # 12. Return cleaned dataframe
    # ---------------------------------------------------------

    return df