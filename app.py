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

# Histórico global
historico = []

def responder(mensagem):
    global historico
    mensagens = [{"role": "system", "content": CONFIG["prompt_sistema"]}]
    # adiciona histórico anterior
    for h in historico:
        mensagens.append({"role": "user", "content": h[0]})
        mensagens.append({"role": "assistant", "content": h[1]})
    # adiciona nova mensagem
    mensagens.append({"role": "user", "content": mensagem})

    resposta = openai.ChatCompletion.create(
        model=CONFIG["modelo"],
        messages=mensagens,
        max_tokens=CONFIG.get("max_tokens", 800)
    )
    conteudo = resposta.choices[0].message["content"]

    # salva no histórico
    historico.append((mensagem, conteudo))
    return conteudo

# Interface simples com input/output de texto
iface = gr.Interface(
    fn=responder,
    inputs="text",
    outputs="text",
    title="Assistente IA",
    description="Digite sua mensagem e receba uma resposta com histórico."
)

if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000)),
        share=True
    )
