import streamlit as st
try:
    import plotly.graph_objects as go
    import plotly.express as px
    _PLOTLY_AVAILABLE = True
except Exception:
    go = None
    px = None
    _PLOTLY_AVAILABLE = False
import pandas as pd
import numpy as np

def show_nutrition_dashboard():
    st.title("📊 Nutrition Dashboard")

    st.markdown("""
    Analyze nutritional content and track your dietary goals with interactive visualizations.
    """)

    # Sample data or use from recipe
    if st.session_state.get('recipe_result') and 'nutritional information' in st.session_state.recipe_result:
        # Parse nutrition from recipe
        nutrition_text = st.session_state.recipe_result['nutritional information']
        # Simple parsing - in real app, you'd have structured data
        sample_nutrition = {
            'protein': 25,
            'carbs': 45,
            'fats': 15,
            'fiber': 8,
            'calories': 350
        }
    else:
        # Sample data
        sample_nutrition = {
            'protein': 25,
            'carbs': 45,
            'fats': 15,
            'fiber': 8,
            'calories': 350
        }

    # Nutrition overview
    st.subheader("🥗 Nutritional Breakdown")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🔥 Calories", f"{sample_nutrition['calories']}")
    with col2:
        st.metric("🥩 Protein", f"{sample_nutrition['protein']}g")
    with col3:
        st.metric("🌾 Carbs", f"{sample_nutrition['carbs']}g")
    with col4:
        st.metric("🧈 Fats", f"{sample_nutrition['fats']}g")
    with col5:
        st.metric("🥦 Fiber", f"{sample_nutrition['fiber']}g")

    # Macronutrient distribution
    st.subheader("📊 Macronutrient Distribution")

    # Pie chart
    labels = ['Protein', 'Carbs', 'Fats']
    values = [sample_nutrition['protein'], sample_nutrition['carbs'], sample_nutrition['fats']]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    if _PLOTLY_AVAILABLE:
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            title="Macronutrients (g)"
        )])
        fig_pie.update_layout(
            font=dict(size=14),
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Interactive charts are unavailable because `plotly` is not installed.")
        st.write("Macronutrients:")
        for k, v in zip(labels, values):
            st.write(f"- {k}: {v}g")

    # Progress bars
    st.subheader("🎯 Daily Goals Progress")

    # Sample daily goals
    daily_goals = {
        'calories': 2000,
        'protein': 150,
        'carbs': 250,
        'fats': 70,
        'fiber': 25
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Calories**")
        progress = min(sample_nutrition['calories'] / daily_goals['calories'], 1.0)
        st.progress(progress)
        st.caption(f"{sample_nutrition['calories']}/{daily_goals['calories']} cal")

        st.markdown("**Protein**")
        progress = min(sample_nutrition['protein'] / daily_goals['protein'], 1.0)
        st.progress(progress)
        st.caption(f"{sample_nutrition['protein']}g/{daily_goals['protein']}g")

        st.markdown("**Fiber**")
        progress = min(sample_nutrition['fiber'] / daily_goals['fiber'], 1.0)
        st.progress(progress)
        st.caption(f"{sample_nutrition['fiber']}g/{daily_goals['fiber']}g")

    with col2:
        st.markdown("**Carbs**")
        progress = min(sample_nutrition['carbs'] / daily_goals['carbs'], 1.0)
        st.progress(progress)
        st.caption(f"{sample_nutrition['carbs']}g/{daily_goals['carbs']}g")

        st.markdown("**Fats**")
        progress = min(sample_nutrition['fats'] / daily_goals['fats'], 1.0)
        st.progress(progress)
        st.caption(f"{sample_nutrition['fats']}g/{daily_goals['fats']}g")

    # Weekly nutrition trend (sample data)
    st.subheader("📈 Weekly Nutrition Trend")

    # Generate sample weekly data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekly_calories = np.random.normal(sample_nutrition['calories'], 50, 7)
    weekly_protein = np.random.normal(sample_nutrition['protein'], 5, 7)

    if _PLOTLY_AVAILABLE:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=days,
            y=weekly_calories,
            mode='lines+markers',
            name='Calories',
            line=dict(color='#FF6B6B', width=3)
        ))
        fig_line.add_trace(go.Scatter(
            x=days,
            y=weekly_protein,
            mode='lines+markers',
            name='Protein (g)',
            line=dict(color='#4ECDC4', width=3)
        ))

        fig_line.update_layout(
            title="Weekly Nutrition Tracking",
            xaxis_title="Day",
            yaxis_title="Amount",
            font=dict(size=14)
        )

        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Interactive charts are unavailable because `plotly` is not installed.")
        st.write("Weekly calories:")
        for d, c in zip(days, weekly_calories.tolist()):
            st.write(f"- {d}: {int(c)} cal")

    # Nutrition tips
    with st.expander("💡 Nutrition Tips"):
        st.markdown("""
        **Protein Sources:**
        - Lean meats, fish, eggs
        - Dairy products, legumes
        - Nuts and seeds

        **Healthy Carbs:**
        - Whole grains, vegetables
        - Fruits, legumes
        - Avoid processed sugars

        **Healthy Fats:**
        - Avocados, nuts, olive oil
        - Fatty fish, seeds
        - Limit saturated fats

        **Fiber Rich Foods:**
        - Vegetables, fruits
        - Whole grains, legumes
        - Nuts and seeds
        """)

    # Export data
    if st.button("📥 Export Nutrition Data"):
        # Sample export functionality
        nutrition_df = pd.DataFrame([sample_nutrition])
        csv = nutrition_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="nutrition_data.csv",
            mime="text/csv"
        )