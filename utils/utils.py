import numpy as np
from funcoes.metodo_minimos_quadrados import mmq
from utils.r_quadrado import r_2
import pandas as pd

def valores_ate_negativo(coefs_lucro: np.ndarray, coefs_racao: np.ndarray, coefs_massa: np.ndarray, 
                         preco_racao: float, preco_carne: float) -> tuple:
    
    """
    Função para calcular os valores de lucro, custo e receita até o lucro ser negativo.
    Parâmetros:
        coefs_lucro: coeficientes do polinômio que representa o lucro
        coefs_racao: coeficientes do polinômio que representa o custo com ração
        coefs_massa: coeficientes do polinômio que representa a massa do animal
        preco_racao: preço da ração
        preco_carne: preço da carne
    """

    t = 1
    lucros_ate_negativo: list = []
    custos_ate_negativo: list = []
    receitas_ate_negativo: list = []
    ts_ate_negativo: list = []
    while True:

        lucro: float = polinomio(coefs=coefs_lucro, entrada=int(t))
        custo: float = preco_racao * polinomio(coefs=coefs_racao, entrada=t)
        receita: float = preco_carne * polinomio(coefs=coefs_massa, entrada=t)
        
        lucros_ate_negativo.append(lucro)
        custos_ate_negativo.append(custo)
        receitas_ate_negativo.append(receita)

        ts_ate_negativo.append(t)
        t += 1

        if lucros_ate_negativo[-1] < 0:
            break

    lucros_ate_negativo: np.ndarray = np.array(lucros_ate_negativo).round(2)

    # o python retornará uma tupla com os valores abaixo (pois não foi especificado o tipo do objeto coleção abaixo)
    return ts_ate_negativo, lucros_ate_negativo, custos_ate_negativo, receitas_ate_negativo

def coefs2str(coefs: np.ndarray) -> str:
    """
    Função para transformar os coeficientes de uma equação em uma string.
    Parâmetros:
        coefs: coeficientes da equação
        Retorno:
        String representando a equação
    Retorno:
        String representando a equação
    """

    g: int = len(coefs) - 1

    str_final: str = ""
    for i, coef in enumerate(coefs):
        str_final += f"{coef:.2f} * x ** {g - i} + "
    
    return str_final[:-3]

from utils.utils import coefs2str

def polinomio(coefs: np.ndarray, entrada: int) -> float:

    """
    Função para calcular o valor de um polinômio em um ponto.
    Parâmetros:
        coefs: coeficientes do polinômio
        entrada: ponto onde o polinômio será avaliado
    Retorno:
        Valor do polinômio no ponto
    """

    funcao = eval(f"lambda x: {coefs2str(coefs)}")
    return funcao(entrada)


def achar_coefs(dados: pd.DataFrame, grau_maximo: int = 10) -> tuple:

    """
    Função para ajustar polinômios de graus diferentes aos dados.
    Parâmetros:
        dados: DataFrame contendo os dados de massa, ração e lucro
        grau_maximo: grau máximo do polinômio que será ajustado
    Retorno:
        Coeficientes dos polinômios que melhor se ajustam aos dados
    """

    # somente para g's pares, pois a curva de lucro deve ter concavidade
    for g in range(2, grau_maximo, 2): # Grau da função ajustada é par (concavidade para baixo)

        coefs_massa: np.ndarray = mmq(entradas=dados["t"], saidas=dados["M"], g=g)
        coefs_racao: np.ndarray = mmq(entradas=dados["t"], saidas=dados["R"], g=g)
        coefs_lucro: np.ndarray = mmq(entradas=dados["t"], saidas=dados["L"], g=g)

        # tentando ajustar polinômios de graus diferentes [2, 10[
        # apenas se o primeiro coeficiente for negativo (concavidade para baixo)
        if (coef_a:=coefs_lucro[0]) < 0:
            ts = np.zeros(shape=(len(dados),), dtype=int)
            massas_teoricas = np.zeros(shape=(len(dados),), dtype=float)
            racoes_teoricas = np.zeros(shape=(len(dados),), dtype=float)
            for t in range(len(dados)):
                massas_teoricas[t] = polinomio(coefs=coefs_massa, entrada=t + 1)
                racoes_teoricas[t] = polinomio(coefs=coefs_racao, entrada=t + 1)
                ts[t] = t + 1

            acerto_massas = r_2(valores_exp=dados["M"], valores_teo=massas_teoricas)
            acerto_racoes = r_2(valores_exp=dados["R"], valores_teo=racoes_teoricas)

            # se o ajuste for bom, para de tentar ajustar polinômios
            if acerto_massas >= 0.99 and acerto_racoes >= 0.99:
                return coefs_massa, coefs_racao, coefs_lucro