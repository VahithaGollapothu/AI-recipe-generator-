import streamlit as st
import streamlit.components.v1 as components
from utils.theme import apply_theme
from pages.meal_planner import show_meal_planner
from pages.nutrition_dashboard import show_nutrition_dashboard
from pages.chatbot import show_chatbot
import speech_recognition as sr
from utils.api_handler import generate_recipe
import time

# Page configuration
st.set_page_config(
    page_title="AI Smart Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

if 'recipe_result' not in st.session_state:
    st.session_state.recipe_result = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Theme toggle
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Apply theme
apply_theme(st.session_state.theme)

# Sidebar
with st.sidebar:
    st.title("🍳 AI Recipe Generator")

    # Theme toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Theme: {st.session_state.theme.title()}")
    with col2:
        if st.button("🌓", key="theme_toggle"):
            toggle_theme()
            st.rerun()

    st.divider()

    # Navigation
    pages = {
        "🏠 Home": "home",
        "🍳 Recipe Generator": "recipe_generator",
        "📊 Nutrition Dashboard": "nutrition_dashboard",
        "📅 Meal Planner": "meal_planner",
        "💬 AI Chatbot": "chatbot"
    }

    for page_name, page_key in pages.items():
        if st.button(page_name, key=f"nav_{page_key}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_page == page_key else "secondary"):
            st.session_state.current_page = page_key
            st.rerun()

    st.divider()
    st.caption("© 2024 AI Recipe Generator")

# Main content
def show_home():
    st.title("🍳 Welcome to AI Smart Recipe Generator")
    st.markdown("""
    Transform your ingredients into delicious recipes with the power of AI!

    **Features:**
    - 🤖 AI-powered recipe generation
    - 🌍 Multiple cuisine options
    - 🥗 Diet-specific recipes
    - 📊 Nutrition analysis
    - 📅 Smart meal planning
    - 🎤 Voice input
    - 💬 Cooking assistant chatbot
    """)

    # Quick start
    st.subheader("🚀 Quick Start")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Try Recipe Generator:**
        1. Go to Recipe Generator
        2. Enter your ingredients
        3. Select cuisine & diet
        4. Get your AI recipe!
        """)

    with col2:
        st.markdown("""
        **Explore Features:**
        - Nutrition Dashboard for analysis
        - Meal Planner for weekly plans
        - AI Chatbot for cooking tips
        """)

def show_recipe_generator():
    st.title("🍳 AI Recipe Generator")

    # Input section
    col1, col2 = st.columns([2, 1])

    if st.session_state.get("voice_text_to_add"):
        current = st.session_state.get("ingredients_input", "")
        st.session_state["ingredients_input"] = (current + "\n" + st.session_state.pop("voice_text_to_add")).strip()

    with col1:
        st.subheader("Enter Your Ingredients")
        ingredients = st.text_area(
            "List your ingredients with quantities (one per line):",
            placeholder="2 eggs\n200g chicken\n1 onion\n100g rice",
            height=150,
            key="ingredients_input"
        )

        # Voice input
        if st.button("🎤 Voice Input", key="voice_input"):
            with st.spinner("Listening..."):
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("Speak your ingredients...")
                    try:
                        audio = recognizer.listen(source, timeout=5)
                        text = recognizer.recognize_google(audio)
                        st.session_state["voice_text_to_add"] = text
                    except sr.WaitTimeoutError:
                        st.error("No speech detected")
                    except sr.UnknownValueError:
                        st.error("Could not understand speech")
                    except sr.RequestError:
                        st.error("Speech recognition service unavailable")

    with col2:
        st.subheader("Preferences")
        cuisine = st.selectbox(
            "Cuisine",
            ["Any", "Indian", "Chinese", "Italian", "Korean", "Mexican", "American"],
            key="cuisine_select"
        )

        diet_type = st.selectbox(
            "Diet Type",
            ["Any", "Weight Loss", "High Protein", "Keto", "Vegan", "Gym Diet", "Diabetic Friendly"],
            key="diet_select"
        )

    # Generate button
    if st.button("🍳 Generate Recipe", type="primary", use_container_width=True):
        if not ingredients.strip():
            st.error("Please enter some ingredients!")
            return

        with st.spinner("Generating your recipe with AI..."):
            result = generate_recipe(ingredients, cuisine, diet_type)
            st.session_state.recipe_result = result

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Recipe generated successfully!")

    # Display result
    if st.session_state.recipe_result and "error" not in st.session_state.recipe_result:
        result = st.session_state.recipe_result

        # Recipe card
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        st.subheader(f"🍽️ {result.get('recipe name', 'Generated Recipe')}")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⏰ Cooking Time", result.get('cooking time', 'N/A'))
        with col2:
            st.metric("🔥 Calories", result.get('calories', 'N/A'))
        with col3:
            st.metric("🍽️ Servings", result.get('serving size', 'N/A'))
        with col4:
            st.metric("📊 Difficulty", result.get('difficulty level', 'N/A'))

        st.markdown('</div>', unsafe_allow_html=True)

        # Details in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Ingredients", "👨‍🍳 Steps", "🥗 Nutrition", "💡 Tips"])

        with tab1:
            st.markdown(result.get('ingredients', 'Ingredients not available'))

        with tab2:
            st.markdown(result.get('cooking steps', 'Cooking steps not available'))

        with tab3:
            nutrition = result.get('nutritional information', 'Nutrition info not available')
            st.markdown(f"**Nutritional Information:**\n{nutrition}")

        with tab4:
            alternatives = result.get('healthy alternatives', 'Healthy alternatives not available')
            st.markdown(f"**Healthy Alternatives:**\n{alternatives}")
            # Show raw AI output when structured fields are missing
            raw = result.get('raw_output')
            if raw:
                st.divider()
                with st.expander("Raw AI output (fallback)"):
                    st.code(raw, language='text')

# Main app logic
if st.session_state.current_page == "home":
    show_home()
elif st.session_state.current_page == "recipe_generator":
    show_recipe_generator()
elif st.session_state.current_page == "nutrition_dashboard":
    show_nutrition_dashboard()
elif st.session_state.current_page == "meal_planner":
    show_meal_planner()
elif st.session_state.current_page == "chatbot":
    show_chatbot()
else:
    show_home()