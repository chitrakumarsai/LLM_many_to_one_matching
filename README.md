# Houston Materials Data Matching

This script processes and matches material data from two Excel files using natural language processing (NLP) techniques. It leverages the `linktransformer` library for semantic matching of textual data.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This script reads two Excel files containing material data, cleans and tokenizes the textual data, and then performs 1-to-many matching using a pre-trained model (`all-MiniLM-L6-v2`) from the `linktransformer` library.

The goal is to identify and link matching records based on semantic similarity between text fields from the two datasets.

## Features

- Reads and processes two Excel files.
- Cleans and tokenizes text fields for better matching.
- Uses NLP for semantic matching of records.
- Outputs matched data with similarity scores.

## Requirements

The script requires the following Python libraries:

- `pandas`
- `openpyxl`
- `linktransformer`
- `re`

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required libraries:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pandas openpyxl linktransformer
   ```

3. **Prepare Data**:
   Place the two Excel files (`Houston SAP Materials.xlsx` and `Material list 011625.xlsx`) in the `data` folder.

## Usage

Run the script to process and match the data:
```bash
python script.py
```

### Key Steps in the Script:
1. **Load Data**:
   - Reads data from two Excel files.
   - Cleans column names by replacing special characters with underscores and converting them to uppercase.

2. **Text Cleaning and Tokenization**:
   - Removes punctuation and converts text to lowercase for better matching.

3. **Semantic Matching**:
   - Uses the `linktransformer` library to perform 1-to-many matching of text fields.

4. **Output**:
   - Displays the top 10 matched records.

## Sample Output

| MATNR       | SHORT_TEXT         | PURCHASE_ORDER__TEXT              | ... | id_lt_y | score  |
|-------------|--------------------|------------------------------------|-----|---------|--------|
| 1100298596  | "O"RING 1AP22 S... | ORING 1AP22 S/N'S: ST-1843...     | ... | 1834    | 0.491  |
| ...         | ...                | ...                                | ... | ...     | ...    |

The output includes matched records with similarity scores.

## Troubleshooting

### Error: Deprecated `load_metric` Import in `linktransformer`
The error indicates that the `linktransformer` package's `train_clf_model.py` file is still trying to import `load_metric` from the `datasets` library, even though it has been deprecated. To resolve this, you need to update the `linktransformer` package code or use a compatible older version of the `datasets` library.

### Resolution Steps

#### Option 1: Update the `linktransformer` Code

1. **Locate the `train_clf_model.py` File**:
   Navigate to the file path:
   ```bash
   /Users/.venv/lib/python3.10/site-packages/linktransformer/train_clf_model.py
   ```

2. **Edit the Import Statement**:
   Replace the `load_metric` import with `load` from the `evaluate` library. Open the file in an editor and update:
   ```python
   from datasets import load_dataset, load_metric, DatasetDict
   ```
   to:
   ```python
   from datasets import load_dataset, DatasetDict
   from evaluate import load as load_metric
   ```

3. **Save the Changes**:
   Save the file and re-run your script.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
