#%%
import pandas as pd
import linktransformer as lt
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path1 = os.path.join(BASE_DIR, "data", "Houston SAP Materials.xlsx")
file_path2 = os.path.join(BASE_DIR, "data", "Material list 011625.xlsx")
DEST_DIR = os.path.join(BASE_DIR, "data")
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
df1['SAP_TEXT'] = df1['PURCHASE_ORDER__TEXT'].apply(clean_and_tokenize)
df2['PLANT_TEXT'] = df2['DESCRIPTION'].astype('str').apply(clean_and_tokenize)

df_lm_matched = lt.merge(df1, df2, merge_type='1:m', model="all-MiniLM-L6-v2", left_on="SAP_TEXT", right_on="PLANT_TEXT")
df_lm_matched.sort_values(by='score', ascending=False, inplace=False)
df_lm_matched.to_excel(DEST_DIR + 'Houston_data_matched.xlsx', index=False)

# %%
