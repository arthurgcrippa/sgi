# Trabalho 1 da Disciplina de Computação Gráfica  

Object3D:
Você pode adicionar um objeto pela interface colocando sua lista de pontos no formato (x1,y1,z1);(x2,y2,z2)... especificado no input padrão da UI e logo abaixo colocar as sequencias de arestas entre os pontos de modo que (1,2,3,4) significa que os pontos (p1,p2) , (p2,p3) e (p3,p4) pertencerão ao objeto. Para desenhar um poliedro onde não é possível ligar todas as arestas partindo de uma você pode colocar sequências de arestas seguindo o modelo padrão do input. (1,2,3,4,1);(1,5);(2,5);(3,5);(4,5) ou alternativamente (1,2,3,4,1);(1,5,2);(3,5,4).

IMPORTANTE: O modelo mencionado anteriormente de arestas foi revistado. A forma descrita acima ainda é operante e funciona perfeitamente bem para Wireframe ou seja modelos de arame não preenchidos. Para que possamos preencher o poliedro é preciso sabermos quais são as faces que ele possui e neste caso o usuário deve descrever todas as faces da mesma forma que um arquivo .obj faz. O exemplo acima ficaria (1,2,3,4,1);(1,5,2,1);(2,5,3,2);(3,5,4,3);(4,5,1,4)


Transformation 3D:
A translação e escalonamento só requerem um ponto com 3 coordenadas que será aplicado sobre o objeto. A rotação todavia depende de dois fatores sendo eles o eixo pelo qual o objeto vai rodar e o ponto de referência de rotação. Ambas as escolhas possuem padrões implícitos ou podem ser colocadas pelo usuário. As opções de eixo padrão são x, y e z indicando que o objeto irá rotacionar sobre um destes vetores. Alternativamente você pode colocar o seu próprio vetor no formato (x,y,z) e.g (1,1,0) e ver o seu objeto rotacionar ao redor dele. Além disso o objeto pode rotacionar ao redor do vetor escolhido mas em relação há um ponto que pode ser inserido pelo usuário, ou pode ser selecionado pela interface para ser o centro do objeto ou a origem. 

Projection:
No canto esquerdo da tela de navegação você pode selecionar entre os eixos x, y e z para rotacionar o mundo movendo os objetos que nele se encontram. No entanto os objetos rotacionados apresentam certa distorção em determinados pontos dependendo do angulo de rotação composto entre os 3 eixos em função de um problema de divisão por 0 encontrado ao aplicar e normaliar os pontos do objeto aplicada a matriz da projeção. Além dos botões de navegação comum (left, right, up, down) foram inclusos dois botões - setas - que afastam e aproximam o objeto tornando mais perceptível as linhas traseiras do objeto - efeito da projeção - se afastando.

Superficies:
A interface de superficies conta com botões para selecionar entre os métodos de bezier, hermite e bspline bem como a escolha do algoritmo - se blending functions ou forwarding differences - e possui uma caixa de testo para que se possa colocar os pontos. Visto que no nosso trabalho até agora estivemos usando (x1,y1,z1);(x2,y2,z2) ou seja ',' como separador intracoordenada e ';' como separador intercoordenada optamos por utilizar '\n' como separador para as linhas da matriz. Ou seja, você escreve uma linha no formato que viemos empregando até agora e aperta enter para escrever a próxima. Como isso seria muito custoso e cansativo para entradas enormes damos a opção de carregar um arquivo .txt com os pontos. Na pasta surfaces temos 3 exemplos prontos para serem carregados. 


Wavefront:
Dentro da pasta savefiles há arquivos .obj que você pode abrir e salvar através da interface de manipulação de arquivos. 

