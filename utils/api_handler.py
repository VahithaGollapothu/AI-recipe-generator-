import os
import re
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "2000"))

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
        pass
    try:
        return response.choices[0].text or ""
    except Exception:
        pass
    try:
        return response.content or ""
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

def _extract_json_object(text):
    start = text.find('{')
    if start == -1:
        return None

    brace_count = 0
    in_string = False
    escape = False
    for i, ch in enumerate(text[start:], start):
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0:
                return text[start:i + 1]

    last_close = text.rfind('}')
    if last_close > start:
        return text[start:last_close + 1]
    return None


def _continue_truncated_json(partial_text):
    prompt = (
        "The previous response was a partial JSON object that was cut off. "
        "Continue the JSON object from the last valid point and return only valid JSON with no explanation. "
        "Do not include any text outside the JSON object."
    )
    return _extract_groq_text(
        _create_groq_completion([
            {"role": "system", "content": "You are a JSON completion assistant."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": partial_text}
        ])
    )


def _try_parse_json_text(text):
    import json
    try:
        return json.loads(text)
    except Exception:
        pass

    json_obj = _extract_json_object(text)
    if json_obj:
        try:
            return json.loads(json_obj)
        except Exception:
            pass

    if text.strip().startswith('{') and not text.strip().endswith('}'):
        continued = _continue_truncated_json(text)
        try:
            return json.loads(continued)
        except Exception:
            combined = text + '\n' + continued
            try:
                return json.loads(combined)
            except Exception:
                pass

    return _extract_json_like_recipe(text)


def _extract_json_value(text, key):
    # match both quoted string values and numeric values
    string_match = re.search(rf'"{re.escape(key)}"\s*:\s*"([^"]*)"', text, re.IGNORECASE)
    if string_match:
        return string_match.group(1).strip()
    number_match = re.search(rf'"{re.escape(key)}"\s*:\s*([0-9]+(?:\.[0-9]+)?)', text, re.IGNORECASE)
    if number_match:
        return number_match.group(1).strip()
    return None


def _extract_json_array(text, key):
    array_match = re.search(rf'"{re.escape(key)}"\s*:\s*\[([^\]]*)\]', text, re.IGNORECASE | re.DOTALL)
    if not array_match:
        return []
    items = re.findall(r'"([^"]*)"', array_match.group(1))
    return [item.strip() for item in items if item.strip()]


def _extract_json_object_fields(text, key):
    obj_match = re.search(rf'"{re.escape(key)}"\s*:\s*\{{([^\}}]*)\}}', text, re.IGNORECASE | re.DOTALL)
    if not obj_match:
        return {}
    fields = {}
    for match in re.finditer(r'"([^"]+)"\s*:\s*"([^"]*)"', obj_match.group(1)):
        fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def _extract_json_like_recipe(text):
    recipe = {}
    recipe['recipe name'] = _extract_json_value(text, 'recipe name') or _extract_json_value(text, 'recipe_name')
    recipe['ingredients'] = _extract_json_array(text, 'ingredients')
    recipe['cooking steps'] = _extract_json_array(text, 'cooking steps') or _extract_json_array(text, 'cooking_steps')
    recipe['cooking time'] = _extract_json_value(text, 'cooking time') or _extract_json_value(text, 'cooking_time') or _extract_json_value(text, 'time')
    recipe['calories'] = _extract_json_value(text, 'calories')
    recipe['serving size'] = _extract_json_value(text, 'serving size') or _extract_json_value(text, 'servings') or _extract_json_value(text, 'serving_size')
    recipe['difficulty level'] = _extract_json_value(text, 'difficulty level') or _extract_json_value(text, 'difficulty')
    nutrition = _extract_json_object_fields(text, 'nutritional information') or _extract_json_object_fields(text, 'nutrition')
    if nutrition:
        recipe['nutritional information'] = '\n'.join(f"{k.title()}: {v}" for k, v in nutrition.items())
    recipe['healthy alternatives'] = '\n'.join(_extract_json_array(text, 'healthy alternatives') or _extract_json_array(text, 'healthy_alternatives') or _extract_json_array(text, 'alternatives'))
    if any(recipe.values()):
        return recipe
    return None


def _normalize_recipe_dict(recipe_dict):
    """Normalize recipe data from parsed JSON into the app's canonical field names."""
    field_map = {
        'recipe_name': 'recipe name',
        'recipe name': 'recipe name',
        'recipe': 'recipe name',
        'ingredients': 'ingredients',
        'cooking_steps': 'cooking steps',
        'cooking steps': 'cooking steps',
        'steps': 'cooking steps',
        'instructions': 'cooking steps',
        'cooking_time': 'cooking time',
        'cooking time': 'cooking time',
        'time': 'cooking time',
        'calories': 'calories',
        'servings': 'serving size',
        'serving_size': 'serving size',
        'serving size': 'serving size',
        'difficulty': 'difficulty level',
        'difficulty_level': 'difficulty level',
        'difficulty level': 'difficulty level',
        'nutritional_information': 'nutritional information',
        'nutritional information': 'nutritional information',
        'nutrition': 'nutritional information',
        'healthy_alternatives': 'healthy alternatives',
        'healthy alternatives': 'healthy alternatives',
        'alternatives': 'healthy alternatives',
        'substitutions': 'healthy alternatives'
    }

    normalized = {}
    for key, value in recipe_dict.items():
        canonical = field_map.get(key.lower().strip(), key.lower().strip())
        if isinstance(value, list):
            normalized[canonical] = '\n'.join(str(item).strip() for item in value if item)
        elif isinstance(value, dict):
            normalized[canonical] = '\n'.join(f"{subkey.title()}: {subvalue}" for subkey, subvalue in value.items() if subvalue)
        else:
            normalized[canonical] = str(value).strip()
    return normalized


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

Return only valid JSON with the following fields:
- recipe name
- ingredients
- cooking steps
- cooking time
- calories
- serving size
- difficulty level
- nutritional information
- healthy alternatives

For ingredients and cooking steps, use arrays of strings.
For nutritional information, use an object with protein, carbs, fats, and fiber.

If JSON is not possible, return the information in plain text sections with headers exactly like this, one section per line:
Recipe Name:
Ingredients:
Cooking Steps:
Cooking Time:
Calories:
Servings:
Difficulty Level:
Nutritional Information:
Healthy Alternatives:

Do not include any extra commentary, explanations, or markdown formatting outside the requested fields.
"""

    try:
        response = _create_groq_completion([
            {"role": "user", "content": prompt}
        ])
        text = _extract_groq_text(response).strip()
        print(f"DEBUG: Groq response received, length={len(text)}")

        result = {}
        parsed = _try_parse_json_text(text)
        if isinstance(parsed, dict):
            result = _normalize_recipe_dict(parsed)

        if not result:
            result = parse_recipe_response(text)

        result['raw_output'] = text

        for key in ['recipe name', 'ingredients', 'cooking steps', 'cooking time', 'calories', 'serving size', 'difficulty level', 'nutritional information', 'healthy alternatives']:
            if key not in result or not result[key]:
                result[key] = 'N/A'

        return result

    except Exception as e:
        print(f"DEBUG: Exception in generate_recipe: {e}")
        return {"error": f"Error generating recipe: {str(e)}"}



def parse_recipe_response(response_text):
    """Parse the AI response into structured data with better header detection."""
    sections = {}
    lines = response_text.split('\n')
    current_section = None

    header_map = {
        'recipe name': 'recipe name',
        'recipe': 'recipe name',
        'name': 'recipe name',
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

    header_regex = re.compile(
        r'^(?P<header>recipe name|recipe|name|ingredients|cooking steps|steps|instructions|cooking time|time|calories|cal|servings|serving size|yield|difficulty level|difficulty|level|nutritional information|nutrition|nutritional|healthy alternatives|alternatives|substitutions)\s*(?:[:\-–—])?\s*(?P<content>.*)$',
        re.IGNORECASE
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        match = header_regex.match(stripped)
        if match:
            header_key = match.group('header').lower().strip()
            canonical_name = header_map.get(header_key, header_key)
            current_section = canonical_name
            if current_section not in sections:
                sections[current_section] = []

            content = match.group('content').strip()
            if content:
                sections[current_section].append(content)
            continue

        if current_section:
            sections[current_section].append(stripped)

    result = {}
    for key, lines_list in sections.items():
        result[key] = '\n'.join(lines_list).strip()

    # Handle cases where calories/servings/difficulty are provided inline but not in a section
    if 'calories' not in result:
        inline = re.search(r'^(?:calories|cal)\s*[:\-–—]?\s*(\d+\s*(?:kcal|cal|calories)?)$', response_text, re.IGNORECASE | re.MULTILINE)
        if inline:
            result['calories'] = inline.group(1).strip()

    if 'serving size' not in result:
        inline = re.search(r'^(?:servings|serving size|yield)\s*[:\-–—]?\s*(\d+)', response_text, re.IGNORECASE | re.MULTILINE)
        if inline:
            result['serving size'] = inline.group(1).strip()

    if 'difficulty level' not in result:
        inline = re.search(r'^(?:difficulty level|difficulty|level)\s*[:\-–—]?\s*(.+)$', response_text, re.IGNORECASE | re.MULTILINE)
        if inline:
            result['difficulty level'] = inline.group(1).strip()

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