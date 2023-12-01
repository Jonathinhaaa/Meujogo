import tkinter as tk
from tkinter import messagebox
import random
import time
import pygame

class JogoMatematica:
    def __init__(self, root):
        self.root = root
        self.inicializar_interface()

    def inicializar_interface(self):
        self.frame_configuracao = tk.Frame(self.root)
        self.frame_configuracao.pack(padx=50, pady=50)

        self.label_instrucao = tk.Label(self.frame_configuracao, text="Escolha as operações:")
        self.label_instrucao.pack()

        self.var_adicao = tk.BooleanVar()
        self.var_subtracao = tk.BooleanVar()
        self.var_multiplicacao = tk.BooleanVar()
        self.var_divisao = tk.BooleanVar()

        self.checkbox_adicao = tk.Checkbutton(self.frame_configuracao, text="Adição", variable=self.var_adicao)
        self.checkbox_subtracao = tk.Checkbutton(self.frame_configuracao, text="Subtração", variable=self.var_subtracao)
        self.checkbox_multiplicacao = tk.Checkbutton(self.frame_configuracao, text="Multiplicação", variable=self.var_multiplicacao)
        self.checkbox_divisao = tk.Checkbutton(self.frame_configuracao, text="Divisão", variable=self.var_divisao)

        self.checkbox_adicao.pack(anchor=tk.W)
        self.checkbox_subtracao.pack(anchor=tk.W)
        self.checkbox_multiplicacao.pack(anchor=tk.W)
        self.checkbox_divisao.pack(anchor=tk.W)

        self.label_vidas = tk.Label(self.frame_configuracao, text="Quantidade de Vidas:")
        self.label_vidas.pack()

        self.entry_vidas = tk.Entry(self.frame_configuracao)
        self.entry_vidas.pack()

        self.label_dificuldade = tk.Label(self.frame_configuracao, text="Nível de Dificuldade (1 para fácil, 2 para médio, 3 para difícil):")
        self.label_dificuldade.pack()

        self.entry_dificuldade = tk.Entry(self.frame_configuracao)
        self.entry_dificuldade.pack()

        self.label_perguntas = tk.Label(self.frame_configuracao, text="Número de Perguntas:")
        self.label_perguntas.pack()

        self.entry_perguntas = tk.Entry(self.frame_configuracao)
        self.entry_perguntas.pack()

        self.botao_iniciar = tk.Button(self.frame_configuracao, text="Iniciar Jogo", command=self.iniciar_jogo)
        self.botao_iniciar.pack()

    def iniciar_jogo(self):
        operacoes_selecionadas = []

        if self.var_adicao.get():
            operacoes_selecionadas.append('+')
        if self.var_subtracao.get():
            operacoes_selecionadas.append('-')
        if self.var_multiplicacao.get():
            operacoes_selecionadas.append('*')
        if self.var_divisao.get():
            operacoes_selecionadas.append('/')

        if not operacoes_selecionadas:
            messagebox.showerror("Erro", "Selecione pelo menos uma operação.")
            return

        num_vidas = int(self.entry_vidas.get())
        nivel_dificuldade = int(self.entry_dificuldade.get())
        num_perguntas = int(self.entry_perguntas.get())

        if num_vidas <= 0 or nivel_dificuldade not in [1, 2, 3] or num_perguntas <= 0:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
            return

        self.frame_configuracao.destroy()

        jogo = JogoMatematicaPrincipal(self.root, num_perguntas, nivel_dificuldade, operacoes_selecionadas, num_vidas)

class JogoMatematicaPrincipal:
    def __init__(self, root, num_perguntas, nivel_dificuldade, operacoes, num_vidas):
        self.root = root
        self.inicializar_atributos(num_perguntas, num_vidas)
        self.operacoes = operacoes
        self.pontuacao = 0
        self.nivel_dificuldade = nivel_dificuldade
        self.num_vidas = num_vidas
        self.historico_perguntas = []
        self.inicializar_interface()
        self.inicializar_musica()

    def inicializar_atributos(self, num_perguntas, num_vidas):
        self.num_perguntas_inicial = num_perguntas
        self.num_perguntas = num_perguntas
        self.num_vidas_inicial = num_vidas
        self.num_vidas = num_vidas
        self.tempo_inicio = 0
        self.tempo_total = 0
        self.recompensa_resposta_rapida = 0.5
        self.penalidade_resposta_incorreta = 0.2
        self.penalidade_vida_perdida = 0.3

    def inicializar_interface(self):
        self.frame_jogo = tk.Frame(self.root, padx=50, pady=50)
        self.frame_jogo.pack()

        self.label_pergunta = tk.Label(self.frame_jogo, text="", font=("Helvetica", 16))
        self.label_pergunta.pack(pady=10)

        self.entry_resposta = tk.Entry(self.frame_jogo, font=("Helvetica", 16))
        self.entry_resposta.pack(pady=10)
        self.entry_resposta.bind("<Return>", self.verificar_resposta)

        self.botao_responder = tk.Button(self.frame_jogo, text="Responder", command=self.verificar_resposta, font=("Helvetica", 14))
        self.botao_responder.pack(pady=10)

        self.gerar_pergunta()
        self.tempo_inicio = time.time()

    def inicializar_musica(self):
        pygame.mixer.init()
        pygame.mixer.music.load("lofi.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def gerar_pergunta(self):
        num1 = random.randint(1, 10 * self.nivel_dificuldade)
        num2 = random.randint(1, 10 * self.nivel_dificuldade)
        operador = random.choice(self.operacoes)

        if operador == '/':
            num2 = random.randint(1, 10 * self.nivel_dificuldade)

        pergunta = f"{num1} {operador} {num2}"
        resposta_correta = eval(pergunta)

        self.label_pergunta.config(text=f"{num1} {operador} {num2} =", font=("Helvetica", 16))
        self.resposta_correta = resposta_correta

    def verificar_resposta(self, event=None):
        resposta_usuario = self.entry_resposta.get()

        try:
            resposta_usuario = float(resposta_usuario)
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido.")
            return

        tempo_pergunta = time.time() - self.tempo_inicio
        self.tempo_total += tempo_pergunta

        self.historico_perguntas.append({
            'Pergunta': self.label_pergunta.cget("text"),
            'Resposta do Usuário': resposta_usuario,
            'Resposta Correta': self.resposta_correta,
            'Tempo de Resposta': round(tempo_pergunta, 2)
        })

        diferenca = abs(resposta_usuario - self.resposta_correta)
        pontuacao_parcial = max(0, 1 - diferenca / max(1, abs(self.resposta_correta)))

        if pontuacao_parcial >= 0.5:
            messagebox.showinfo("Parcialmente Correto", f"Sua resposta está parcialmente correta!")
            self.pontuacao += pontuacao_parcial + self.recompensa_resposta_rapida
        elif resposta_usuario == self.resposta_correta:
            messagebox.showinfo("Correto!", "Resposta correta!")
            self.pontuacao += 1
        else:
            messagebox.showinfo("Incorreto", f"Incorreto. A resposta correta era {self.resposta_correta}")

            self.pontuacao -= self.penalidade_resposta_incorreta

            if self.num_vidas > 0:
                self.num_vidas -= 1
                self.pontuacao -= self.penalidade_vida_perdida
                messagebox.showinfo("Vida Perdida", f"Você perdeu uma vida! Vidas restantes: {self.num_vidas}")
            else:
                self.finalizar_jogo()
                return

        self.num_perguntas -= 1
        if self.num_perguntas > 0:
            self.gerar_pergunta()
            self.tempo_inicio = time.time()
        else:
            self.finalizar_jogo()

    def finalizar_jogo(self):
        pygame.mixer.music.stop()
        pontuacao_final = round(self.pontuacao / self.num_perguntas_inicial * 100, 2)
        tempo_medio_por_pergunta = round(self.tempo_total / self.num_perguntas_inicial, 2)

        relatorio = f"Sua pontuação final é {pontuacao_final}%\n\n"
        relatorio += f"Tempo médio por pergunta: {tempo_medio_por_pergunta} segundos\n\n"
        relatorio += "Histórico de perguntas:\n"

        for pergunta in self.historico_perguntas:
            relatorio += f"\nPergunta: {pergunta['Pergunta']}\n"
            relatorio += f"Resposta do Usuário: {pergunta['Resposta do Usuário']}\n"
            relatorio += f"Resposta Correta: {pergunta['Resposta Correta']}\n"
            relatorio += f"Tempo de Resposta: {pergunta['Tempo de Resposta']} segundos\n"

        relatorio += f"\nRecompensas e Penalidades:\n"
        relatorio += f"Pontos por resposta rápida: +{self.recompensa_resposta_rapida}\n"
        relatorio += f"Pontos por resposta correta: +1\n"
        relatorio += f"Pontos por resposta incorreta: -{self.penalidade_resposta_incorreta}\n"
        relatorio += f"Pontos por perder uma vida: -{self.penalidade_vida_perdida}\n"

        messagebox.showinfo("Fim do jogo", relatorio)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jogo de Matemática")

    jogo_config = JogoMatematica(root)

    root.mainloop()
