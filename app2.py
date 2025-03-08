import streamlit as st
import google.generativeai as genai

# Hardcode the API key (not recommended for production)
GOOGLE_API_KEY = "AIzaSyD_jB8En_E4vhuuTBiE9Ial1Zny2TwTM0c"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get AI response
def get_fitness_advice(user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text
    except genai.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Streamlit UI Setup
st.set_page_config(page_title="FitSync AI", page_icon="🏋", layout="wide")

# User Details Page
if "page" not in st.session_state:
    st.session_state.page = "details"

if st.session_state.page == "details":
    st.title("Welcome to FitSync AI")
    st.write("Please enter your details to personalize your fitness journey.")
    
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=16, max_value=100, step=1)
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=300, step=1)
    fitness_goal = st.text_area("What is your fitness goal?")
    fitness_stage = st.selectbox("Fitness Stage", ["", "Beginner", "Intermediate", "Advanced"])
    
    if st.button("Get Started"):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "main":
    # Custom CSS for Modern Design
    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            .header {
                background: linear-gradient(135deg, #ff6f61, #ffcc00);
                padding: 40px;
                text-align: center;
                color: white;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .header h1 {
                font-size: 48px;
                font-weight: bold;
                margin: 0;
            }
            .header p {
                font-size: 18px;
                margin: 10px 0 0;
            }
            .video-container {
                margin-top: 20px;
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header Section
    st.markdown(
        """
        <div class="header">
            <h1>FitSync AI</h1>
            <p>Your Personal Fitness Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search Bar with Images
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.image("https://th.bing.com/th/id/OIP.QiOI4YknDbOIGlFp6X6ZXAHaEu?w=273&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", use_container_width=True)

    with col2:
        user_query = st.text_input(
            "Search for fitness advice",  # Label for accessibility
            placeholder="e.g., Best leg day exercises",
            key="search",
            help="Type your fitness goal or question",
            label_visibility="collapsed"  # Hide the label visually
        )

    with col3:
        st.image("https://th.bing.com/th/id/OIP.FjOxznpWXmSBXRkoB0JtFQHaEq?w=265&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", use_container_width=True)

    # Floating Bar for Muscle Selection
    st.sidebar.header("Customize Your Workout")
    muscle_group = st.sidebar.selectbox("Select Muscle Group", ["", "Chest", "Back", "Legs", "Arms", "Shoulders", "Core"])
    sub_muscle = ""
    if muscle_group == "Back":
        sub_muscle = st.sidebar.selectbox("Target Sub-Muscle", ["", "Lats", "Traps", "Rhomboids"])
    elif muscle_group == "Legs":
        sub_muscle = st.sidebar.selectbox("Target Sub-Muscle", ["", "Quads", "Hamstrings", "Calves"])
    elif muscle_group == "Arms":
        sub_muscle = st.sidebar.selectbox("Target Sub-Muscle", ["", "Biceps - Short Head", "Biceps - Long Head", "Triceps - Long Head", "Triceps - Lateral Head", "Triceps - Medial Head"])
    elif muscle_group == "Shoulders":
        sub_muscle = st.sidebar.selectbox("Target Sub-Muscle", ["", "Front Delts", "Side Delts", "Rear Delts"])
    elif muscle_group == "Core":
        sub_muscle = st.sidebar.selectbox("Target Sub-Muscle", ["", "Upper Abs", "Lower Abs", "Obliques", "Transverse Abdominis"])
    elif muscle_group == "Chest":
        sub_muscle = st.sidebar.selectbox("Target Sub-Muscle", ["", "Upper Chest", "Middle Chest", "Lower Chest", "Inner Chest", "Outer Chest"])

    training_type = st.sidebar.selectbox("Select Training Type", ["", "Bodybuilding", "Powerlifting", "Calisthenics", "CrossFit", "Strongman", "Compound Lifting (Deadlifts, Squats, Bench Press)"])
    intensity = st.sidebar.selectbox("Workout Intensity", ["", "Light", "Moderate", "Intense", "Extreme"])

    # Fitness Stage Logic
    fitness_stage = st.session_state.get("fitness_stage", "")
    if fitness_stage == "Beginner":
        st.sidebar.warning("💡 As a beginner, we recommend hitting the gym and working with a professional trainer for at least 15 days to understand your body's adaptability and conditions.")

    # Generate Workout Plan
    if st.button("💡 Generate Workout Plan", key="generate", help="Click to generate a workout plan"):
        if not user_query.strip():
            st.warning("⚠ Please enter a valid fitness-related query.")
        else:
            with st.spinner("⏳ Generating workout plan..."):
                final_query = f"{user_query}. Fitness stage: {fitness_stage}. Last workout intensity: {intensity}."
                if muscle_group:
                    final_query += f" Focus on {muscle_group}."
                if sub_muscle:
                    final_query += f" Targeting {sub_muscle}."
                if training_type:
                    final_query += f" Training type: {training_type}."
                final_query += " Provide the number of reps and sets for each exercise. Include rest periods of 1-1.5 minutes between sets. Also, remind the user to re-rack weights after completing their workout."
                advice = get_fitness_advice(final_query)

                # Add workout video links and sleep cycle recommendations
                workout_videos = {
                    "Chest": "https://www.youtube.com/watch?v=bps0uIgf6dg",
                    "Back": "https://www.youtube.com/watch?v=w1eQ67dLsgA",
                    "Legs": "https://www.youtube.com/watch?v=MzeiSTQtuyw",
                    "Arms": "https://www.youtube.com/watch?v=o9zCgPtsups",
                    "Shoulders": "https://www.youtube.com/watch?v=MzeiSTQtuyw",
                    "Core": "https://www.youtube.com/watch?v=RarcD0Q50nU",
                }

                sleep_cycle_recommendation = {
                    "Beginner": "9-10 hours of sleep per night. Focus on consistency and quality sleep concentrate on fueling carbs.",
                    "Intermediate": "7-9 hours of sleep per night. Consider tracking sleep stages using a wearable device concentrate on protein intake also mind muscle connection.",
                    "Advanced": "6-8 hours of sleep per night. Optimize sleep hygiene and recovery strategies concentrate on diet because body is made in kitchen .",
                }

                # Display Workout Plan
                st.markdown(
                    f"""
                    <div class='workout-plan'>
                        <h3>🤖 Your Workout Plan:</h3>
                        {advice.replace("\n", "<br>")}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Display Workout Videos
                if muscle_group in workout_videos:
                    st.markdown("### 🎥 Recommended Workout Videos")
                    st.video(workout_videos[muscle_group])

                # Display Sleep Cycle Recommendation
                if fitness_stage in sleep_cycle_recommendation:
                    st.markdown("### 😴 Recommended Sleep Cycle")
                    st.info(sleep_cycle_recommendation[fitness_stage])

    # Footer
    st.markdown(
        "<div class='footer'>Developed by Team Shouryanga | Powered by Llama3</div>",
        unsafe_allow_html=True,
    )
