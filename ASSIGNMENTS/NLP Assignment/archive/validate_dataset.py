"""
validate_dataset.py

Validation script for the "NLP Concepts Learning Dataset" collection.

Run this script from inside the NLP_Concepts_Learning_Dataset folder
(or point DATA_DIR at the folder) to check that every required file is
present and that each CSV meets basic data-quality expectations:

  - The file exists and loads correctly
  - Displays shape (rows, columns) and column names
  - Checks for missing values
  - Checks for duplicate rows
  - Checks for duplicate IDs (where an 'id' column is present)
  - Displays basic descriptive statistics
  - Reports any problems in a clear, readable summary at the end

Usage:
    python validate_dataset.py
    python validate_dataset.py --data-dir /path/to/NLP_Concepts_Learning_Dataset
"""

import argparse
import os
import sys
import pandas as pd

REQUIRED_FILES = [
    "nlp_basics.csv",
    "text_preprocessing.csv",
    "bow_tfidf.csv",
    "ngrams.csv",
    "sentiment_analysis.csv",
    "named_entity_recognition.csv",
    "text_classification.csv",
    "text_similarity.csv",
    "word_embeddings.csv",
    "transformer_examples.csv",
    "question_answering.csv",
    "text_summarization.csv",
    "spam_detection.csv",
    "topic_modeling.csv",
    "language_detection.csv",
    "dataset_summary.csv",
]

EXPECTED_MIN_ROWS = {
    "nlp_basics.csv": 2000,
    "text_preprocessing.csv": 2000,
    "bow_tfidf.csv": 2000,
    "ngrams.csv": 2000,
    "sentiment_analysis.csv": 3000,
    "named_entity_recognition.csv": 2000,
    "text_classification.csv": 3000,
    "text_similarity.csv": 2000,
    "word_embeddings.csv": 2000,
    "transformer_examples.csv": 2000,
    "question_answering.csv": 2000,
    "text_summarization.csv": 2000,
    "spam_detection.csv": 3000,
    "topic_modeling.csv": 3000,
    "language_detection.csv": 2000,
}


def hr(char="-", width=88):
    print(char * width)


def validate_file(path, filename, problems, warnings):
    print()
    hr("=")
    print(f"FILE: {filename}")
    hr("=")

    if not os.path.exists(path):
        msg = f"MISSING FILE: {filename} was not found at {path}"
        print(f"  [FAIL] {msg}")
        problems.append(msg)
        return

    try:
        df = pd.read_csv(path)
    except Exception as e:
        msg = f"COULD NOT LOAD {filename}: {e}"
        print(f"  [FAIL] {msg}")
        problems.append(msg)
        return

    # Shape and columns
    print(f"  Shape        : {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"  Columns      : {list(df.columns)}")

    # Expected row count check
    expected_min = EXPECTED_MIN_ROWS.get(filename)
    if expected_min is not None:
        if df.shape[0] < expected_min:
            msg = f"{filename}: expected at least {expected_min} rows, found {df.shape[0]}"
            print(f"  [FAIL] {msg}")
            problems.append(msg)
        else:
            print(f"  [OK]   Row count meets minimum expectation ({expected_min})")

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        print(f"  [WARN] Missing values found (may be expected, e.g. NER rows that "
              f"don't contain every entity type):")
        for col, cnt in missing.items():
            print(f"           - {col}: {cnt} missing")
        warnings.append(f"{filename}: missing values in columns {list(missing.index)}")
    else:
        print("  [OK]   No missing values")

    # Duplicate rows
    dup_rows = df.duplicated().sum()
    if dup_rows > 0:
        msg = f"{filename}: {dup_rows} fully duplicated rows found"
        print(f"  [FAIL] {msg}")
        problems.append(msg)
    else:
        print("  [OK]   No fully duplicated rows")

    # Duplicate IDs
    if "id" in df.columns:
        dup_ids = df["id"].duplicated().sum()
        if dup_ids > 0:
            msg = f"{filename}: {dup_ids} duplicate 'id' values found"
            print(f"  [FAIL] {msg}")
            problems.append(msg)
        else:
            print("  [OK]   No duplicate IDs")
    else:
        print("  [INFO] No 'id' column in this file (skipping duplicate-ID check)")

    # Basic statistics
    print("  Basic statistics:")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        stats = df[numeric_cols].describe().transpose()
        print(stats.to_string())
    else:
        print("           (no numeric columns)")

    # Text column length stats for the first text-like column, if present
    text_col_candidates = [c for c in df.columns if df[c].dtype == object]
    if text_col_candidates:
        sample_col = text_col_candidates[0]
        lengths = df[sample_col].astype(str).str.len()
        print(f"  Sample text column '{sample_col}' length stats:")
        print(f"           min={lengths.min()}, max={lengths.max()}, mean={lengths.mean():.1f}")


def main():
    parser = argparse.ArgumentParser(description="Validate the NLP Concepts Learning Dataset collection.")
    parser.add_argument(
        "--data-dir",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Path to the folder containing the dataset CSV files (defaults to this script's folder).",
    )
    args = parser.parse_args()
    data_dir = args.data_dir

    print("NLP Concepts Learning Dataset - Validation Report")
    print(f"Data directory: {data_dir}")

    problems = []
    warnings = []

    # Check required files exist
    print()
    hr("=")
    print("REQUIRED FILE CHECK")
    hr("=")
    for f in REQUIRED_FILES:
        exists = os.path.exists(os.path.join(data_dir, f))
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {f}")
        if not exists:
            problems.append(f"Required file missing: {f}")

    # Validate each CSV file in detail
    for f in REQUIRED_FILES:
        validate_file(os.path.join(data_dir, f), f, problems, warnings)

    # Final summary
    print()
    hr("=")
    print("VALIDATION SUMMARY")
    hr("=")
    if warnings:
        print(f"  {len(warnings)} warning(s) (non-fatal, review recommended):\n")
        for i, w in enumerate(warnings, start=1):
            print(f"    {i}. {w}")
        print()
    if problems:
        print(f"  {len(problems)} problem(s) found:\n")
        for i, p in enumerate(problems, start=1):
            print(f"    {i}. {p}")
        print()
        print("  Result: FAILED - please review the issues above.")
        sys.exit(1)
    else:
        print("  All required files present; no duplicate rows, no duplicate IDs, no missing required files.")
        print("  Result: PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
