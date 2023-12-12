import streamlit as st
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
import os
from io import StringIO
import csv
import pdfx
import glob

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = pdfx.PDFx(file)
        text = pdf_reader.get_text()
        return text

# Function to preprocess text
def preprocess_text(text):
    # You may add your text preprocessing steps here
    return text.lower()

# Function to load and preprocess the job description
def load_and_preprocess_job_description(job_description):
    return preprocess_text(job_description)

# Function to load and preprocess CVs
def load_and_preprocess_cvs(pdf_files):
    cv_data = pd.DataFrame(columns=['Parsed_text'])
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        parsed_text = preprocess_text(text)
        cv_data = cv_data.append({'Parsed_text': parsed_text}, ignore_index=True)
    return cv_data

# Function to rank CVs based on Doc2Vec model
def rank_cvs(doc2vec_model, job_vector, cv_data):
    cv_vectors = [doc2vec_model.infer_vector(text.split()) for text in cv_data['Parsed_text']]
    similarity_scores = cosine_similarity([job_vector], cv_vectors)[0]
    return similarity_scores

def parser(pdf_files, output_csv):
    # Create a list to store tuples of (pdf_file_name, parsed_text)
    parsed_data = []

    for pdf_file in pdf_files:
        if pdf_file.name.endswith(".pdf"):
            # Parse
            pdf = pdfx.PDFx(pdf_file)
            parsed_text = pdf.get_text()

            # Append the tuple to the list
            parsed_data.append((pdf_file.name, parsed_text))

    # Save the parsed data to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['PDF File Name', 'Parsed Text'])  # Write header

        for pdf_name, parsed_text in parsed_data:
            csv_writer.writerow([pdf_name, parsed_text])


    # Save the parsed data to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['PDF File Name', 'Parsed Text'])  # Write header

        for pdf_name, parsed_text in parsed_data:
            csv_writer.writerow([pdf_name, parsed_text])

# Streamlit App
def main():
    st.title("RecruitFlow")

    # Job Description Input
    job_description = st.text_area("Enter Job Description")

    # CVs Upload
    st.write("Upload CVs (PDF)")
    pdf_files = st.file_uploader("Drop PDF files here", type=["pdf"], accept_multiple_files=True)

    # Rank Button
    if st.button("Rank CVs"):
        if not pdf_files or not job_description:
            st.warning("Please provide a job description and upload CVs.")
        else:
            # Parse PDFs and save to CSV
            csv_file = r"C:\Users\rayen\OneDrive\Desktop\LCS3\AI (mini project)\RecruitFlow\tempcv.csv"
            parser(pdf_files, csv_file)

            # Load Doc2Vec model (modify the path accordingly)
            model_path = r"C:\Users\rayen\OneDrive\Desktop\LCS3\AI (mini project)\RecruitFlow\modelData"
            doc2vec_model = Doc2Vec.load(model_path)

            # Load and preprocess job description
            job_description = load_and_preprocess_job_description(job_description)
            job_vector = doc2vec_model.infer_vector(job_description.split())

            # Load and preprocess CVs
            cv_data = load_and_preprocess_cvs(pdf_files)

            # Rank CVs
            ranking_scores = rank_cvs(doc2vec_model, job_vector, cv_data)
            cv_data['Ranking_Score'] = ranking_scores

            # Display Results
            st.subheader("Ranked CVs:")
            st.table(cv_data.sort_values(by='Ranking_Score', ascending=False)[['Parsed_text', 'Ranking_Score']])


if __name__ == "__main__":
    main()
