# app.py
import streamlit as st
import traceback
from recommender import recommend, CONTENT_DF

st.set_page_config(page_title="Personalized Learning Recommender", layout="centered")

st.title("🎓 Personalized Learning Recommendation System")
st.write("Select your interests and enter your last quiz score to get personalized content recommendations.")

# Sidebar (debug + data view)
with st.sidebar:
    st.header("Debug / Data View")
    if st.checkbox("Show loaded dataset"):
        st.dataframe(CONTENT_DF)

# Subjects for user selection
subjects = sorted(CONTENT_DF["subject"].dropna().unique().tolist())
if not subjects:
    subjects = ["Math", "Science", "History"]

# User inputs
interests = st.multiselect("Select your interests:", options=subjects)
score = st.slider("Enter your last quiz score:", 0, 100, 60)

# Recommendation button
if st.button("Get Recommendations"):
    try:
        if not interests:
            st.info("No interests selected — recommending top content based on score only.")

        results = recommend(interests, score, top_k=10)

        if results is None or results.empty:
            st.warning("No recommendations found. Try changing your inputs.")
        else:
            st.success(f"Found {len(results)} recommendation(s):")

            # Show each recommendation with quiz + video links
            for _, row in results.iterrows():
                st.markdown(f"### 📘 {row['title']}")
                st.write(
                    f"**Subject:** {row['subject']} | "
                    f"**Difficulty:** {row['difficulty']} | "
                    f"**Type:** {row.get('type','')}"
                )

                # Quiz link
                if 'quiz_link' in row and isinstance(row['quiz_link'], str) and row['quiz_link'].startswith("http"):
                    st.markdown(f"[📝 Take Quiz]({row['quiz_link']})", unsafe_allow_html=True)

                # Video link
                if 'video_link' in row and isinstance(row['video_link'], str) and row['video_link'].startswith("http"):
                    st.markdown(f"[🎥 Watch Video]({row['video_link']})", unsafe_allow_html=True)

                st.markdown("---")
    except Exception as e:
        st.error("An unexpected error occurred. See stack trace below:")
        st.exception(traceback.format_exc())
