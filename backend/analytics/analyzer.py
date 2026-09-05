import pandas as pd


def clean_distribution(series):
    """
    Convert a Pandas Series into a JSON-safe dictionary.
    Missing values are shown as 'Missing'.
    """

    cleaned = series.fillna("Missing")

    counts = cleaned.value_counts()

    return {
        str(key): int(value)
        for key, value in counts.items()
    }


def get_top_values(series, limit=10):
    """
    Return the most common values from a column.
    """

    cleaned = series.fillna("Missing")

    counts = cleaned.value_counts().head(limit)

    return [
        {
            "name": str(name),
            "count": int(count)
        }
        for name, count in counts.items()
    ]


def get_cross_tabulation(df, row_column, column_column):
    """
    Create a cross-tabulation between two columns.
    """

    table = pd.crosstab(
        df[row_column].fillna("Missing"),
        df[column_column].fillna("Missing")
    )

    result = []

    for row_name, row in table.iterrows():

        row_data = {
            "name": str(row_name)
        }

        for column_name, value in row.items():
            row_data[str(column_name)] = int(value)

        result.append(row_data)

    return result


def analyze_dataset(df):
    """
    Perform business analytics on the cleaned
    Trans Express dataset.
    """

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    total_records = len(df)
    total_columns = len(df.columns)

    # =========================================================
    # UNIQUE COUNTS
    # =========================================================

    total_operators = df["Operator"].nunique()

    total_branches = df["Branch"].nunique()

    total_departments = df["Department"].nunique()

    total_statuses = df["Status"].nunique()

    # =========================================================
    # CLIENT DISTRIBUTION
    # =========================================================

    client_distribution = clean_distribution(
        df["Client Y / N"]
    )

    # =========================================================
    # DEPARTMENT DISTRIBUTION
    # =========================================================

    department_distribution = clean_distribution(
        df["Department"]
    )

    # =========================================================
    # BRANCH DISTRIBUTION
    # =========================================================

    branch_distribution = clean_distribution(
        df["Branch"]
    )

    # =========================================================
    # STATUS DISTRIBUTION
    # =========================================================

    status_distribution = clean_distribution(
        df["Status"]
    )

    # =========================================================
    # SOLUTION DISTRIBUTION
    # =========================================================

    solution_distribution = clean_distribution(
        df["Solution"]
    )

    # =========================================================
    # COMPLAINT DISTRIBUTION
    # =========================================================

    complaint_distribution = clean_distribution(
        df["Complaint / Inquiry"]
    )

    # =========================================================
    # COMPLAINT CATEGORY DISTRIBUTION
    # =========================================================

    complaint_category_distribution = clean_distribution(
        df["Complaint Category"]
    )

    # =========================================================
    # SOLUTION CATEGORY DISTRIBUTION
    # =========================================================

    solution_category_distribution = clean_distribution(
        df["Solution Category"]
    )

    # =========================================================
    # OPERATOR DISTRIBUTION
    # =========================================================

    operator_distribution = clean_distribution(
        df["Operator"]
    )

    # =========================================================
    # TOP COMPLAINT CATEGORIES
    # =========================================================

    top_complaint_categories = get_top_values(
        df["Complaint Category"],
        limit=10
    )

    # =========================================================
    # TOP BRANCHES
    # =========================================================

    top_branches = get_top_values(
        df["Branch"],
        limit=10
    )

    # =========================================================
    # TOP DEPARTMENTS
    # =========================================================

    top_departments = get_top_values(
        df["Department"],
        limit=10
    )

    # =========================================================
    # OPERATOR WORKLOAD
    # =========================================================

    operator_workload = get_top_values(
        df["Operator"],
        limit=20
    )

    # =========================================================
    # BRANCH × COMPLAINT CATEGORY
    # =========================================================

    branch_complaint_analysis = get_cross_tabulation(
        df,
        "Branch",
        "Complaint Category"
    )

    # =========================================================
    # DEPARTMENT × COMPLAINT CATEGORY
    # =========================================================

    department_complaint_analysis = get_cross_tabulation(
        df,
        "Department",
        "Complaint Category"
    )

    # =========================================================
    # STATUS × COMPLAINT CATEGORY
    # =========================================================

    status_complaint_analysis = get_cross_tabulation(
        df,
        "Status",
        "Complaint Category"
    )

    # =========================================================
    # MISSING VALUE SUMMARY
    # =========================================================

    missing_values = {
        str(column): int(value)
        for column, value in df.isnull().sum().items()
    }

    # =========================================================
    # DUPLICATE COUNT
    # =========================================================

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # =========================================================
    # FINAL RESULT
    # =========================================================

    return {

        # Basic information
        "total_records": int(total_records),
        "total_columns": int(total_columns),

        # KPI counts
        "total_operators": int(total_operators),
        "total_branches": int(total_branches),
        "total_departments": int(total_departments),
        "total_statuses": int(total_statuses),

        # Data quality
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,

        # Main distributions
        "client_distribution": client_distribution,
        "operator_distribution": operator_distribution,
        "department_distribution": department_distribution,
        "branch_distribution": branch_distribution,
        "status_distribution": status_distribution,

        # Raw data distributions
        "solution_distribution": solution_distribution,
        "complaint_distribution": complaint_distribution,

        # Standardized analytical categories
        "complaint_category_distribution":
            complaint_category_distribution,

        "solution_category_distribution":
            solution_category_distribution,

        # Top values
        "top_complaint_categories":
            top_complaint_categories,

        "top_branches":
            top_branches,

        "top_departments":
            top_departments,

        "operator_workload":
            operator_workload,

        # Cross-analysis
        "branch_complaint_analysis":
            branch_complaint_analysis,

        "department_complaint_analysis":
            department_complaint_analysis,

        "status_complaint_analysis":
            status_complaint_analysis
    }