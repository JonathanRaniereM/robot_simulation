import numpy as np
import matplotlib.pyplot as plt

def relaxacao_laplace(N, Nint, tol=0.01):
    """
    Campo de temperatura de uma chapa bidimensional
    usando o método de relaxação.
    
    Parâmetros:
        N (int): Número de pontos em cada dimensão da grade (N x N).
        Nint (int): Número de iterações do método de relaxação.
    
    Retorna:
        V (ndarray): Matriz de temperaturas após Nint iterações.
    """


    # Inicialização da matriz de temperaturas
    V = np.zeros((N, N))
    V_new = np.zeros_like(V)

    # Condições de contorno
    V[0, :] = 100    # Topo da chapa em 100°C
    V[-1, :] = 0  # Base da chapa em 0°C
    V[:, 0] = 0    # Lado esquerdo da chapa em 0°C
    V[:, -1] = 0   # Lado direito da chapa em 0°C

    # Método de relaxação para resolver a equação de Laplace
    for iteration in range(Nint):
        V_new[1:-1, 1:-1] = 0.25 * (V[2:, 1:-1] + V[:-2, 1:-1] + V[1:-1, 2:] + V[1:-1, :-2])

        # Aplica as condições de contorno em cada iteração
        V_new[0, :] = 100
        V_new[-1, :] = 0
        V_new[:, 0] = 0
        V_new[:, -1] = 0

        # Verifica a convergência
        if np.max(np.abs(V_new - V)) < tol:
            print(f"Convergência alcançada após {iteration} iterações.")
            break

        V = np.copy(V_new)

    return V_new

# Parâmetros
N = 50  # Dimensão da grade
Nint = 1000  # Número máximo de iterações

# Aplicando o método de relaxação
campo_temperatura = relaxacao_laplace(N, Nint)

# Plotando o resultado
plt.figure(figsize=(8, 6))
plt.imshow(campo_temperatura, cmap='hot', origin='lower')
plt.colorbar(label='Temperatura (°C)')
plt.title('Distribuição de Temperatura na Chapa')
plt.xlabel('x')
plt.ylabel('y')
plt.show()