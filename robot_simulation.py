import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros
size = 100
goal = np.array([90, 80])
start = np.array([10, 10])
# Mudança na posição dos obstáculos para testar diferentes cenários
obstacles =  [np.array([30, 40]), np.array([55, 40]), np.array([75, 70])]
tolerance = 1e-3
max_iterations = 10000
force_scale = 0.5
safe_distance = 0  # Distância segura para desvio de obstáculos


# Inicialização do grid
phi = np.zeros((size, size))
phi[int(goal[0]), int(goal[1])] =  100
for obs in obstacles:
    phi[int(obs[0]), int(obs[1])] = -100

# Método de Relaxação para resolver a equação de Laplace
for iteration in range(max_iterations):
    phi_old = phi.copy()
    
    # Atualização do potencial interno do grid baseado nos valores dos vizinhos
    phi[1:-1, 1:-1] = 0.25 * (phi_old[2:, 1:-1] + phi_old[:-2, 1:-1] + phi_old[1:-1, 2:] + phi_old[1:-1, :-2])
    # Esta linha aplica a média dos quatro vizinhos (acima, abaixo, esquerda, direita) a cada ponto do grid, exceto nas bordas
    
    # Aplicando condições de contorno fixas a cada iteração
    phi[int(goal[0]), int(goal[1])] = 100
    for obs in obstacles:
        phi[int(obs[0]), int(obs[1])] = -100
        # Garantindo que áreas próximas aos obstáculos também tenham potencial baixo
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= obs[0] + dx < size and 0 <= obs[1] + dy < size:
                    phi[int(obs[0] + dx), int(obs[1] + dy)] = -80  # Ajustar para um valor suficientemente baixo

    # Checando a convergência
    if np.max(np.abs(phi - phi_old)) < tolerance:
        
        print(f"Convergência Atingida. Maior mudança no campo: {np.max(np.abs(phi - phi_old))}. Em: {iteration}")
        break

# Gradiente do potencial
phi_x, phi_y = np.gradient(phi)

# Posição inicial do robô
current_pos = start.astype(float).copy()
trajectory = [current_pos.copy()]
moving_to_goal = True

# Configuração do gráfico
fig, ax = plt.subplots()
ax.set_xlim(0, size)
ax.set_ylim(0, size)

# Desenhar os contornos do campo de potencial
potential_contour = ax.contourf(phi.T, levels=50, cmap='viridis', antialiased=False, zorder=1)

goal_circle = plt.Circle(goal.T, 2, color='red')
ax.add_patch(goal_circle)
robot_circle = plt.Circle(current_pos, 2, color='blue')
ax.add_patch(robot_circle)






# Adicionando obstáculos com intensidade visual baseada no potencial
for obs in obstacles:
    obstacle_circle = plt.Circle(obs, 2, color='black', fill=True, zorder=2)  # Mais vermelho indica maior repulsão
    ax.add_patch(obstacle_circle)

trajectory_line, = ax.plot([], [], 'b-', lw=2)  # Linha para a trajetória

# Função de atualização da animação
def update(frame):
    global current_pos, moving_to_goal
    
    idx = int(current_pos[0])
    idy = int(current_pos[1])
    
    f_x = phi_x[idy, idx]
    f_y = phi_y[idy, idx]
    
    direction = np.array([f_x, f_y]) # Cria um array numpy com os componentes x e y do gradiente do campo de potencial
    
    if np.linalg.norm(direction) > 0:  # Normaliza o vetor de direções
        direction /= np.linalg.norm(direction)
        
    target = goal 
    
    to_target = target - current_pos # Calcula o vetor direcional do robô ao alvo
    
    if np.linalg.norm(to_target) > 0:
        to_target = to_target / np.linalg.norm(to_target)   # Normaliza o vetor direcional  ao alvo para garantir que ele tenha magnitude 1
        
    combined_direction = 0.2 * direction + 0.4 * to_target # Combina o vetor gradiente (campo potencial)  e o vetor ao alvo com pesos, dando mais importância ao alvo
    
    if np.linalg.norm(combined_direction) > 0:
        combined_direction /= np.linalg.norm(combined_direction)
        
    new_pos = current_pos + force_scale * combined_direction
    
    # Ajustar a direção baseada na proximidade e no gradiente do potencial
    for obs in obstacles:
        distance = np.linalg.norm(new_pos - obs)
        
        phi_val = phi[int(obs[0]), int(obs[1])]
        
        if distance < safe_distance:
            if np.linalg.norm(new_pos - current_pos) < 1: # Verifica se o robô quase não se moveu entre as atualizações de posição. (Ou seja, está travado)
                avoidance_direction = new_pos - obs + np.random.randn(2) # Vetor apontando para longe do obstáculo + componente aléatorio
                print(f"Metod Random {obs}, phi_value: {phi_val}, distance: {distance}")

            if np.linalg.norm(avoidance_direction) > 0:
                avoidance_direction /= np.linalg.norm(avoidance_direction) 
            new_pos = current_pos + force_scale * (avoidance_direction + 0.5 * to_target)
            break
        
        if phi_val <=  -90:  # Verificando a intensidade nos arredores
            avoidance_direction = new_pos - obs  # Vetor apontando para longe do obstáculo + componente aléatorio
            if np.linalg.norm(avoidance_direction) > 0:
                avoidance_direction /= np.linalg.norm(avoidance_direction)
                
            target_influence = 2 * to_target # dando mais importância ao alvo
            new_pos = current_pos + force_scale * (avoidance_direction + target_influence)
            
            print(f"Adjusting path due to obstacle. New position: {new_pos}, Target influence: {target_influence}")
            break
        
            
    if 0 <= new_pos[0] < size and 0 <= new_pos[1] < size: # Verifica se a nova posição de escape está dentro dos limites do grid.
        current_pos[:] = new_pos
      
        
    robot_circle.center = current_pos
    trajectory_line.set_data([p[0] for p in trajectory], [p[1] for p in trajectory])
    trajectory.append(current_pos.copy())
    

        

    return robot_circle, trajectory_line,

# Animação
ani = FuncAnimation(fig, update, frames=range(2000), blit=True, interval=20, repeat=False)
plt.show()
