#%%
import pandas as pd
import linktransformer as lt
import os
import re
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/proc_houston_ta'
file_path1 = os.path.join(BASE_DIR, "data", "Houston SAP Materials.xlsx")
file_path2 = os.path.join(BASE_DIR, "data", "Material list 011625.xlsx")
DEST_DIR = os.path.join(BASE_DIR + '/proc_houston_ta', "data")
df1 = pd.read_excel(file_path1, engine='openpyxl')
df1.columns = [re.sub(r'[^a-zA-Z0-9]', "_",\
                         col.replace(' ', "_")).upper() for col in df1.columns]
df2 = pd.read_excel(file_path2, engine='openpyxl', skiprows=1)
df2.columns = [re.sub(r'[^a-zA-Z0-9]', "_",\
                            col.replace(' ', "_")).upper() for col in df2.columns]
# Function to clean, tokenize, and convert to lowercase
def clean_and_tokenize(text) -> str:
    # Replace all punctuation with spaces
    cleaned_text = re.sub(r'[^\w\s]', ' ', text)
    # Convert to lowercase
    cleaned_text = cleaned_text.lower()
    # # Split into tokens
    # tokens = cleaned_text.split()
    return cleaned_text
df1['SAP_TEXT'] = df1['ALL_TEXTS'].apply(clean_and_tokenize)
df2['PLANT_TEXT'] = df2['DESCRIPTION'].astype('str').apply(clean_and_tokenize)

df_lm_matched = lt.merge(df1, df2, merge_type='1:m', model="all-MiniLM-L6-v2", left_on="SAP_TEXT", right_on="PLANT_TEXT")
# df_lm_matched.to_excel(DEST_DIR + '/Houston_data_matched.xlsx', index=False)
# Function to extract numbers from a string



def extract_numbers(text):
    return re.findall(r'\d+', text)

# # Function to calculate the penalty
# def calculate_penalty(row):
#     numbers_a = extract_numbers(row['SAP_TEXT'])
#     numbers_b = extract_numbers(row['PLANT_TEXT'])
#     if numbers_a != numbers_b:
#         return 0.5
#     else:
#         return -0.5
#     return 0

# Function to calculate penalty dynamically
def calculate_dynamic_penalty(row):
    numbers_a = extract_numbers(row['SAP_TEXT'])
    numbers_b = extract_numbers(row['PLANT_TEXT'])
    
    # Count mismatches
    mismatch_count = sum(1 for a, b in zip(numbers_a, numbers_b) if a != b)
    mismatch_count += abs(len(numbers_a) - len(numbers_b))  # Account for unequal lengths
    
    # Derive penalty: each mismatch adds 10 points to the penalty
    penalty = mismatch_count * 0.1
    return row['score'] - penalty

# Apply dynamic penalty calculation
df_lm_matched['score'] = df_lm_matched.apply(calculate_dynamic_penalty, axis=1)

# # Apply the penalty calculation
# df_lm_matched['PENALTY'] = df_lm_matched.apply(calculate_penalty, axis=1)

# # Subtract the penalty from the score
# df_lm_matched['ADJ_SCORE'] = df_lm_matched['score'] - df_lm_matched['PENALTY']


columns_to_front = ['MATNR', 'ALL_TEXTS', 'DESCRIPTION', 'score', 'PLANT', 'PROJECT_NAME']
# Reorder the columns
new_column_order = columns_to_front + [col for col in df_lm_matched.columns if col not in columns_to_front]
df_lm_matched = df_lm_matched[new_column_order]
# Convert all columns to string except 'ADJ_SCORE'
columns_to_convert = [col for col in df_lm_matched.columns if col != 'score']
df_lm_matched[columns_to_convert] = df_lm_matched[columns_to_convert].astype(str)

# Function to set ADJ_SCORE to zero if specific strings are present
def adjust_score(row):
    phrases_to_set_zero = [
        "UOP Catalyst ordered by Capital-Walker",
        "SEE VALVE TECHNICIAN",
        "UOP Catalyst Order by Capital",
        "NO MATERIAL",
        "BLINDS PART OF THE HYDROCARBON HEADER ISOLATION",
        "nan"
    ]
    # Ensure the DESCRIPTION is a string and handle NaN values
    description = str(row['DESCRIPTION']) if pd.notnull(row['DESCRIPTION']) else ""
    
    # Check if any of the target phrases are in the description
    if any(phrase in description for phrase in phrases_to_set_zero):
        return float("-inf")  # Set ADJ_SCORE to zero
    return row['score']  # Keep original score

# Apply the function to adjust scores
df_lm_matched['score'] = df_lm_matched.apply(adjust_score, axis=1)

df_lm_matched.sort_values(by='score', ascending=False, inplace=True)

st.set_page_config(layout="wide", page_title="Houston Turn Around Materials" )
st.title("Houston Turn Around Materials")
st.data_editor(df_lm_matched)
# st.write(df_lm_matched.columns)

# %%
