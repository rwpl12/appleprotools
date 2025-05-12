import streamlit as st
import pandas as pd
import datetime

# -------------------- Dados Simulados --------------------
usuarios = {"admin": "1234"}
clientes = []
vendas = []

precos_mock = {
    "iPhone 11 64GB": {"mercado_livre": 2350, "olx": 2200, "shopee": 2400},
    "iPhone 12 128GB": {"mercado_livre": 2850, "olx": 2700, "shopee": 2950},
    "iPhone 12 Pro 128GB": {"mercado_livre": 3350, "olx": 3200, "shopee": 3450},
    "iPhone 13 128GB": {"mercado_livre": 3250, "olx": 3100, "shopee": 3350},
    "iPhone 13 Pro Max 256GB": {"mercado_livre": 4450, "olx": 4300, "shopee": 4550},
    "iPhone 14 128GB": {"mercado_livre": 3750, "olx": 3600, "shopee": 3850},
    "iPhone 14 Pro Max 512GB": {"mercado_livre": 6250, "olx": 6100, "shopee": 6350},
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
    {"modelo": "iPhone 13 Pro Max 256GB", "qtd": 1, "data": "2024-11-05", "custo": 4300.0},
]

# -------------------- Funções Auxiliares --------------------
def calcular_media(modelo):
    fontes = precos_mock.get(modelo, {})
    return sum(fontes.values()) / len(fontes) if fontes else 0

def calcular_margem(custo, preco_medio):
    return ((preco_medio - custo) / custo) * 100 if custo > 0 else 0

def previsao_desvalorizacao(modelo):
    base = calcular_media(modelo)
    return {"7 dias": base * 0.98, "30 dias": base * 0.95, "60 dias": base * 0.92}

def gerar_combos(estoque):
    return [{"combo": f"{i['modelo']} + Película + Capa", "preco_sugerido": calcular_media(i['modelo']) + 50} for i in estoque if i['qtd'] >= 2]

def calcular_custo_reparo(avarias):
    return sum([custo_reparo.get(a, 0) for a in avarias])

def gerar_insights(modelo):
    item = next((i for i in estoque_demo if i['modelo'] == modelo), None)
    if item:
        if item['qtd'] > 3: return ["✅ Ofereça brinde"]
        elif item['qtd'] == 1: return ["⚠️ Última unidade"]
        return ["📦 Estoque moderado"]
    return ["🚫 Fora de estoque"]

def registrar_venda(modelo, cliente, vendedor, garantia):
    for item in estoque_demo:
        if item['modelo'] == modelo and item['qtd'] > 0:
            item['qtd'] -= 1
            vendas.append({"modelo": modelo, "cliente": cliente, "vendedor": vendedor, "garantia": garantia, "data": datetime.date.today().isoformat()})
            clientes.append({"nome": cliente, "data": datetime.date.today().isoformat()})
            return True
    return False

def verificar_similares(modelo):
    match = [e['modelo'] for e in estoque_demo if modelo.split()[1] in e['modelo']]
    return f"🔎 Similares no estoque: {match}" if match else "🚫 Nenhum similar. Últimos duraram < 3 dias."

# -------------------- Login --------------------
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if not st.session_state['logado']:
    st.title("🔐 Login de Acesso")
    u, s = st.text_input("Usuário"), st.text_input("Senha", type="password")
    if st.button("Entrar") and usuarios.get(u) == s:
        st.session_state['logado'] = True
    elif u or s:
        st.error("Credenciais inválidas. Use admin / 1234")
    st.stop()

# -------------------- Dashboard --------------------
st.set_page_config(layout="wide")
st.title("🍏 AppleProTools – Plataforma para Lojistas Apple")

aba = st.sidebar.radio("Escolha um módulo:", [
    "Dashboard", "Consulta de Preços", "Calculadora de Margem", "Previsão de Queda",
    "Gestão de Estoque", "Sugestão de Combos", "Simulador de Troca", "Insights para Fechamento",
    "Registro de Venda", "Relatório de Vendas", "Busca por Garantia", "CRM"])

if aba == "Dashboard":
    st.subheader("📊 Visão Geral")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estoque total", sum(i['qtd'] for i in estoque_demo))
    col2.metric("Vendas realizadas", len(vendas))
    col3.metric("Clientes registrados", len(clientes))
    st.markdown("---")
    st.write("🔁 Últimas vendas")
    st.dataframe(pd.DataFrame(vendas[-5:]) if vendas else pd.DataFrame([{"status": "sem dados"}]))

elif aba == "Consulta de Preços":
    m = st.selectbox("Modelo:", list(precos_mock.keys()))
    if st.button("🔍 Pesquisar"):
        df = pd.DataFrame(precos_mock[m].items(), columns=["Fonte", "Preço"])
        st.dataframe(df)
        st.success(f"Preço médio: R$ {calcular_media(m):.2f}")

elif aba == "Calculadora de Margem":
    m = st.selectbox("Modelo:", list(precos_mock.keys()))
    c = st.number_input("Custo total:", min_value=0.0)
    if c:
        media = calcular_media(m)
        st.write(f"📊 Margem: {calcular_margem(c, media):.2f}% (Preço médio: R$ {media:.2f})")

elif aba == "Previsão de Queda":
    m = st.selectbox("Modelo:", list(precos_mock.keys()))
    st.dataframe(pd.DataFrame(previsao_desvalorizacao(m).items(), columns=["Período", "Estimativa R$"]))

elif aba == "Gestão de Estoque":
    df = pd.DataFrame(estoque_demo)
    df['dias_em_estoque'] = df['data'].apply(lambda d: (datetime.datetime.now() - datetime.datetime.strptime(d, "%Y-%m-%d")).days)
    st.dataframe(df)

elif aba == "Sugestão de Combos":
    st.dataframe(pd.DataFrame(gerar_combos(estoque_demo)))

elif aba == "Simulador de Troca":
    d, u = st.selectbox("Desejado:", list(precos_mock)), st.selectbox("Usado:", list(precos_mock))
    a = st.multiselect("Avarias:", list(custo_reparo))
    val_u, val_d = calcular_media(u) - calcular_custo_reparo(a), calcular_media(d)
    st.write(f"Cliente paga: R$ {val_d - val_u:.2f} | Margem estimada: {calcular_margem(val_u, val_d):.2f}%")
    st.caption(verificar_similares(d))

elif aba == "Insights para Fechamento":
    m = st.selectbox("Modelo:", list(precos_mock))
    for i in gerar_insights(m): st.write(f"- {i}")

elif aba == "Registro de Venda":
    m = st.selectbox("Modelo vendido:", list(precos_mock))
    cli = st.text_input("Nome do cliente")
    doc = st.text_input("Documento")
    ven = st.text_input("Vendedor")
    gar = st.date_input("Início da garantia")
    if st.button("Registrar") and cli and ven:
        registrar_venda(m, cli, ven, gar.isoformat())
        st.success("Venda registrada.")

elif aba == "Relatório de Vendas":
    st.dataframe(pd.DataFrame(vendas))

elif aba == "Busca por Garantia":
    nome = st.text_input("Nome do cliente")
    r = [v for v in vendas if v['cliente'] == nome]
    st.dataframe(pd.DataFrame(r)) if r else st.warning("Nada encontrado.")

elif aba == "CRM":
    hoje = datetime.date.today()
    inativos = [v for v in vendas if (hoje - datetime.date.fromisoformat(v['data'])).days > 365]
    st.subheader("📆 Inativos há 12+ meses")
    st.dataframe(pd.DataFrame(inativos) if inativos else pd.DataFrame([{"status": "Nenhum encontrado"}]))
