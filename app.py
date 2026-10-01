import gradio as gr
import os
import yaml
import openai

# Lê config.yml
with open("config.yml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

# Pega chave do ambiente
CHAVE = os.environ.get("OPENROUTER_API_KEY")

if not CHAVE:
    raise ValueError("Cadastre a chave OPENROUTER_API_KEY no Render.")

# Configura cliente OpenAI para usar OpenRouter
openai.api_key = CHAVE
openai.base_url = "https://openrouter.ai/api/v1"

def responder(mensagem, historico):
    mensagens = [{"role": "system", "content": CONFIG["prompt_sistema"]}]
    for h in historico:
        mensagens.append({"role": "user", "content": h[0]})
        mensagens.append({"role": "assistant", "content": h[1]})
    mensagens.append({"role": "user", "content": mensagem})

    resposta = openai.ChatCompletion.create(
        model=CONFIG["modelo"],
        messages=mensagens,
        max_tokens=CONFIG.get("max_tokens", 800)
    )
    return resposta.choices[0].message["content"]

chat = gr.ChatInterface(
    fn=responder,
    title=str(CONFIG.get("nome", "Assistente IA")),
    description=str(CONFIG.get("descricao", "Chat com IA"))
)

if __name__ == "__main__":
    chat.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000)),
        share=True
    )
