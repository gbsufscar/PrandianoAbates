import pandas as pd
import numpy as np

def r_2(valores_exp: pd.Series, valores_teo: np.ndarray) -> float:

    """
    Função que calcula o coeficiente de determinação (R²) para um modelo de regressão linear.

    Args:
        valores_exp: valores experimentais.
        valores_teo: valores teóricos.

    Returns:
        float: coeficiente de determinação (R²).
    """

    # sse = somatório dos quadrados dos erros
    sse: np.ndarray = (valores_teo - valores_exp.mean()) ** 2

    # sst = somatório dos quadrados totais
    sst: np.ndarray = (valores_exp - valores_exp.mean()) ** 2

    return sse.sum() / sst.sum()
