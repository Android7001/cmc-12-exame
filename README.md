CMC-12 - Exame : Simulação de Caminhada de Robô Humanóide

Integrantes do Grupo
    Marcos Levi
    Rafael Bittar
    Davi Lessa

Descrição do Projeto
    Este projeto é dedicado à simulação da caminhada de um robô humanóide. No entanto, implementamos apenas a simulação do centro de massa e dos dois pés do robô. A parte das pernas, incluindo o cálculo dos ângulos por cinemática inversa, não foi incluída.

Estrutura do Projeto
    O projeto é composto por três arquivos principais:
        -> cm.py: Implementa a classe referente ao Centro de Massa.
        -> foot.py: Implementa a classe referente a um pé.
        -> simulacao.py: Responsável pela simulação, contendo a lógica para unir os dois pés e o centro de massa.

Requisitos
    Para rodar a simulação, são necessárias as seguintes bibliotecas: numpy e matplotlib. 
        Você pode instalá-las usando o seguinte comando: pip install numpy matplotlib

Simulação
    Para rodar a simulação, basta executar o arquivo simulacao.py (para compilá-lo e executálo: python simulacao.py). Vale ressaltar, caso opte por mudançã de parâmetros como os valores das velocidades, precisará também alterar parãmetros como as dimensões dos eixos, os quais estão devidamente identificados por comentários
        