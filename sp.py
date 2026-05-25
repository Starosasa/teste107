import streamlit as st
from datetime import datetime

st.set_page_config(page_title='POSITIVO Service', layout='wide')

if "equipamentos" not in st.session_state:
    st.session_state.equipamentos = []
if "pagina" not in st.session_state:
    st.session_state.pagina = "cadastro"

def cabecalho():
    st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a, #1e40af); padding: 1rem; border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h1 style="margin: 0;">POSITIVO</h1>
            <p style="margin: 0;">Service · New Energy</p>
        </div>
    """, unsafe_allow_html=True)

def salvar_equipamento(oss, modelo, cliente, status, nome, descricao):
    if not oss or not nome:
        st.error("OSS e Nome do equipamento são obrigatórios!")
        return False
    novo = {
        "oss": oss,
        "modelo": modelo,
        "cliente": cliente,
        "status": status,
        "nome": nome,
        "descricao": descricao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.session_state.equipamentos.append(novo)
    return True

def pagina_cadastro():
    st.markdown("## Cadastro de Equipamento")
    with st.form(key="form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            oss = st.text_input("OSS")
            modelo = st.text_input("Modelo do equipamento")
            cliente = st.text_input("Cliente")
            status = st.radio("Status", ["aprovado", "reprovado", "aguardando"])
        with col2:
            nome = st.text_input("Nome do equipamento")
            descricao = st.text_area("Descrição / causa", height=100)
        enviar = st.form_submit_button("Enviar", use_container_width=True, type="primary")
        if enviar:
            if salvar_equipamento(oss, modelo, cliente, status, nome, descricao):
                st.success("Equipamento cadastrado com sucesso!")
                st.session_state.pagina = "galeria"
                st.rerun()

def pagina_galeria():
    st.markdown("## Galeria de Equipamentos")
    busca = st.text_input("Buscar", placeholder="Digite OSS, modelo, cliente, nome...")
    dados = st.session_state.equipamentos
    if busca:
        termo = busca.lower()
        dados = [e for e in dados if termo in f"{e['oss']} {e['modelo']} {e['cliente']} {e['nome']} {e['descricao']}".lower()]
    
    st.caption(f"{len(dados)} registro(s)")
    if not dados:
        st.info("Nenhum equipamento encontrado.")
        return
    
    cols = st.columns(3)
    for idx, eq in enumerate(dados):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"**OSS:** {eq['oss']}")
                st.markdown(f"**Nome:** {eq['nome']}")
                st.markdown(f"**Modelo:** {eq['modelo']}")
                st.markdown(f"**Cliente:** {eq['cliente']}")
                st.markdown(f"**Status:** {eq['status']}")
                st.caption(f"Cadastro: {eq['data']}")
                if st.button("Excluir", key=f"del_{idx}_{eq['oss']}_{eq['data']}"):
                    for i, item in enumerate(st.session_state.equipamentos):
                        if item['oss'] == eq['oss'] and item['data'] == eq['data']:
                            st.session_state.equipamentos.pop(i)
                            break
                    st.rerun()

def main():
    cabecalho()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cadastro", use_container_width=True):
            st.session_state.pagina = "cadastro"
            st.rerun()
    with col2:
        if st.button("Galeria", use_container_width=True):
            st.session_state.pagina = "galeria"
            st.rerun()
    
    if st.session_state.pagina == "cadastro":
        pagina_cadastro()
    else:
        pagina_galeria()

if __name__ == "__main__":
    main()