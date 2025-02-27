import streamlit as st
import pandas as pd
import difflib

# Load CSV files from GitHub repository
def load_csv_from_github(file_name):
    url = f"https://raw.githubusercontent.com/carly-meyer-lakota/Reach-Higher-Alignment-2/main/{file_name}"
    return pd.read_csv(url)

# Load datasets
@st.cache_data
def load_data():
    vocabulary_df = load_csv_from_github("vocabulary.csv")
    skills_df = load_csv_from_github("reach_higher_curriculum.csv")
    return vocabulary_df, skills_df

vocabulary_df, skills_df = load_data()

# Fuzzy matching function
def fuzzy_match(query, choices, cutoff=0.6):
    matches = difflib.get_close_matches(query, choices, n=5, cutoff=cutoff)
    return matches if matches else None

# Search for a topic in vocabulary.csv
def search_topic(query):
    matched_units = fuzzy_match(query, vocabulary_df['Topic'].astype(str).tolist())
    if matched_units:
        results = vocabulary_df[vocabulary_df['Topic'].isin(matched_units)]
        return results[['Unit Name', 'Reach Higher Level', 'Unit Number', 'Part of Unit', 'Key Vocabulary']]
    return None

# Search for a learning skill in reach_higher_curriculum.csv
def search_skill(query):
    matched_skills = fuzzy_match(query, skills_df['Skill'].astype(str).tolist())
    if matched_skills:
        results = skills_df[skills_df['Skill'].isin(matched_skills)]
        return results[['Skill']]
    return None

# Streamlit UI
st.title("Reach Higher Alignment Search Tool")
search_type = st.radio("Select search type:", ("Topic", "Learning Skill"))
query = st.text_input("Enter your search term:")

if query:
    if search_type == "Topic":
        result = search_topic(query)
        if result is not None:
            st.write("### Matching Unit:")
            st.dataframe(result)
        else:
            st.write("No matching unit found.")
    else:
        result = search_skill(query)
        if result is not None:
            st.write("### Matching Skill:")
            st.dataframe(result)
        else:
            st.write("No matching skill found.")
