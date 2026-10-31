import streamlit as st
from google import genai

# 1. Page Configuration & Modern Styling
st.set_page_config(
    page_title="Letterboxd AI Cinematic Engine",
    page_icon="🎬",
    layout="wide",
)

# Custom CSS for a sleek, dark-themed cinematic UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #b20710;
        color: white;
    }
    .css-1544g2n {
        padding-top: 2rem;
    }
    .card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🎬 Letterboxd AI Cinematic Recommender")
st.markdown("Upload your Letterboxd CSV, set your pre-flight preferences, and unlock hyper-targeted hidden gems and masterpieces tailored strictly to your taste.")
st.markdown("---")

# Sidebar for API Key & File Upload
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="AIzaSy...")
    
    st.markdown("---")
    st.header("📁 Data Source")
    uploaded_file = st.file_uploader("Upload Letterboxd CSV", type=["csv"])
    
    st.markdown("---")
    st.markdown("💡 *Tip: Export your watched history directly from your Letterboxd account settings.*")

# Main Content Layout using Columns for Preferences
st.subheader("🎯 Pre-flight Preferences")

col1, col2 = st.columns(2)

with col1:
    q1 = st.radio(
        "1. Strictly Family-Friendly? (Zero adult/sexual scenes)",
        ["No / Skip (Anything goes)", "Yes"],
    )
    q3 = st.text_input(
        "3. Specific mood or genre bias?",
        placeholder="e.g., Mind-bending thriller, Feel-good",
    )
    q5 = st.text_input(
        "5. Blacklist Directors/Actors/Franchises?",
        placeholder="Leave blank if none",
    )

with col2:
    q2 = st.text_input(
        "2. Country restriction?",
        placeholder="e.g., India, South Korea, Hollywood (Blank for global)",
    )
    q4 = st.text_input(
        "4. Era preference?",
        placeholder="e.g., Post-2015, Pre-2000 (Blank for mix)",
    )
    q6 = st.text_input(
        "6. Runtime constraint?",
        placeholder="e.g., Under 2 hours, or open epics",
    )

st.markdown("---")

# Generate Action Area
if st.button("🚀 Generate Curated Recommendations"):
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key in the sidebar first!")
    elif uploaded_file is None:
        st.error("⚠️ Please upload your Letterboxd CSV file in the sidebar!")
    else:
        with st.spinner("🔄 Parsing your CSV, analyzing technical crew DNA, and curating recommendations..."):
            try:
                # Read CSV content
                csv_data = uploaded_file.getvalue().decode("utf-8")

                # Initialize Gemini Client with correct model
                client = genai.Client(api_key=api_key)

                # System Instructions (Aap apna poora lamba role aur formatting rules yahan daal sakte hain)
                system_instructions = """You are an elite, highly sophisticated cinematic data scientist and expert film recommendation engine. 
                Ingest the user's Letterboxd CSV, analyze their ratings (3.0 to 5.0 scale), filter out low scores, and follow all user pre-flight constraints strictly. 
                Provide results in three sections: Taste Profile Summary, The Masterpiece Cohort (5 films), and The Excellent/Good Cohort (5 films) using the exact requested formatting."""

                user_prompt = f"""
                Here is my Letterboxd CSV data:
                {csv_data}

                Here are my answers to the 6 pre-flight questions:
                1. Family Friendly: {q1}
                2. Country: {q2 if q2 else 'BLANK/SKIP'}
                3. Mood/Genre: {q3 if q3 else 'BLANK/SKIP'}
                4. Era: {q4 if q4 else 'BLANK/SKIP'}
                5. Blacklist: {q5 if q5 else 'BLanking/SKIP'}
                6. Runtime: {q6 if q6 else 'BLANK/SKIP'}
                """

                # Updated model call using gemini-3.8-flash
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=user_prompt,
                    config={
                        "system_instruction": system_instructions,
                        "temperature": 0.7,
                    },
                )

                st.success("✨ Your personalized cinematic report is ready!")
                
                # Display output inside a clean card container
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
