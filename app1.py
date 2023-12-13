import streamlit as st
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import os
from io import BytesIO
import tempfile
import shutil
import csv

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    if isinstance(pdf_file, BytesIO):
        pdf_content = pdf_file.read()
        codecs_to_try = ['utf-8', 'latin-1']
        pdf_content_str = None

        for codec in codecs_to_try:
            try:
                pdf_content_str = pdf_content.decode(codec)
                break
            except UnicodeDecodeError:
                continue

        if pdf_content_str is None:
            raise UnicodeDecodeError("Unable to decode PDF content with available codecs.")

        return pdf_content_str
    else:
        raise ValueError("Invalid input. Expected BytesIO object.")

# Function to parse PDFs and save to CSV
def parser(pdf_files, output_csv):
    # Create a list to store tuples of (pdf_file_name, parsed_text)
    parsed_data = []

    for pdf_file in pdf_files:
        if pdf_file.name.endswith(".pdf"):
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_file)
            
            # Append the tuple to the list
            parsed_data.append((pdf_file.name, text))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, escapechar='\\')  # Specify escapechar
        csv_writer.writerow(['PDF File Name', 'Parsed Text'])  # Write header

        for pdf_name, parsed_text in parsed_data:
            csv_writer.writerow([pdf_name, parsed_text])

    # Move the temporary file to the desired location
    shutil.move(csv_file.name, output_csv)

# Function to load and preprocess job description
def load_and_preprocess_job_description(job_description):
    # Add your preprocessing steps here if needed
    return job_description

# Function to load and preprocess CVs
def load_and_preprocess_cvs(pdf_files):
    cv_data = pd.DataFrame(columns=['PDF File Name', 'Parsed Text'])

    for pdf_file in pdf_files:
        if pdf_file.name.endswith(".pdf"):
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_file)
            cv_data.loc[len(cv_data)] = [pdf_file.name, text]

    return cv_data

# Function to rank CVs
def rank_cvs(doc2vec_model, job_vector, cv_data):
    cv_vectors = [doc2vec_model.infer_vector(text.split()) for text in cv_data['Parsed Text']]
    similarity_matrix = cosine_similarity([job_vector], cv_vectors)
    
    scaler = MinMaxScaler()
    normalized_similarity = scaler.fit_transform(similarity_matrix.T).T

    return normalized_similarity[0]

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
            csv_file = "./pdf_parse.csv"
            parser(pdf_files, csv_file)

            # Load Doc2Vec model (modify the path accordingly)
            model_path = "./doc2vec_model.model"
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
            st.table(cv_data.sort_values(by='Ranking_Score', ascending=False)[['PDF File Name', 'Ranking_Score']])

if __name__ == "__main__":
    main()
