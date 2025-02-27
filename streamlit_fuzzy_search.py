import streamlit as st
import pandas as pd
import requests
from thefuzz import process

# GitHub raw file URLs
GITHUB_USER = "carly-meyer-lakota"
REPO_NAME = "Reach-Higher-Alignment-2"
VOCAB_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/vocabulary.csv"
CURRICULUM_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/reach_higher_curriculum.csv"

def load_data(url):
    try:
        df = pd.read_csv(url)
        st.write(f"Loaded {url} with columns: {df.columns.tolist()}")  # Debugging: Print column names
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def fuzzy_match(query, choices, threshold=60):
    match, score = process.extractOne(query, choices)
    return match if score >= threshold else None

def search_any_column(query, df):
    best_match = None
    best_score = 0
    match_info = {}
    
    for column in df.columns:
        matches = df[column].dropna().astype(str).tolist()
        match, score = process.extractOne(query, matches) if matches else (None, 0)
        
        if match and score > best_score:
            best_score = score
            best_match = match
            match_info = df[df[column] == match].iloc[0].to_dict()
    
    return match_info if best_match else None

# Load Data
vocab_df = load_data(VOCAB_URL)
curriculum_df = load_data(CURRICULUM_URL)

# Streamlit UI
st.title("Reach Higher Alignment Search")
search_input = st.text_input("Enter your search term")

if st.button("Search") and search_input:
    vocab_result = search_any_column(search_input, vocab_df) if vocab_df is not None else None
    curriculum_result = search_any_column(search_input, curriculum_df) if curriculum_df is not None else None
    
    if vocab_result or curriculum_result:
        st.write("### Match Found:")
        if vocab_result:
            st.write("#### Vocabulary Match:")
            for key, value in vocab_result.items():
                st.write(f"**{key}:** {value}")
        
        if curriculum_result:
            st.write("#### Curriculum Match:")
            for key, value in curriculum_result.items():
                st.write(f"**{key}:** {value}")
    else:
        st.write("No close match found.")
