import streamlit as st
import pandas as pd

# Simulação de preços reais
precos_mock = {
    "iPhone 11 64GB": {"mercado_livre": 2350, "olx": 2200, "shopee": 2400},
    "iPhone 12 128GB": {"mercado_livre": 2850, "olx": 2700, "shopee": 2950},
    "iPhone 13 128GB": {"mercado_livre": 3250, "olx": 3100, "shopee": 3350},
    "iPhone 14 128GB": {"mercado_livre": 3750, "olx": 3600, "shopee": 3850},
}

def calcular_media(modelo):
    fontes = precos_mock.get(modelo, {})
    return sum(fontes.values()) / len(fontes) if fontes else 0

def calcular_margem(custo, preco_medio):
    if custo == 0:
        return 0
    return ((preco_medio - custo) / custo) * 100

# Interface
st.title("📱 AppleProTools – MVP de Consulta e Margem")

modelo = st.selectbox("Selecione o modelo do iPhone:", list(precos_mock.keys()))
custo = st.number_input("Informe seu custo total (compra + frete + taxa):", min_value=0.0, format="%.2f")

if modelo:
    st.subheader("📊 Preços de Mercado")
    fontes = precos_mock[modelo]
    df = pd.DataFrame(list(fontes.items()), columns=["Fonte", "Preço (R$)"])
    st.dataframe(df)

    preco_medio = calcular_media(modelo)
    st.markdown(f"**💰 Preço médio de mercado:** R$ {preco_medio:.2f}")

    if custo > 0:
        margem = calcular_margem(custo, preco_medio)
        st.markdown(f"**📈 Margem estimada:** {margem:.2f}%")

    st.info("🔧 Em breve: previsão de desvalorização, sugestão de combos e integração com WhatsApp bot.")
