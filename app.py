import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Helper function to categorize values
def get_category(position):
    if 1 <= position <= 3:
        return "1-3"
    elif 4 <= position <= 5:
        return "4-5"
    elif 6 <= position <= 10:
        return "6-10"
    elif 11 <= position <= 20:
        return "11-20"
    elif position >= 21:
        return "21+"
    return None

# Function to process the data
def process_data(data, regex_pattern):
    data['Category'] = data['Position'].apply(get_category)
    data['Marque/Hors Marque'] = data['Keyword'].apply(
        lambda x: "Marque" if re.search(regex_pattern, str(x), re.IGNORECASE) else "Hors Marque"
    )
    summary = data.groupby(['Category', 'Marque/Hors Marque']).size().unstack(fill_value=0)
    return data, summary

# Export to Excel
def export_to_excel(df, summary):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed Data')
        summary.to_excel(writer, sheet_name='Summary')
    return output.getvalue()

# Streamlit UI
st.title("Analyse Marque / Hors Marque")

# Step 1: Upload XLSX file
uploaded_file = st.file_uploader("Upload your XLSX file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(df)

    # Ensure necessary columns exist
    if "Keyword" in df.columns and "Position" in df.columns:
        # Step 2: Input regex for "Marque"
        regex_pattern = st.text_input("Enter regex pattern for 'Marque'", ".*sara.*|.*lavoi.*|.*ponia.*")

        # Step 3: Process data
        processed_data, summary = process_data(df, regex_pattern)

        st.write("Processed Data:")
        st.dataframe(processed_data)

        st.write("Summary:")
        st.dataframe(summary)

        # Step 4: Export processed data
        st.download_button(
            label="Download Processed Data",
            data=export_to_excel(processed_data, summary),
            file_name="processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("The uploaded file must contain 'Keyword' and 'Position' columns.")
