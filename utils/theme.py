import streamlit as st

def get_theme_css(theme):
    """Return CSS for the selected theme"""
    if theme == "dark":
        return """
        <style>
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
            background-color: #262730;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
        }
        .stButton>button:hover {
            background-color: #ff6b6b;
        }
        .card {
            background-color: #262730;
            border: 1px solid #4a4a4a;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .recipe-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            color: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .metric-card {
            background-color: #1f2937;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .sidebar {
            background-color: #0e1117;
        }
        </style>
        """
    else:  # light theme
        return """
        <style>
        .main {
            background-color: #ffffff;
            color: #000000;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
            background-color: #f8f9fa;
            color: #000000;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
        }
        .stButton>button:hover {
            background-color: #ff6b6b;
        }
        .card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .recipe-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            color: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .sidebar {
            background-color: #f8f9fa;
        }
        </style>
        """

def apply_theme(theme):
    """Apply the selected theme to the Streamlit app"""
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)