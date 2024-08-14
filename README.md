# A Equação de Laplace para Navegação de Robôs Móveis

<img width="700" src="https://raw.githubusercontent.com/JonathanRaniereM/robot_simulation/main/representation/simulation.gif">

## Sobre o Projeto

 O algoritmo desenvolvido emprega o Método de Relaxação iterativa, como parte do qual o Método de Jacob é utilizado, para calcular o potencial em cada ponto do domínio. Além disso, a formação de campos potenciais é adotada para orientar o movimento do robô em direção ao objetivo, ao mesmo tempo em que evita obstáculos. Essa combinação de técnicas visa fornecer uma abordagem eficaz para a navegação de robôs móveis em ambientes desconhecidos e dinâmicos, aproveitando os princípios fundamentais da Equação de Laplace e da formação de campos potenciais na robótica móvel. 

### Características Principais

- **MÉTODO DE JACOB**: O método de Jacob (equação de Laplace discretizada) é um método iterativo utilizado para resolver sistemas lineares de equações, incluindo sistemas representados na forma matricial. Na sua forma mais básica, o método de Jacob envolve a iteração através de uma série de equações lineares, onde cada equação é atualizada individualmente com base nos valores atuais das outras equações.
  
- **CÁUCULO DO GRADIENTE E MOVIMENTO DO ROBÔ**: O gradiente do campo indica a direção de maior aumento do potencial. Na etapa de movimento, o robô se desloca na direção oposta ao gradiente, ou seja, em direção à maior descida do potencial, o que naturalmente o direciona para longe dos obstáculos e em direção ao objetivo. 

- **ATUALIZAÇÃO DA ANIMAÇÃO**: Além de seguir a direção oposta ao gradiente, o robô pode combinar esta direção com um vetor apontando diretamente para a meta. Isso ajuda o robô a não apenas evitar obstáculos mas também a se mover efetivamente em direção ao objetivo final.

- **MEDIDAS DE SEGURANÇA**: Para cada obstáculo no ambiente, é calculada a distância entre a nova posição prevista do robô e o obstáculo. Se essa distância for menor que uma distância segura predefinida, significa que o robô está muito próximo de um obstáculo e precisa ajustar sua direção para evitar uma colisão,ou seja, casos onde obstaculos sem potenciais calculados tem garantia de desvio nessas condições.  


## Motivação

Este projeto foi desenvolvido visando atender soluções de Equações Diferenciais no ambiente academico, no intuito de gerar discussões sobre a aplicação em questão, além de sugestões de melhorias ao projeto, promovendo assim, um ambiente de aprendizado colaborativo e engajador.


## Contribuição

Sua contribuição é bem-vinda! Se você tem interesse em contribuir para o projeto, por favor, leia o arquivo CONTRIBUTING.md para mais informações sobre como proceder.



Para mais informações, por favor, entre em contato conosco através de enginerdeveloper7@gmail.com.

Agradecemos seu interesse e apoio ao nosso projeto!
