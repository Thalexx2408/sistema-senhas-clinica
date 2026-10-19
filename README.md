# Sistema de Gerenciamento de Senhas - Clínica Médica

**Disciplina:** Estrutura de Dados II  
**Curso:** Tecnologia da Informação  
**Professora:** Profa. Karla Sartin  
**Integrantes:** [Seu Nome], [Nome 2], [Nome 3]  

## 1. Situação-Problema
A clínica médica enfrentava dificuldades com o controle manual das filas de atendimento. Isso dificultava o controle da ordem de chegada, a gestão das regras legais de prioridade e o cálculo do tempo de espera. Para solucionar o problema, foi desenvolvido este sistema para automatizar a emissão e chamada de senhas.

## 2. Objetivo do Sistema
Automatizar o gerenciamento de filas da clínica por meio de uma interface gráfica intuitiva, implementando regras rigorosas de controle baseadas em conceitos de Filas FIFO e Filas de Prioridade, além de fornecer aos pacientes uma estimativa do tempo de espera.

## 3. Tecnologias e Bibliotecas Utilizadas
* **Linguagem:** Python 3.x
* **Interface Gráfica:** Tkinter (biblioteca padrão)
* **Estruturas de Dados:** `collections.deque` e `heapq` (built-in do Python)

## 4. Estruturas de Dados Implementadas
* **Fila Normal (FIFO):** Implementada utilizando `collections.deque`. O `deque` garante complexidade O(1) para operações de inserção e remoção no início, sendo a estrutura ideal para manter a ordem de chegada.
* **Fila de Prioridades:** Implementada através de uma lista manipulada pela biblioteca `heapq` (Min-Heap). O Min-Heap garante que a prioridade máxima legal fique no topo da árvore binária em complexidade O(log N). A ordem de chegada serve como critério de desempate.

## 5. Funcionalidades
* **Cadastro:** Registro de até 3 especialidades independentes.
* **Emissão:** Geração automática e sequencial de senhas.
* **Fila de Atendimento:** Painel para gerenciamento interno.
* **Painel do Paciente:** Exibição da última senha chamada de forma visual.
* **Tempo de Espera:** Algoritmo que calcula a estimativa em minutos.

## 6. Instruções de Execução
1. Certifique-se de ter o Python 3 instalado.
2. Clone o repositório.
3. Execute o arquivo principal via terminal: `python main.py`

## 7. Vídeo Demonstrativo
* **Link:** [Coloque o link do YouTube ou Drive aqui após gravarem]