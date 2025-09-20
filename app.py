# app.py
import streamlit as st
import traceback
from recommender import recommend, CONTENT_DF

st.set_page_config(page_title="Personalized Learning Recommender", layout="centered")

st.title("🎓 Personalized Learning Recommendation System")
st.write("Select interests and enter your last quiz score. The app recommends suitable content.")

# Sidebar/debug
with st.sidebar:
    st.header("Debug / Deployment Help")
    st.write("If the app fails, check that `data/content.csv` or `content.csv` exists in the repo root or `data/` folder.")
    if st.checkbox("Show loaded dataset (debug)"):
        st.dataframe(CONTENT_DF)

# Build UI inputs
subjects = sorted(CONTENT_DF["subject"].dropna().unique().tolist())
if not subjects:
    subjects = ["Math", "Science", "History"]

interests = st.multiselect("Select your interests:", options=subjects)
score = st.slider("Enter your last quiz score:", 0, 100, 60)

if st.button("Get Recommendations"):
    try:
        if not interests:
            st.info("No interests selected — recommending top content based on score only.")
        results = recommend(interests, score, top_k=10)

        if results is None or results.empty:
            st.warning("No recommendations found for the chosen inputs. Try selecting other interests or adjust the score.")
        else:
            st.success(f"Found {len(results)} recommendation(s):")
            for _, row in results.iterrows():
                st.markdown(f"**{row['title']}** — {row['subject']} • {row['difficulty']} • {row.get('type','')}")
    except Exception as e:
        st.error("An unexpected error occurred. See stack trace below.")
        st.exception(traceback.format_exc())
