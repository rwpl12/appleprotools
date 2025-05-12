import streamlit as st
import pandas as pd
import datetime

# --- Dados simulados ---
usuarios = {"admin": "1234"}
clientes = []
vendas = []

# Simulação de dados de preço por modelo
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

def registrar_venda(modelo, cliente, vendedor, garantia):
    for item in estoque_demo:
        if item['modelo'] == modelo and item['qtd'] > 0:
            item['qtd'] -= 1
            vendas.append({
                "modelo": modelo,
                "cliente": cliente,
                "vendedor": vendedor,
                "garantia": garantia,
                "data": datetime.date.today().isoformat()
            })
            clientes.append(cliente)
            return True
    return False

def verificar_similares(modelo):
    similares = [item for item in estoque_demo if modelo.split()[1] in item['modelo']]
    if similares:
        return f"🔎 Existem modelos similares em estoque: {[s['modelo'] for s in similares]}"
    else:
        return "🚫 Nenhum modelo similar no estoque. Os últimos saíram em menos de 3 dias. Considere melhorar a oferta."

# Autenticação
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if not st.session_state['logado']:
    st.title("🔐 Login de Acesso")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state['logado'] = True
        else:
            st.error("Usuário ou senha inválidos. Use admin / 1234")
    st.stop()

# App Principal
st.title("🍏 AppleProTools – Plataforma para Lojistas Apple")

aba = st.sidebar.radio("Escolha um módulo:", [
    "Consulta de Preços", "Calculadora de Margem", "Previsão de Queda", "Gestão de Estoque",
    "Sugestão de Combos", "Simulador de Troca", "Insights para Fechamento",
    "Registro de Venda", "Relatório de Vendas", "Busca por Garantia", "CRM"
])

if aba == "Registro de Venda":
    st.subheader("📝 Registrar nova venda")
    modelo_vendido = st.selectbox("Modelo vendido:", list(precos_mock.keys()))
    nome_cliente = st.text_input("Nome do cliente")
    documento = st.text_input("CPF ou documento")
    aniversario = st.date_input("Data de nascimento")
    vendedor = st.text_input("Nome do vendedor")
    garantia = st.date_input("Início da garantia")
    if st.button("Registrar venda"):
        sucesso = registrar_venda(modelo_vendido, nome_cliente, vendedor, garantia.isoformat())
        if sucesso:
            st.success("✅ Venda registrada e estoque atualizado.")
        else:
            st.error("❌ Modelo sem estoque disponível. Verifique novamente.")

elif aba == "Relatório de Vendas":
    st.subheader("📊 Relatório de Vendas")
    df = pd.DataFrame(vendas)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Nenhuma venda registrada ainda.")

elif aba == "Busca por Garantia":
    st.subheader("🔎 Buscar garantia por nome")
    nome = st.text_input("Nome do cliente para consulta")
    resultado = [v for v in vendas if v['cliente'] == nome]
    if resultado:
        df = pd.DataFrame(resultado)
        st.dataframe(df)
    elif nome:
        st.warning("Nenhuma venda encontrada para este nome.")

elif aba == "CRM":
    st.subheader("📞 CRM – Retenção e Relacionamento")
    hoje = datetime.date.today()
    clientes_12m = [v for v in vendas if (hoje - datetime.date.fromisoformat(v['data'])).days > 365]
    aniversariantes = [c for c in clientes if isinstance(c, str)]
    if clientes_12m:
        st.markdown("### 📆 Clientes com última compra há mais de 12 meses")
        st.dataframe(pd.DataFrame(clientes_12m))
    else:
        st.info("Nenhum cliente com mais de 12 meses ainda.")
