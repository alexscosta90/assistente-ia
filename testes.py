import yaml

with open("config.yml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

# Teste 1: nome e descrição
assert "nome" in CONFIG and CONFIG["nome"], "Campo 'nome' obrigatório"
assert "descricao" in CONFIG and CONFIG["descricao"], "Campo 'descricao' obrigatório"

# Teste 2: cor principal
assert CONFIG["cor_principal"].startswith("#"), "Cor principal deve estar em formato #RRGGBB"

# Teste 3: prompt
assert len(CONFIG["prompt_sistema"]) >= 80, "Prompt deve ter pelo menos 80 caracteres"
