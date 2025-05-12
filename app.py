import streamlit as st
import pandas as pd
import datetime

# Simulação de dados de preço por modelo
precos_mock = {
    "iPhone 11 64GB": {"mercado_livre": 2350, "olx": 2200, "shopee": 2400},
    "iPhone 12 128GB": {"mercado_livre": 2850, "olx": 2700, "shopee": 2950},
    "iPhone 13 128GB": {"mercado_livre": 3250, "olx": 3100, "shopee": 3350},
    "iPhone 14 128GB": {"mercado_livre": 3750, "olx": 3600, "shopee": 3850},
}

custo_reparo = {
    "tela trincada": 650,
    "sem carregador": 50,
    "com riscos": 200,
    "bateria ruim": 350,
    "carcaça amassada": 400
}

estoque_demo = [
    {"modelo": "iPhone 12 128GB", "qtd": 3, "data": "2024-11-10", "custo": 2700.0},
    {"modelo": "iPhone 11 64GB", "qtd": 5, "data": "2024-11-01", "custo": 2200.0},
    {"modelo": "iPhone 13 128GB", "qtd": 2, "data": "2024-11-05", "custo": 3100.0},
]

# Funções auxiliares
def calcular_media(modelo):
    fontes = precos_mock.get(modelo, {})
    return sum(fontes.values()) / len(fontes) if fontes else 0

def calcular_margem(custo, preco_medio):
    if custo == 0:
        return 0
    return ((preco_medio - custo) / custo) * 100

def previsao_desvalorizacao(modelo):
    base = calcular_media(modelo)
    return {
        "7 dias": base * 0.98,
        "30 dias": base * 0.95,
        "60 dias": base * 0.92
    }

def gerar_combos(estoque):
    combos = []
    for item in estoque:
        if item["qtd"] >= 2:
            combos.append({
                "combo": f"{item['modelo']} + Película + Capa",
                "preco_sugerido": calcular_media(item['modelo']) + 50
            })
    return combos

def calcular_custo_reparo(avarias):
    return sum([custo_reparo[a] for a in avarias if a in custo_reparo])

def gerar_insights(modelo, estoque):
    estoque_item = next((item for item in estoque if item['modelo'] == modelo), None)
    insights = []
    if estoque_item:
        if estoque_item['qtd'] > 3:
            insights.append("✅ Ofereça brinde: estoque alto do modelo")
        elif estoque_item['qtd'] == 1:
            insights.append("⚠️ Última unidade! Use escassez para fechar a venda")
        else:
            insights.append("📦 Estoque moderado. Priorize giro.")
    else:
        insights.append("🔍 Modelo não está no estoque atual.")
    return insights

# Interface Streamlit
st.set_page_config(layout="wide")
st.title("🍏 AppleProTools – Plataforma para Lojistas Apple")

aba = st.sidebar.radio("Escolha um módulo:", [
    "Consulta de Preços", "Calculadora de Margem", "Previsão de Queda", "Gestão de Estoque",
    "Sugestão de Combos", "Simulador de Troca", "Insights para Fechamento"
])

if aba == "Consulta de Preços":
    modelo = st.selectbox("Selecione o modelo:", list(precos_mock.keys()))
    if st.button("🔍 Pesquisar preços atualizados"):
        st.success("Dados atualizados com base simulada.")
    if modelo:
        fontes = precos_mock[modelo]
        df = pd.DataFrame(list(fontes.items()), columns=["Fonte", "Preço (R$)"])
        st.dataframe(df)
        media = calcular_media(modelo)
        st.success(f"Preço médio de mercado: R$ {media:.2f}")

elif aba == "Calculadora de Margem":
    modelo = st.selectbox("Modelo para cálculo:", list(precos_mock.keys()))
    custo = st.number_input("Informe seu custo total (R$):", min_value=0.0, format="%.2f")
    if modelo and custo:
        preco_medio = calcular_media(modelo)
        margem = calcular_margem(custo, preco_medio)
        st.info(f"Preço médio atual: R$ {preco_medio:.2f}")
        st.success(f"Margem estimada: {margem:.2f}%")

elif aba == "Previsão de Queda":
    modelo = st.selectbox("Modelo para previsão:", list(precos_mock.keys()))
    if modelo:
        st.subheader("📉 Previsão de desvalorização")
        previsoes = previsao_desvalorizacao(modelo)
        df = pd.DataFrame(previsoes.items(), columns=["Período", "Preço Estimado"])
        st.dataframe(df)

elif aba == "Gestão de Estoque":
    st.subheader("📦 Estoque Atual")
    df = pd.DataFrame(estoque_demo)
    df['dias_em_estoque'] = df['data'].apply(lambda d: (datetime.datetime.now() - datetime.datetime.strptime(d, "%Y-%m-%d")).days)
    st.dataframe(df)

elif aba == "Sugestão de Combos":
    st.subheader("🧠 Combos Inteligentes Sugeridos")
    combos = gerar_combos(estoque_demo)
    df = pd.DataFrame(combos)
    st.dataframe(df)
    st.caption("Combos criados com base no estoque parado e maior margem de revenda.")

elif aba == "Simulador de Troca":
    st.subheader("💱 Simulação de troca com aparelho usado")
    modelo_desejado = st.selectbox("Modelo que o cliente deseja:", list(precos_mock.keys()))
    modelo_usado = st.selectbox("Modelo do aparelho do cliente:", list(precos_mock.keys()))
    avarias = st.multiselect("Selecione as avarias detectadas:", list(custo_reparo.keys()))
    preco_medio_desejado = calcular_media(modelo_desejado)
    preco_medio_usado = calcular_media(modelo_usado)
    desconto_reparo = calcular_custo_reparo(avarias)
    valor_oferecido = preco_medio_usado - desconto_reparo
    valor_a_pagar = preco_medio_desejado - valor_oferecido
    margem = calcular_margem(valor_oferecido + desconto_reparo, preco_medio_desejado)
    st.markdown(f"📱 Valor médio do aparelho desejado: R$ {preco_medio_desejado:.2f}")
    st.markdown(f"♻️ Valor estimado do usado com avarias: R$ {valor_oferecido:.2f}")
    st.markdown(f"💸 Diferença a ser paga pelo cliente: R$ {valor_a_pagar:.2f}")
    st.success(f"📊 Margem estimada da negociação: {margem:.2f}%")

elif aba == "Insights para Fechamento":
    modelo_desejado = st.selectbox("Modelo que o cliente quer comprar:", list(precos_mock.keys()))
    if modelo_desejado:
        st.subheader("💡 Insights para o vendedor:")
        for insight in gerar_insights(modelo_desejado, estoque_demo):
            st.write("- ", insight)
        st.caption("Use essas estratégias para convencer o cliente e fechar mais vendas.")
