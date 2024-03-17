import streamlit as st # streamlit utilizado para criar a interface gráfica do programa
from streamlit_echarts import st_echarts 
import pandas as pd
import numpy as np
import os
from configuracoes.configs_graficos import configs_lucro, configs_massas
from utils.utils import valores_ate_negativo, achar_coefs

def main(dados: pd.DataFrame):
    """
    #####
    """

    # Título
    st.title("Sistema de recomendação para data de abate de lote de animais")

    # Componente visual para inserir o preço do arroba
    preco_carne = st.slider(label = "Preço do arroba", min_value = 3.0, max_value = 8.0, value = 7.0, step = 0.1)

    # Componente visual para inserir o preço da racão
    preco_racao = st.slider(label = "Custo de Produção", min_value = 0.50, max_value = 1.50, value = 0.80, step = 0.1)

    
    # Inserindo a coluna de lucro
    dados["L"] = dados["M"] * preco_carne - dados["R"] * preco_racao

    # Achar os coeficientes de ajuste par os dados L(t)
    resp = achar_coefs(dados=dados, grau_maximo=10)
    if resp is None:
        st.warning(label="São necessários mais dados para fazer a previsão do abate.", icon="⚠")
        st.stop()

    else:
        coefs_massa, coefs_racao, coefs_lucro = resp
    
    # Obter os dados de lucro, custo e receita até a data de lucro negativo.
    # (apenas para visualização)
    
    tupla_resultante = valores_ate_negativo(coefs_lucro=coefs_lucro, 
                                            coefs_racao=coefs_racao, 
                                            coefs_massa=coefs_massa,
                                            preco_racao=preco_racao,
                                            preco_carne=preco_carne)
    
    # Desempacotar a tupla
    ts_ate_negativo = tupla_resultante[0]
    lucros: np.ndarray = tupla_resultante[1]
    custos: list = tupla_resultante[2]
    receitas: list = tupla_resultante[3]

    # t_ideal é um índice que indica o momento ideal para o abate
    t_ideal: int = lucros.argmax() + 1
    lucro_maximo: float = lucros[t_ideal]
    custo_total: float = custos[t_ideal]
    receita_total: float = receitas[t_ideal]

    # Visualizar gráfico de lucro
    st.title("Gráfico de lucro")
    configs_lucro["xAxis"]["data"] = ts_ate_negativo
    configs_lucro["series"][0]["data"] = list(lucros)
    st_echarts(options=configs_lucro)

    # Exibindo métricas
    col1, col2 = st.columns(2)
    col1.metric(label="Data ideal para abate: ", value=t_ideal)

    col2.metric(label=f"Lucro máximo: ", 
                value=f"R$ {lucro_maximo:.2f}", 
                delta=f"{receita_total / custo_total - 1:.2%}")
    
    # Visualizar gráfico de massas e rações
    st.title("Custos vs Massa do Lote")
    configs_massas["xAxis"]["data"] = dados["t"].to_list()
    configs_massas["series"][0]["data"] = dados["M"].to_list()
    configs_massas["series"][1]["data"] = dados["R"].to_list()
    st_echarts(options=configs_massas)












if __name__ == "__main__":
    nome_arquivo = os.path.join("base_dados", "BaseDados.xlsx")
    df = pd.read_excel(nome_arquivo, sheet_name=0, engine="openpyxl")
    main(dados = df)