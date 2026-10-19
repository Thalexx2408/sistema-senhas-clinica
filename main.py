import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import heapq

# =====================================================================
# ESTRUTURAS DE DADOS E LÓGICA DE NEGÓCIO
# =====================================================================

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

    def estimar_tempo(self, senha):
        if senha not in self.pacientes_ativos:
            return -1
        
        pac_buscado = self.pacientes_ativos[senha]
        posicao = 0
        
        if pac_buscado.tipo == 'P':
            for cat, ordem, p in self.fila_prioridade:
                if cat < pac_buscado.categoria or (cat == pac_buscado.categoria and ordem < pac_buscado.ordem):
                    posicao += 1
        else:
            posicao += len(self.fila_prioridade)
            for p in self.fila_normal:
                if p.ordem < pac_buscado.ordem:
                    posicao += 1
                    
        return posicao * 30

# =====================================================================
# INTERFACE GRÁFICA (TKINTER)
# =====================================================================

class ClinicaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Senhas - Clínica Médica")
        self.geometry("700x500")
        
        self.especialidades_disponiveis = [
            "Clínica Geral", "Pediatria", "Ginecologia", "Cardiologia", "Psiquiatria"
        ]
        self.categorias_prioridade = {
            "1 - 80 anos ou mais": 1,
            "2 - Idosos (60 a 79 anos)": 2,
            "3 - Pessoas com deficiência (PCD)": 3,
            "4 - Gestantes": 4,
            "5 - Pessoas com obesidade": 5,
            "6 - Acompanhadas de criança de colo": 6
        }
        
        self.clinicas = {}
        self.contador_ids = 1
        self.ultima_chamada = {"senha": "Nenhuma", "especialidade": "-", "tipo": "-"}

        self.criar_menu_lateral()
        self.container = tk.Frame(self)
        self.container.pack(side="right", fill="both", expand=True)
        
        self.frames = {}
        for F in (TelaMenu, TelaCadastro, TelaEmissao, TelaGerenciamento, TelaPainel, TelaTempo):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.mostrar_frame(TelaMenu)

    def criar_menu_lateral(self):
        menu = tk.Frame(self, bg="#2c3e50", width=200)
        menu.pack(side="left", fill="y")
        tk.Label(menu, text="Menu Principal", bg="#2c3e50", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
        
        botoes = [
            ("🏠 Início", TelaMenu), ("⚙️ Especialidades", TelaCadastro),
            ("🎟️ Emitir Senha", TelaEmissao), ("📋 Gerenciar Filas", TelaGerenciamento),
            ("📺 Painel", TelaPainel), ("⏱️ Tempo de Espera", TelaTempo)
        ]
        for texto, frame in botoes:
            tk.Button(menu, text=texto, bg="#34495e", fg="white", relief="flat", 
                      command=lambda f=frame: self.mostrar_frame(f)).pack(fill="x", pady=5, padx=10)

    def mostrar_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, 'atualizar'):
            frame.atualizar()

class TelaMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Sistema de Gerenciamento de Senhas", font=("Arial", 18, "bold")).pack(pady=50)
        tk.Label(self, text="Selecione uma opção no menu lateral para começar.", font=("Arial", 12)).pack()

class TelaCadastro(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Cadastro de Especialidades (Máx. 3)", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.combo_esp = ttk.Combobox(self, values=controller.especialidades_disponiveis, state="readonly", width=30)
        self.combo_esp.pack(pady=10)
        tk.Button(self, text="Cadastrar Especialidade", command=self.cadastrar).pack(pady=10)
        
        self.lista_label = tk.Label(self, text="", font=("Arial", 12), justify="left")
        self.lista_label.pack(pady=20)

    def cadastrar(self):
        nome = self.combo_esp.get()
        if not nome: return messagebox.showwarning("Aviso", "Selecione uma especialidade.")
        if len(self.controller.clinicas) >= 3: return messagebox.showerror("Erro", "Limite máximo de 3 atingido!")
        if any(fila.nome == nome for fila in self.controller.clinicas.values()):
            return messagebox.showerror("Erro", "Especialidade já cadastrada!")
            
        id_esp = f"C{self.controller.contador_ids}"
        self.controller.clinicas[id_esp] = FilaEspecialidade(nome, id_esp)
        self.controller.contador_ids += 1
        messagebox.showinfo("Sucesso", f"{nome} ({id_esp}) cadastrada!")
        self.atualizar()

    def atualizar(self):
        texto = "Especialidades Cadastradas:\n\n"
        for id_esp, fila in self.controller.clinicas.items(): texto += f"{id_esp} — {fila.nome}\n"
        self.lista_label.config(text=texto)

class TelaEmissao(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Emissão de Senhas", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.combo_esp = ttk.Combobox(self, state="readonly", width=30)
        self.combo_esp.pack(pady=5)
        
        self.tipo_var = tk.StringVar(value="N")
        tk.Radiobutton(self, text="Normal", variable=self.tipo_var, value="N", command=self.toggle_prioridade).pack()
        tk.Radiobutton(self, text="Prioritário", variable=self.tipo_var, value="P", command=self.toggle_prioridade).pack()
        
        self.combo_prioridade = ttk.Combobox(self, values=list(controller.categorias_prioridade.keys()), state="readonly", width=40)
        self.combo_prioridade.pack(pady=10)
        self.combo_prioridade.configure(state="disabled")
        
        tk.Button(self, text="Gerar Senha", command=self.emitir).pack(pady=10)
        self.lbl_senha = tk.Label(self, text="", font=("Arial", 24, "bold"), fg="blue")
        self.lbl_senha.pack(pady=20)

    def toggle_prioridade(self):
        if self.tipo_var.get() == "P": self.combo_prioridade.configure(state="readonly")
        else:
            self.combo_prioridade.set("")
            self.combo_prioridade.configure(state="disabled")

    def atualizar(self):
        self.combo_esp.configure(values=[f"{id_esp} - {fila.nome}" for id_esp, fila in self.controller.clinicas.items()])

    def emitir(self):
        sel_esp = self.combo_esp.get()
        if not sel_esp: return messagebox.showwarning("Aviso", "Selecione a especialidade.")
        
        id_esp = sel_esp.split(" - ")[0]
        fila = self.controller.clinicas[id_esp]
        
        if self.tipo_var.get() == "N": senha = fila.adicionar_normal()
        else:
            cat_str = self.combo_prioridade.get()
            if not cat_str: return messagebox.showwarning("Aviso", "Selecione a categoria de prioridade.")
            senha = fila.adicionar_prioridade(self.controller.categorias_prioridade[cat_str])
            
        self.lbl_senha.config(text=f"SENHA: {senha}")

class TelaGerenciamento(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Gerenciamento de Filas", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.combo_esp = ttk.Combobox(self, state="readonly", width=30)
        self.combo_esp.pack(pady=5)
        self.combo_esp.bind("<<ComboboxSelected>>", lambda e: self.atualizar_lista())
        
        tk.Button(self, text="Chamar Próximo Paciente", bg="green", fg="white", command=self.chamar).pack(pady=10)
        self.txt_filas = tk.Text(self, width=50, height=15, state="disabled")
        self.txt_filas.pack(pady=10)

    def atualizar(self):
        self.combo_esp.configure(values=[f"{id_esp} - {fila.nome}" for id_esp, fila in self.controller.clinicas.items()])
        self.atualizar_lista()

    def atualizar_lista(self):
        sel_esp = self.combo_esp.get()
        self.txt_filas.config(state="normal")
        self.txt_filas.delete(1.0, tk.END)
        if not sel_esp:
            self.txt_filas.insert(tk.END, "Selecione uma especialidade acima.")
            self.txt_filas.config(state="disabled")
            return
            
        fila = self.controller.clinicas[sel_esp.split(" - ")[0]]
        texto = f"Especialidade: {fila.nome}\nAguardando: {len(fila.fila_prioridade) + len(fila.fila_normal)}\n"
        texto += f"Prioridades: {len(fila.fila_prioridade)} | Normais: {len(fila.fila_normal)}\n\nOrdem Prevista:\n"
        
        temp_heap = fila.fila_prioridade.copy()
        temp_heap.sort()
        for _, _, pac in temp_heap: texto += f"- {pac.senha} (Prioridade)\n"
        for pac in fila.fila_normal: texto += f"- {pac.senha} (Normal)\n"
            
        self.txt_filas.insert(tk.END, texto)
        self.txt_filas.config(state="disabled")

    def chamar(self):
        sel_esp = self.combo_esp.get()
        if not sel_esp: return messagebox.showwarning("Aviso", "Selecione uma especialidade.")
        
        fila = self.controller.clinicas[sel_esp.split(" - ")[0]]
        pac = fila.chamar_proximo()
        if pac:
            self.controller.ultima_chamada = {"senha": pac.senha, "especialidade": fila.nome, "tipo": "Prioritário" if pac.tipo == 'P' else "Normal"}
            messagebox.showinfo("Chamada", f"Paciente {pac.senha} chamado