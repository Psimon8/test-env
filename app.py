import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Helper function to categorize values
def get_category(position):
    if position == 1:
        return "Top 1"
    elif 2 <= position <= 3:
        return "Position 2-3"
    elif 4 <= position <= 5:
        return "Position 4-5"
    elif 6 <= position <= 10:
        return "Position 6-10"
    elif 11 <= position <= 20:
        return "Position 11-20"
    elif position >= 21:
        return "21+"
    return None

# Function to process the data
def process_data(data, regex_pattern):
    data['Category'] = data['Position'].apply(get_category)
    data['Marque/Hors Marque'] = data['Keyword'].apply(
        lambda x: "Marque" if re.search(regex_pattern, str(x), re.IGNORECASE) else "Hors Marque"
    )
    # Reorder columns: place Category and Marque/Hors Marque after Search Volume
    if "Search Volume" in data.columns:
        columns = list(data.columns)
        columns.insert(columns.index("Search Volume") + 1, columns.pop(columns.index("Category")))
        columns.insert(columns.index("Search Volume") + 2, columns.pop(columns.index("Marque/Hors Marque")))
        data = data[columns]

    # Group by Category and Marque/Hors Marque
    summary = data.groupby(['Category', 'Marque/Hors Marque']).size().unstack(fill_value=0)

    # Ensure the summary is displayed in the specified order
    category_order = ["Top 1", "Position 2-3", "Position 4-5", "Position 6-10", "Position 11-20", "21+"]
    summary = summary.reindex(category_order)

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

    # Ensure necessary columns exist
    if "Keyword" in df.columns and "Position" in df.columns and "Search Volume" in df.columns:
        # Step 2: Input regex for "Marque"
        col1, col2 = st.columns(2)
        with col1:
            regex_pattern = st.text_input("Enter regex pattern for 'Marque'", "regex-friendly .*")
            selected_category = st.selectbox("Select Category", ["All"] + ["Top 1", "Position 2-3", "Position 4-5", "Position 6-10", "Position 11-20", "21+"])
            keyword = st.text_input("Enter Keyword (regex supported)")

        # Step 3: Process data
        processed_data, summary = process_data(df, regex_pattern)

        # Filter data based on selected category and keyword
        filtered_data = processed_data.copy()
        if selected_category != "All":
            filtered_data = filtered_data[filtered_data['Category'] == selected_category]
        if keyword:
            filtered_data = filtered_data[filtered_data['Keyword'].str.contains(keyword, case=False, na=False)]

        # Display summary table
        with col2:
            st.write("Summary Table:")
            summary_table = filtered_data.groupby(['Category', 'Marque/Hors Marque']).size().unstack(fill_value=0).reindex(["Top 1", "Position 2-3", "Position 4-5", "Position 6-10", "Position 11-20", "21+"], fill_value=0)
            st.dataframe(summary_table)

        # Display data for Marque and Hors Marque side by side
        col1, col2 = st.columns(2)
        with col1:
            st.write("Data for Marque:")
            marque_data = filtered_data[filtered_data['Marque/Hors Marque'] == 'Marque']
            st.dataframe(marque_data)
        with col2:
            st.write("Data for Hors Marque:")
            hors_marque_data = filtered_data[filtered_data['Marque/Hors Marque'] == 'Hors Marque']
            st.dataframe(hors_marque_data)

        # Add download button
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )

        # Step 5: Export processed data
        st.download_button(
            label="Download Processed Data",
            data=export_to_excel(filtered_data, summary),
            file_name="processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("The uploaded file must contain 'Keyword', 'Position', and 'Search Volume' columns.")
