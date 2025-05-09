import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Inicialização do histórico no estado da sessão
if 'historico' not in st.session_state:
    st.session_state.historico = []

st.set_page_config(page_title="Previsor Inteligente", layout="centered")
st.title("Previsor Inteligente de Resultados - Aviator")

st.markdown("**Digite os últimos valores registrados (ex: 2.35):**")
entrada = st.text_input("Novo valor", placeholder="Digite e clique em 'Adicionar'")

# Função para adicionar valor ao histórico
def adicionar_valor():
    try:
        valor = float(entrada)
        if valor > 0:
            st.session_state.historico.append(valor)
            st.success(f"Valor {valor} adicionado com sucesso.")
        else:
            st.warning("Por favor, insira um valor maior que 0.")
    except ValueError:
        st.error("Entrada inválida. Digite um número.")

if st.button("Adicionar"):
    adicionar_valor()

# Exibição do histórico
if st.session_state.historico:
    st.subheader("Histórico de Entradas")
    st.write(st.session_state.historico)

    # Inteligência de análise e previsão
    dados = np.array(st.session_state.historico).reshape(-1, 1)
    X = np.arange(len(dados)).reshape(-1, 1)

    modelo = LinearRegression()
    modelo.fit(X, dados)
    proximo_index = len(dados)
    previsao_media = modelo.predict([[proximo_index]])[0][0]

    # Previsão mínima com base no padrão
    if len(dados) >= 5:
        ultimos = dados[-5:]
        media_recente = np.mean(ultimos)
        previsao_minima = max(min(ultimos)[0] * 0.9, 1.00)
    else:
        previsao_minima = max(dados[-1][0] * 0.85, 1.00)

    st.subheader("Previsão Inteligente")
    st.write(f"**Próximo valor mínimo estimado:** {previsao_minima:.2f}x")
    st.write(f"**Próximo valor médio estimado:** {previsao_media:.2f}x")

    # Alerta inteligente
    if any(v >= 10 for v in st.session_state.historico[-10:]):
        st.warning("Alerta: Alta sequência de valores elevados — possível queda em breve.")
    elif all(v < 2.0 for v in st.session_state.historico[-5:]):
        st.info("Observação: Muitos valores baixos — aumento pode estar próximo.")

else:
    st.info("Nenhum dado inserido ainda.")
