import ast, traceback
path = 'd:/vahitha/ai_recipe_generator/app.py'
try:
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    ast.parse(src, filename=path)
    print('PARSE_OK')
except Exception:
    traceback.print_exc()
