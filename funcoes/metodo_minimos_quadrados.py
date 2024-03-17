import numpy as np
import pandas as pd

def mmq(entradas: np.ndarray | pd.Series, saidas: np.ndarray | pd.Series, g: int) -> np.ndarray:

    # s_x = [somatorio de x^(2g), somatorio de x^(2g-1), ..., somatorio de x², somatorio de x¹, somatorio de x⁰]
    s_x: np.ndarray = np.zeros(shape=(1, 2 * g + 1))
    for i in range(2 * g, -1, -1):
        s_x[0, i] = sum(entradas ** (2 * g - i))
    
    # m = matriz contento os somatórios de x^(2g), x^(2g-1), ..., x², x¹, x⁰ no formato:
    # para g = 2: 
        # [[soma_x⁴, soma_x³, soma_x²], 
        # [ soma_x³, soma_x², soma_x¹], 
        # [ soma_x², soma_x¹, soma_x⁰]]
    
    # para g = 3:
        # [[soma_x⁶, soma_x⁵, soma_x⁴, soma_x³], 
        # [ soma_x⁵, soma_x⁴, soma_x³, soma_x²], 
        # [ soma_x⁴, soma_x³, soma_x², soma_x¹], 
        # [ soma_x³, soma_x², soma_x¹, soma_x⁰]]

    # para g = 4:
        # [[soma_x⁸, soma_x⁷, soma_x⁶, soma_x⁵, soma_x⁴], 
        # [ soma_x⁷, soma_x⁶, soma_x⁵, soma_x⁴, soma_x³], 
        # [ soma_x⁶, soma_x⁵, soma_x⁴, soma_x³, soma_x²], 
        # [ soma_x⁵, soma_x⁴, soma_x³, soma_x², soma_x¹], 
        # [ soma_x⁴, soma_x³, soma_x², soma_x¹, soma_x⁰]]

    m = np.zeros(shape=(g + 1, g + 1))
    for j in range(g + 1):
        m[j, :] = s_x[0, j:j + g + 1]
    m_inv = np.linalg.inv(m)

    # s_xy = [somatorio de x^g * y, somatorio de x^(g-1) * y, ..., somatorio de x² * y, somatorio de x¹ * y, somatorio de x⁰ * y]
    s_xy = np.zeros(shape=(g + 1, 1))
    for k in range(g, -1, -1):
        s_xy[g - k, 0] = sum((entradas ** k) * saidas)

    # o sistema de equações a ser resolvido é a vetor resultante do produto das matrizes m_inv e s_xy
    # coeficientes = m_inv @ s_xy # mesmo que np.dot(m_inv, s_xy) ou m_inv.dot(s_xy) ou np.matmul(m_inv, s_xy) ou np.linalg.solve(m, s_xy)
    coeficientes = m_inv @ s_xy

    # o produto acuma retorna um array de arrays (n+1 * 1), então é necessário transformar em um array (n + 1) de floats
    return coeficientes.ravel()


if __name__ == "__main__":
    # x = np.array([0, 1, 2, 3, 4, 5])
    # f = np.array([11, -2, 7, 20, 19, -14])    # f(x) = -3x³ + 20x² - 30x¹ + 11x⁰
    # g = 3

    x = np.array([-1, 0, 1, 2])
    f = np.array([2, 3, 6, 11])             # f(x) = 1x² + 2x¹ + 3x⁰
    g = 2

    coef = mmq(entradas=x, saidas=f, g=g)
    print(coef)
    print(f"Coeficientes (equação de {g}⁰):")
    print(dict(zip([chr(c) for c in range(97, 97 + g + 1, 1)], coef.T)))