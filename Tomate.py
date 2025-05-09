import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import time
from data_storage import load_data, save_data, clear_data

st.set_page_config(page_title="Previsão Aviator1", layout="wide")
st.title("Inteligência de Prognóstico - Aviator1")

# Dados
data = load_data()

# Interface para inserir novos valores
st.subheader("Adicionar novo valor")
new_value = st.number_input("Digite o valor (ex: 2.62)", min_value=0.01, step=0.01, format="%.2f")
if st.button("Adicionar"):
    tempo_digitacao = 3
    timestamp = time.time() - tempo_digitacao
    data.append({"timestamp": timestamp, "valor": new_value})
    save_data(data)
    st.success("Valor adicionado com sucesso!")

if st.button("Limpar histórico"):
    clear_data()
    data = []
    st.warning("Histórico apagado.")

# Mostrar histórico
st.subheader("Histórico de valores")
df = pd.DataFrame(data)
if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)
    st.dataframe(df[["timestamp", "valor"]], height=250)

    # Gráfico
    st.subheader("Gráfico dos últimos valores")
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df['valor'], marker='o', linestyle='-')
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Valor")
    ax.set_title("Histórico de Rodadas")
    st.pyplot(fig)

    # Previsão Inteligente
    st.subheader("Previsão Inteligente (mínimo e média estimada)")
    df_recent = df.sort_values("timestamp").tail(20)
    X = np.arange(len(df_recent)).reshape(-1, 1)
    y = df_recent['valor'].values

    if len(X) >= 2:
        model = LinearRegression()
        model.fit(X, y)
        next_index = np.array([[len(X)]])
        predicted_mean = model.predict(next_index)[0]
        predicted_min = max(min(y[-5:]) - 0.1, 1.00)  # mínimo baseado nos últimos 5

        st.markdown(f"**Valor mínimo estimado da próxima rodada:** `{predicted_min:.2f}x`")
        st.markdown(f"**Valor médio previsto:** `{predicted_mean:.2f}x`")

        if any(v >= 10 for v in y[-10:]) or y[-1] >= 10:
            st.warning("ATENÇÃO: Grandes valores recentes podem indicar forte queda nas próximas rodadas.")

else:
    st.info("Insira valores para começar a análise.")
