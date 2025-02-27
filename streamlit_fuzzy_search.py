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
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def fuzzy_match(query, choices, threshold=60):
    match, score = process.extractOne(query, choices)
    return match if score >= threshold else None

def search_topic(topic, vocab_df):
    matched_unit = fuzzy_match(topic, vocab_df['Vocabulary Words'].astype(str).tolist())
    if matched_unit:
        unit_info = vocab_df[vocab_df['Vocabulary Words'] == matched_unit].iloc[0]
        return {
            "Unit Name": unit_info["Unit Name"],
            "Reach Higher Level": unit_info["Reach Higher Level"],
            "Unit Number": unit_info["Unit Number"],
            "Part of Unit": unit_info["Part of Unit"],
            "Key Vocabulary": vocab_df[vocab_df['Unit Number'] == unit_info['Unit Number']]['Vocabulary Words'].tolist()
        }
    return None

def search_skill(skill, curriculum_df):
    matched_skill = fuzzy_match(skill, curriculum_df['Skill'].astype(str))
    if matched_skill:
        skill_info = curriculum_df[curriculum_df['Skill'] == matched_skill].iloc[0]
        return {
            "Skill Name": skill_info["Skill"],
            "Unit Name": skill_info["Unit Name"],
            "Reach Higher Level": skill_info["Reach Higher Level"],
            "Unit Number": skill_info["Unit Number"],
            "Part of Unit": skill_info["Part of Unit"]
        }
    return None

# Load Data
vocab_df = load_data(VOCAB_URL)
curriculum_df = load_data(CURRICULUM_URL)

# Streamlit UI
st.title("Reach Higher Alignment Search")
search_type = st.radio("Select Search Type", ["Topic", "Learning Skill"])
search_input = st.text_input("Enter your search term")

if st.button("Search") and search_input:
    if search_type == "Topic" and vocab_df is not None:
        result = search_topic(search_input, vocab_df)
    elif search_type == "Learning Skill" and curriculum_df is not None:
        result = search_skill(search_input, curriculum_df)
    else:
        result = None
    
    if result:
        st.write("### Match Found:")
        for key, value in result.items():
            if isinstance(value, list):
                st.write(f"**{key}:**")
                st.write("- " + "\n- ".join(value))
            else:
                st.write(f"**{key}:** {value}")
    else:
        st.write("No close match found.")
