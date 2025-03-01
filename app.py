# Import
import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Set up our App
st.set_page_config(page_title="Data Sweeper", layout='wide')
st.title("Data Sweeper")
st.write("Transform your file between CVS and Excel format with built-in data cleaning and visualization!")

upload_files = st.file_uploader("Upload you file (CSV or Excel):" , type=["csv" and "xlsx"],accept_multiple_files=True)

if upload_files:
     for file in upload_files:
         files_ext = os.path.splitext(file.name)[-1].lower()
         
         
         if files_ext == ".csv":
             df = pd.read_csv(file)
         elif files_ext == ".xlsx":
             df = pd.read_excel(file)
         else:
             st.error(f"Unsupported file type: {files_ext}")
             continue
         
         # Display info about the file 
         st.write(f"**File Name:** {file.name}")
         st.write(f"**File Size:** {file.size/1024}")
         
         # Show 5 row of our df
         st.write("Preview the Head of Dataframe")
         st.dataframe(df.head())
         
         # Option for data cleaning
         st.subheader("Data Cleaning Options")
         if st.checkbox(f"Clean Data for {file.name}"):
             col1, col2 = st.columns(2)
             
             with col1:
                 if st.button(f"Remove Duplicate from {file.name}"):
                     df.drop_duplicates(inplace=True)
                     st.write("Duplicate Removed!")
                     
                     with col2:
                         if st.button(f"Fill Missing Values for {file.name}"):
                             numeric_cols = df.select_dtypes(include=['numbers']).column
                             df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                             st.write("Missing Value has been filled!")
                             
                
         # Choose Specific Columns to Keep or Convert
         st.subheader("Select Columns to Convert")       
         columns = st.multiselect(f"Choose columns for {file.name}" , df.columns, default=df.columns)
         df = df(columns)
         
         
         # Create Some Visualization
         st.subheader("Data Visualization")
         if st.checkbox(f"Show Visualization for {file.name}"):
             st.bar_chart(df.select_dtype(include='number').iloc[:,:2])
             
             
         # Convert the File -> CSV to Excle
         st.subheader("Conversion Options")
         conversion_type = st.radio(f"Convert{file.name} to:" ,["CSV" ,"Excel"], key=file.name)
         if st.button(f"Convert{file.name}"):
             buffer = BytesIO
             if conversion_type == "CSV":
                 df.to_csv(buffer,index=False)
                 file_name = file.name.replace(files_ext,".csv")
                 mime_type = "text/csv"
                 
             elif conversion_type == "Excel":
                 df.to_excle(buffer, index=False)
                 file_name = file.name.replace(files_ext,".xlsx")
                 mime_type = "application/vnd.openxmlformats-officedocoment.spreadsheethtml.sheet"
             buffer.seek(0)   
             
             
             # Download Button
             st.download_button(
                 lable=f"Download {file.name} as {conversion_type}",
                 data=buffer,
                 filename=file_name,
                 mime=mime_type
                 )
             
st.success("All files processd!")