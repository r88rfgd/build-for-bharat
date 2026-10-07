import pandas as pd
import numpy as np

def clean_and_convert():
    print("Converting JDS Skill Traits.xlsx to cleaned_jds_skills.csv...")
    try:
        # Load JDS
        jds = pd.read_excel('JDS Skill Traits.xlsx')
        print(f"Original JDS Columns: {jds.columns.tolist()}")
        
        # Clean column names: lower case, strip whitespace, replace spaces/slashes with underscores
        jds.columns = jds.columns.str.lower().str.strip().str.replace(' ', '_').str.replace('/', '_')
        print(f"Cleaned JDS Columns: {jds.columns.tolist()}")
        
        # Save to CSV
        jds.to_csv('cleaned_jds_skills.csv', index=False)
        print(f"Successfully saved cleaned_jds_skills.csv, shape: {jds.shape}\n")
    except Exception as e:
        print(f"Error processing JDS dataset: {e}\n")

    print("Converting SDS Personality Traits.xlsx to cleaned_sds_personality.csv...")
    try:
        # Load SDS
        sds = pd.read_excel('SDS Personality Traits.xlsx')
        print(f"Original SDS Columns: {sds.columns.tolist()}")
        
        # Clean column names
        sds.columns = sds.columns.str.lower().str.strip().str.replace(' ', '_').str.replace('/', '_')
        print(f"Cleaned SDS Columns: {sds.columns.tolist()}")
        
        # Save to CSV
        sds.to_csv('cleaned_sds_personality.csv', index=False)
        print(f"Successfully saved cleaned_sds_personality.csv, shape: {sds.shape}\n")
    except Exception as e:
        print(f"Error processing SDS dataset: {e}\n")

if __name__ == "__main__":
    clean_and_convert()
