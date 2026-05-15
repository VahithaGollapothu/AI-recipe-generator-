import streamlit as st
from utils.api_handler import generate_meal_plan

def show_meal_planner():
    st.title("📅 AI Meal Planner")

    st.markdown("""
    Generate personalized meal plans based on your calorie goals and dietary preferences.
    """)

    col1, col2 = st.columns(2)

    with col1:
        calories = st.number_input(
            "Daily Calorie Goal",
            min_value=1200,
            max_value=4000,
            value=2000,
            step=100
        )

        days = st.selectbox(
            "Plan Duration",
            [1, 3, 7, 14, 30],
            index=2  # Default to 7 days
        )

    with col2:
        diet_type = st.selectbox(
            "Diet Type",
            ["Balanced", "Weight Loss", "High Protein", "Keto", "Vegan", "Gym Diet", "Diabetic Friendly"]
        )

        # Additional preferences
        st.subheader("Preferences")
        include_snacks = st.checkbox("Include Snacks", value=True)
        vegetarian = st.checkbox("Vegetarian Options")

    if st.button("🍽️ Generate Meal Plan", type="primary", use_container_width=True):
        with st.spinner("Creating your personalized meal plan..."):
            plan = generate_meal_plan(calories, days, diet_type)

        if isinstance(plan, dict) and "error" in plan:
            st.error(plan["error"])
        else:
            st.success("Meal plan generated!")

            # Display plan
            st.subheader("📋 Your Meal Plan")

            # Parse and display the plan
            lines = plan.split('\n')
            current_day = None

            for line in lines:
                if line.strip().startswith('Day'):
                    current_day = line.strip()
                    st.markdown(f"### {current_day}")
                elif line.strip().startswith('-'):
                    st.markdown(line.strip())
                elif line.strip():
                    st.write(line.strip())

            # Summary
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Days", days)
            with col2:
                st.metric("Daily Calories", f"~{calories}")
            with col3:
                st.metric("Diet Type", diet_type)

            # Tips
            with st.expander("💡 Meal Planning Tips"):
                st.markdown("""
                - Adjust portion sizes based on your activity level
                - Stay hydrated throughout the day
                - Include variety in your meals
                - Consult a nutritionist for personalized advice
                - Track your actual calorie intake vs. planned
                """)

    # Sample meal plan preview
    with st.expander("👀 Sample Meal Plan"):
        st.markdown("""
        **Day 1:**
        - Breakfast: Oatmeal with berries (300 cal)
        - Snack 1: Greek yogurt (150 cal)
        - Lunch: Grilled chicken salad (400 cal)
        - Snack 2: Apple with almond butter (200 cal)
        - Dinner: Baked salmon with vegetables (450 cal)

        **Total: ~1,500 calories**

        *This is just a sample. Generate your personalized plan above!*
        """)