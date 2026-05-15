import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "800"))

try:
    import groq
except ImportError:
    groq = None

client = None
if groq and GROQ_API_KEY:
    client = groq.Groq(api_key=GROQ_API_KEY)


def _groq_ready():
    if not groq:
        return False, "Groq SDK is not installed. Please install the `groq` package."
    if not GROQ_API_KEY:
        return False, "Groq API key not configured. Please add GROQ_API_KEY to your .env file."
    if not client:
        return False, "Groq client failed to initialize. Check your API key and environment."
    return True, None


def _extract_groq_text(response):
    try:
        return response.choices[0].message.content or ""
    except Exception:
        return str(response)


def _format_nutrition(nutrition_dict):
    """Format nutrition dictionary into readable text"""
    if not nutrition_dict:
        return "Not available"
    lines = []
    for key, value in nutrition_dict.items():
        if value:
            lines.append(f"**{key.title()}**: {value}")
    return "\n".join(lines) if lines else "Not available"


def _create_groq_completion(messages):
    ready, error = _groq_ready()
    if not ready:
        raise RuntimeError(error)

    return client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        temperature=GROQ_TEMPERATURE,
        max_completion_tokens=GROQ_MAX_TOKENS,
    )

def generate_recipe(ingredients, cuisine, diet_type):
    """Generate a recipe using Groq AI"""
    import json
    ready, error = _groq_ready()
    if not ready:
        return {"error": error}

    prompt = f"""Generate a recipe with these details:

Ingredients available: {ingredients}
Cuisine: {cuisine}
Diet type: {diet_type}

Format your response EXACTLY like this (include all headers):

Recipe Name: [name]

Ingredients:
[list each ingredient with quantity, one per line]

Cooking Steps:
[list each step numbered, one per line]

Cooking Time: [time]

Calories: [number]

Servings: [number]

Difficulty Level: [Easy/Medium/Hard]

Nutritional Information:
Protein: [amount]
Carbs: [amount]
Fats: [amount]
Fiber: [amount]

Healthy Alternatives:
[list alternatives, one per line]"""

    try:
        response = _create_groq_completion([
            {"role": "user", "content": prompt}
        ])
        text = _extract_groq_text(response).strip()
        
        print(f"DEBUG: Groq response received, length={len(text)}")
        
        # Parse the structured text response
        result = parse_recipe_response(text)
        result['raw_output'] = text
        
        # Fill in N/A values with defaults
        for key in ['recipe name', 'ingredients', 'cooking steps', 'cooking time', 'calories', 'serving size', 'difficulty level']:
            if key not in result or not result[key]:
                result[key] = 'N/A'
        
        return result

    except Exception as e:
        print(f"DEBUG: Exception in generate_recipe: {e}")
        return {"error": f"Error generating recipe: {str(e)}"}



def parse_recipe_response(response_text):
    """Parse the AI response into structured data with better header detection"""
    sections = {}
    lines = response_text.split('\n')
    current_section = None
    
    # Map various header formats to canonical section names
    header_map = {
        'recipe name': 'recipe name',
        'recipe': 'recipe name',
        'ingredients': 'ingredients',
        'cooking steps': 'cooking steps',
        'steps': 'cooking steps',
        'instructions': 'cooking steps',
        'cooking time': 'cooking time',
        'time': 'cooking time',
        'calories': 'calories',
        'cal': 'calories',
        'servings': 'serving size',
        'serving size': 'serving size',
        'yield': 'serving size',
        'difficulty': 'difficulty level',
        'difficulty level': 'difficulty level',
        'level': 'difficulty level',
        'nutritional information': 'nutritional information',
        'nutrition': 'nutritional information',
        'nutritional': 'nutritional information',
        'healthy alternatives': 'healthy alternatives',
        'alternatives': 'healthy alternatives',
        'substitutions': 'healthy alternatives',
    }
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check if this is a header line (contains ':' and matches known headers)
        is_header = False
        for header_key, canonical_name in header_map.items():
            if header_key in stripped.lower():
                # Make sure it's actually a header (ends with ':' or is the full line)
                if stripped.lower().startswith(header_key) and (stripped.endswith(':') or ':' in stripped):
                    current_section = canonical_name
                    if current_section not in sections:
                        sections[current_section] = []
                    is_header = True
                    
                    # If there's content after the ':', add it
                    if ':' in stripped:
                        content = stripped.split(':', 1)[1].strip()
                        if content:
                            sections[current_section].append(content)
                    break
        
        if not is_header and current_section:
            sections[current_section].append(stripped)
    
    # Join lines for each section
    result = {}
    for key, lines_list in sections.items():
        result[key] = '\n'.join(lines_list).strip()
    
    return result

def chat_with_ai(message, history):
    """Chat with AI assistant for cooking questions"""
    ready, error = _groq_ready()
    if not ready:
        return f"AI assistant is not available. {error}"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful cooking assistant. Answer questions about cooking, recipes, nutrition, and healthy eating."
        }
    ]
    for msg in history[-5:]:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})
    messages.append({"role": "user", "content": message})

    try:
        response = _create_groq_completion(messages)
        return _extract_groq_text(response)
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def generate_meal_plan(calories, days, diet_type):
    """Generate a meal plan"""
    ready, error = _groq_ready()
    if not ready:
        return {"error": error}

    prompt = f"""
    Generate a {days}-day meal plan for approximately {calories} calories per day.
    Diet type: {diet_type}

    Provide meals for breakfast, lunch, dinner, and 2 snacks per day.
    Include approximate calories for each meal.
    Make it healthy and balanced.

    Format as:
    Day 1:
    - Breakfast: [meal] ([calories] cal)
    - Snack 1: [meal] ([calories] cal)
    - Lunch: [meal] ([calories] cal)
    - Snack 2: [meal] ([calories] cal)
    - Dinner: [meal] ([calories] cal)

    And so on for each day.
    """

    try:
        response = _create_groq_completion([
            {"role": "user", "content": prompt}
        ])
        return _extract_groq_text(response)
    except Exception as e:
        return f"Error generating meal plan: {str(e)}"