import sys
sys.path.insert(0, r'd:/vahitha/ai_recipe_generator')

try:
    import app
    import pages.meal_planner as mp
    import pages.chatbot as cb
    import pages.nutrition_dashboard as nd
    import utils.api_handler as api
    print('IMPORT_OK')
    print('meal', hasattr(mp, 'show_meal_planner'))
    print('chat', hasattr(cb, 'show_chatbot'))
    print('nutrition', hasattr(nd, 'show_nutrition_dashboard'))
    print('api_gen', hasattr(api, 'generate_recipe'))
except Exception:
    import traceback
    traceback.print_exc()
