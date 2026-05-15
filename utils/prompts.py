# Prompt templates for AI interactions

RECIPE_GENERATION_PROMPT = """
Generate a detailed recipe based on the following inputs:

Ingredients: {ingredients}
Cuisine: {cuisine}
Diet Type: {diet_type}

Please provide a structured response with the following sections:
1. Recipe Name
2. Ingredients (with quantities)
3. Cooking Steps
4. Cooking Time
5. Calories (per serving)
6. Nutritional Information (protein, carbs, fats, fiber)
7. Healthy Alternatives
8. Serving Size
9. Difficulty Level (Easy/Medium/Hard)

Make sure the recipe is practical, healthy, and matches the cuisine and diet preferences.
Format the response clearly with section headers.
"""

CHAT_PROMPT_TEMPLATE = """
You are a helpful cooking assistant. Answer questions about cooking, recipes, nutrition, and healthy eating.

Previous conversation:
{history}

User: {message}
Assistant:
"""

MEAL_PLAN_PROMPT = """
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