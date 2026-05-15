import streamlit as st
from utils.api_handler import chat_with_ai

def show_chatbot():
    st.title("💬 AI Cooking Assistant")

    st.markdown("""
    Ask me anything about cooking, recipes, nutrition, or healthy eating!
    I'm here to help you become a better cook.
    """)

    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(message["user"])
            with st.chat_message("assistant"):
                st.write(message["assistant"])

    # Chat input
    if prompt := st.chat_input("Ask me about cooking..."):
        # Add user message to history
        st.session_state.chat_history.append({"user": prompt, "assistant": ""})

        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)

        # Generate AI response
        with st.spinner("Thinking..."):
            response = chat_with_ai(prompt, st.session_state.chat_history[:-1])  # Exclude current message

        # Update history with response
        st.session_state.chat_history[-1]["assistant"] = response

        # Display assistant response
        with chat_container:
            with st.chat_message("assistant"):
                st.write(response)

    # Clear chat
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("💡 Cooking Tips", type="secondary"):
            quick_tips = """
            Here are some quick cooking tips:

            🍳 **Basic Techniques:**
            - Always preheat your pans
            - Salt pasta water generously
            - Rest meat after cooking

            🥗 **Healthy Cooking:**
            - Use olive oil instead of butter
            - Steam vegetables to retain nutrients
            - Add herbs and spices for flavor without calories

            ⏰ **Time Savers:**
            - Prep ingredients before starting
            - Use one-pot meals
            - Cook in batches for meal prep

            Ask me for more specific advice!
            """
            st.info(quick_tips)

    # Suggested questions
    with st.expander("❓ Suggested Questions"):
        st.markdown("""
        Try asking me:
        - "How do I substitute eggs in baking?"
        - "What's the difference between baking soda and baking powder?"
        - "How to make crispy roasted vegetables?"
        - "Calorie content of common foods"
        - "Healthy alternatives to fried foods"
        - "How to cook perfect rice every time"
        - "Best spices for different cuisines"
        - "Meal prep ideas for the week"
        """)

    # Chat statistics
    if st.session_state.chat_history:
        with st.expander("📊 Chat Statistics"):
            total_messages = len(st.session_state.chat_history)
            user_messages = len([m for m in st.session_state.chat_history if m["user"]])
            ai_messages = len([m for m in st.session_state.chat_history if m["assistant"]])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Messages", total_messages)
            with col2:
                st.metric("Your Questions", user_messages)
            with col3:
                st.metric("AI Responses", ai_messages)