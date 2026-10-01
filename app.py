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

def responder(mensagem):
    mensagens = [{"role": "system", "content": CONFIG["prompt_sistema"]}]
    mensagens.append({"role": "user", "content": mensagem})

    resposta = openai.ChatCompletion.create(
        model=CONFIG["modelo"],
        messages=mensagens,
        max_tokens=CONFIG.get("max_tokens", 800)
    )
    return resposta.choices[0].message["content"]

# Interface simples com input/output de texto
iface = gr.Interface(
    fn=responder,
    inputs="text",
    outputs="text",
    title="Assistente IA",
    description="Digite sua mensagem e receba uma resposta."
)

if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000)),
        share=True
    )
