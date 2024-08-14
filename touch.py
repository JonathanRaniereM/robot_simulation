import numpy as np
import matplotlib.pyplot as plt

class TouchSimulator:
    def __init__(self, size=100, touch_intensity=500, decay_rate=0.2):
        # Inicializa a simulação com uma grade quadrada.
        self.size = size
        self.touch_intensity = touch_intensity
        self.grid = np.zeros((size, size))
        self.decay_rate = decay_rate
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.grid, cmap='viridis', interpolation='nearest', vmin=0, vmax=touch_intensity)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.colorbar(self.im)
        plt.title('Simulação Interativa do Campo Elétrico em uma Tela Capacitiva')

    def on_click(self, event):
        # Detecta cliques na tela e aplica um "toque".
        if event.inaxes == self.ax:
            x, y = int(event.ydata), int(event.xdata)
            self.apply_touch(x, y)
            self.update_field()

    def apply_touch(self, x, y):
        # Simula um toque aplicando uma intensidade de carga num raio definido.
        radius = 5
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    self.grid[x + dx, y + dy] += self.touch_intensity

    def update_field(self):
        # Utiliza a Equação de Laplace para simular a distribuição do campo elétrico após um toque.
        new_grid = self.grid.copy()
        tolerance = 1e-5  
        for _ in range(50):  
            old_grid = new_grid.copy()
            # Aplicação iterativa da Equação de Laplace para calcular o potencial em cada ponto
            new_grid[1:-1, 1:-1] = 0.25 * (old_grid[:-2, 1:-1] + old_grid[2:, 1:-1] + old_grid[1:-1, :-2] + old_grid[1:-1, 2:])
            max_change = np.max(np.abs(new_grid - old_grid))
            if max_change < tolerance:
                break  # Sai do loop se a mudança for menor que a tolerância
        self.grid = new_grid * (1 - self.decay_rate)  # Aplica o decaimento para simular perda de carga
        self.im.set_data(self.grid)
        self.fig.canvas.draw_idle()  # Atualiza a visualização


    def show(self):
        plt.show()

# Cria e inicia a instância do simulador para visualização
simulator = TouchSimulator()
simulator.show()
