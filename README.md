# AI Smart Recipe Generator

A modern, AI-powered web application for generating smart recipes using available ingredients. Built with Python and Streamlit, featuring Groq AI integration.

## Features

- 🤖 AI Recipe Generator with ingredient input
- 🌍 Cuisine Selection (Indian, Chinese, Italian, Korean, Mexican, American)
- 🥗 Diet Type Filters (Weight Loss, High Protein, Keto, Vegan, Gym Diet, Diabetic Friendly)
- 📊 Smart Nutrition Analyzer with visualizations
- 📅 Meal Planner (Daily/Weekly/Calorie-based)
- 🎤 Voice Input for ingredients
- 💬 AI Cooking Assistant Chatbot
- 🌓 Light/Dark Mode Toggle
- 📱 Responsive Design

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: Groq
- **Libraries**: streamlit, groq, python-dotenv, pandas, plotly, numpy, requests, speechrecognition, gTTS, pyttsx3

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Groq API key

### Installation

1. **Clone or download the project**:
   ```bash
   cd ai_recipe_generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**:
   - Get your Groq API key from [Groq Console](https://console.groq.com)
   - Open `.env` file and set `GROQ_API_KEY=your_groq_api_key_here`
   - Optional settings:
     ```bash
     GROQ_MODEL=openai/gpt-oss-20b
     GROQ_TEMPERATURE=0.7
     GROQ_MAX_TOKENS=800
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**:
   - Open your browser and go to `http://localhost:8501`

## Project Structure

```
ai_recipe_generator/
│
├── app.py                    # Main Streamlit application
├── pages/
│   ├── meal_planner.py       # Meal planner page
│   ├── nutrition_dashboard.py # Nutrition dashboard page
│   ├── chatbot.py            # AI chatbot page
│
├── utils/
│   ├── prompts.py            # AI prompt templates
│   ├── api_handler.py        # Gemini API handler
│   ├── theme.py              # Theme management
│
├── assets/                   # Static assets (images, etc.)
│
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage

1. **Home**: Welcome page with overview
2. **Recipe Generator**: Enter ingredients, select cuisine and diet, generate recipes
3. **Nutrition Dashboard**: View nutritional analysis with charts
4. **Meal Planner**: Generate meal plans
5. **AI Chatbot**: Get cooking advice and answers

## Features Details

### AI Recipe Generator
- Input ingredients with quantities
- Select cuisine type
- Choose diet preferences
- Get complete recipes with cooking steps, nutrition info, and more

### Voice Input
- Click the microphone button to speak ingredients
- Speech is converted to text automatically

### Theme Toggle
- Switch between Light and Dark modes
- Theme preference is saved in session

### AI Chatbot
- Ask cooking questions
- Get ingredient substitutions
- Receive healthy cooking tips
- Conversation history maintained

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue on GitHub.