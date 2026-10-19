import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import heapq

class Paciente:
    def __init__(self, id_esp, tipo, categoria=None, numero=0, ordem_chegada=0):
        self.senha = f"{id_esp}-{tipo}{numero:03d}"
        self.tipo = tipo
        self.categoria = categoria
        self.ordem = ordem_chegada

class FilaEspecialidade:
    def __init__(self, nome, id_esp):
        self.nome = nome
        self.id_esp = id_esp
        self.fila_normal = deque()
        self.fila_prioridade = []
        self.contador_normal = 1
        self.contador_prioridade = 1
        self.ordem_global = 1
        self.pacientes_ativos = {}

    def adicionar_normal(self):
        pac = Paciente(self.id_esp, 'N', 99, self.contador_normal, self.ordem_global)
        self.fila_normal.append(pac)
        self.pacientes_ativos[pac.senha] = pac
        self.contador_normal += 1
        self.ordem_global += 1
        return pac.senha

    def adicionar_prioridade(self, categoria):
        pac = Paciente(self.id_esp, 'P', categoria, self.contador_prioridade, self.ordem_global)
        heapq.heappush(self.fila_prioridade, (categoria, self.ordem_global, pac))
        self.pacientes_ativos[pac.senha] = pac
        self.contador_prioridade += 1
        self.ordem_global += 1
        return pac.senha

    def chamar_proximo(self):
        if self.fila_prioridade:
            _, _, pac = heapq.heappop(self.fila_prioridade)
            del self.pacientes_ativos[pac.senha]
            return pac
        elif self.fila_normal:
            pac = self.fila_normal.popleft()
            del self.pacientes_ativos[pac.senha]
            return pac
        return None