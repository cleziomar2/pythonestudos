import streamlit as st
import requests

# URL base do Elasticsearch
BASE_URL = "http://200.9.155.126:9200/pessoas_v4/_search?q="

# Função para formatar dados
def formatar_dados(dados, index=1):
    def get(valor):
        return valor if valor else "(não informado)"
    
    cpf = dados.get("CPF", "")
    cpf_formatado = (
        f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if cpf and len(cpf) == 11 else "(não informado)"
    )

    try:
        renda = float(dados.get("RENDA", 0))
        renda_str = f"R$ {renda:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        renda_str = "(não informado)"

    return f"""
### Resultado {index}
**Nome:** {get(dados.get("NOME"))}  
**CPF:** {cpf_formatado}  
**Nascimento:** {get(dados.get("NASC"))}  
**Sexo:** {get(dados.get("SEXO"))}  
**Renda:** {renda_str}  
**Situação Cadastro:** {get(dados.get("CD_SIT_CAD"))}  
**Data Situação:** {get(dados.get("DT_SIT_CAD"))}  

**Nome da Mãe:** {get(dados.get("NOME_MAE"))}  
**Nome do Pai:** {get(dados.get("NOME_PAI"))}  
**Contato ID:** {get(dados.get("CONTATOS_ID"))}  
**Título Eleitor:** {get(dados.get("TITULO_ELEITOR"))}  
**RG:** {get(dados.get("RG"))}  
**UF Emissão:** {get(dados.get("UF_EMISSAO"))}  
---
"""

# Interface do app
st.title("🔍 Consulta  (pessoas_v4)")
termo = st.text_input("Digite o termo de busca (ex: cpf:, nome:JOAO, email:gmail.com)")

if st.button("Buscar") and termo:
    url = BASE_URL + termo
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            hits = dados.get("hits", {}).get("hits", [])
            if not hits:
                st.warning("Nenhum resultado encontrado.")
            else:
                for i, item in enumerate(hits, start=1):
                    st.markdown(formatar_dados(item.get("_source", {}), i))
        else:
            st.error(f"Erro na consulta: HTTP {response.status_code}")
    except Exception as e:
        st.error(f"Erro: {str(e)}")
