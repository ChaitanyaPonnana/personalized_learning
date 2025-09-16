import streamlit as st
from recommender import recommend

st.title("🎓 Personalized Learning Recommendation System")

# User inputs
interests = st.multiselect("Select your interests:", ["Math", "Science", "History"])
score = st.slider("Enter your last quiz score:", 0, 100, 50)

if st.button("Get Recommendations"):
    results = recommend(interests, score)
    if results.empty:
        st.write("No recommendations found. Try different interests/score.")
    else:
        st.write("### Recommended Content:")
        for _, row in results.iterrows():
            st.write(f"- *{row['title']}* ({row['subject']}, {row['difficulty']})")
