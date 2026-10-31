import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(
    page_title="Letterboxd AI Recommender", page_icon="🎬", layout="centered"
)

st.title("🎬 Letterboxd AI Cinematic Engine")
st.write(
    "Upload your Letterboxd CSV, set your preferences, and get hyper-targeted recommendations!"
)

# 2. Gemini API Key Input (Aap isko st.secrets mein bhi rakh sakte hain)
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# 3. File Uploader for CSV
uploaded_file = st.file_uploader(
    "Upload your Letterboxd CSV file", type=["csv"]
)

# 4. Interactive Protocol Questions UI
st.subheader("Pre-flight Preferences")
q1 = st.radio(
    "1. Strictly Family-Friendly with ZERO adult/sexual scenes?",
    ["No / Skip (Anything goes)", "Yes"],
)
q2 = st.text_input(
    "2. Country restriction? (e.g., India, South Korea, Hollywood, or leave blank):"
)
q3 = st.text_input(
    "3. Specific mood or genre bias? (Leave blank for open history):"
)
q4 = st.text_input(
    "4. Era preference? (e.g., Post-2015, Pre-2000, or leave blank):"
)
q5 = st.text_input(
    "5. Directors/Actors/Franchises to BLACKLIST? (Leave blank if none):"
)
q6 = st.text_input(
    "6. Runtime constraint? (e.g., Under 2 hours, or leave blank):"
)

# 5. Generate Button Logic
if st.button("Generate Recommendations"):
  if not api_key:
    st.error("Please enter your Gemini API key first!")
  elif uploaded_file is None:
    st.error("Please upload your Letterboxd CSV file!")
  else:
    with st.spinner("Analyzing your cinematic DNA and parsing CSV..."):
      try:
        # CSV content ko read karo
        csv_data = uploaded_file.getvalue().decode("utf-8")

        # Initialize Gemini Client
        client = genai.Client(api_key=api_key)

        # Aapka poora System Prompt yahan define hoga
        system_instructions = """[Yahan apna poora lamba role, rating scale, quality control, aur formatting rules wala system prompt paste kar dena]"""

        # User ka dynamic input assemble karo
        user_prompt = f"""
                Here is my Letterboxd CSV data:
                {csv_data}

                Here are my answers to the 6 pre-flight questions:
                1. Family Friendly: {q1}
                2. Country: {q2 if q2 else 'BLANK/SKIP'}
                3. Mood/Genre: {q3 if q3 else 'BLANK/SKIP'}
                4. Era: {q4 if q4 else 'BLANK/SKIP'}
                5. Blacklist: {q5 if q5 else 'BLANK/SKIP'}
                6. Runtime: {q6 if q6 else 'BLANK/SKIP'}
                """

        # Gemini API call (using gemini-2.5-flash or standard model)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config={
                "system_instruction": system_instructions,
                "temperature": 0.7,
            },
        )

        st.success("Here are your custom recommendations!")
        st.markdown(response.text)

      except Exception as e:
        st.error(f"An error occurred: {e}")