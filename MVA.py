import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import json
from datetime import datetime

def centralizar_janela(janela, largura_janela, altura_janela):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    posicao_x = (largura_tela - largura_janela) // 2
    posicao_y = (altura_tela - altura_janela) // 2

    janela.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

def fechar_janela_atual():
    janela_atual.quit()
    janela_atual.destroy()

def abrir_nova_janela():
    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"

    if os.path.exists(arquivo_mes):
        with open(arquivo_mes, "r", encoding="utf-8") as file:
            informacoes = json.load(file)
        exibir_informacoes(mes_escolhido, informacoes)
    else:
        mensagem = f"O arquivo para o mês de {mes_escolhido} não foi encontrado. Deseja adicionar um novo registro?"
        resposta = messagebox.askyesno("Registro não encontrado", mensagem)
        if resposta:
            criar_novo_registro(mes_escolhido)
            abrir_nova_janela()

def criar_novo_registro(mes):
    arquivo_mes = f"{mes}.json"
    with open(arquivo_mes, "w", encoding="utf-8") as file:
        json.dump({}, file)

def exibir_informacoes(mes, informacoes):

    global planilha
    global janela_atual

    janela_atual = tk.Toplevel(janela)
    janela_atual.title(f"Informações de {mes}")
    janela_atual.geometry("600x400")
    centralizar_janela(janela_atual,600,400)

    planilha = ttk.Treeview(janela_atual, columns=("NF", "Fornecedor", "Data de Chegada", "Destinatario"))
    planilha.heading("NF", text="NF")
    planilha.heading("Fornecedor", text="Fornecedor")
    planilha.heading("Data de Chegada", text="Data de Chegada")
    planilha.heading("Destinatario", text="Destinatario")

    planilha.column("#0", width=0, stretch="NO")
    planilha.column("NF", width=120, stretch="NO")
    planilha.column("Fornecedor", width=120, stretch="NO")
    planilha.column("Data de Chegada", width=120, stretch="NO")
    planilha.column("Destinatario", width=120, stretch="NO")

    planilha.bind("<Button-1>", lambda e: "break")

    planilha.pack(padx=20, pady=20)

    adicionar_mercadoria_button = ttk.Button(janela_atual, text="Adicionar Mercadoria", command=adicionar_nova_mercadoria)
    adicionar_mercadoria_button.pack(pady=10)

def adicionar_nova_mercadoria():
    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"

    if not os.path.exists(arquivo_mes):
        messagebox.showerror("Erro", f"O arquivo para o mês de {mes_escolhido} não existe.")
        return

    nova_janela = tk.Toplevel(janela_atual)
    nova_janela.title("Adicionar Nova Mercadoria")
    centralizar_janela(nova_janela, 500, 350)

    nf_label = ttk.Label(nova_janela, text="Nota Fiscal:")
    nf_label.pack(pady=5)

    nf_entry = ttk.Entry(nova_janela)
    nf_entry.pack(pady=5)

    fornecedor_label = ttk.Label(nova_janela, text="Fornecedor:")
    fornecedor_label.pack(pady=5)

    fornecedor_entry = ttk.Entry(nova_janela)
    fornecedor_entry.pack(pady=5)

    data_label = ttk.Label(nova_janela, text="Data de Chegada (dd/mm/yyyy):")
    data_label.pack(pady=5)

    data_entry = ttk.Entry(nova_janela)
    data_entry.pack(pady=5)

    Destinatario_label = ttk.Label(nova_janela, text="Destinatario:")
    Destinatario_label.pack(pady=5)

    Destinatario_combobox = ttk.Combobox(nova_janela, values=["MVA", "Eletronica Horizonte"])
    Destinatario_combobox.pack(pady=5)

    salvar_button = ttk.Button(nova_janela, text="Salvar", command=lambda: salvar_nova_mercadoria(nf_entry.get(), fornecedor_entry.get(), data_entry.get(), Destinatario_combobox.get()))

    salvar_button.pack(pady=10)

    # Após a janela de edição ser fechada, atualize a planilha
    nova_janela.protocol("WM_DELETE_WINDOW", lambda: atualizar_planilha())


def salvar_nova_mercadoria(nf, fornecedor, data, Destinatario):
    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"

    if nf and fornecedor and data and Destinatario:
        try:
            data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use dd/mm/yyyy.")
            return

        if os.path.exists(arquivo_mes):
            with open(arquivo_mes, "r", encoding="utf-8") as file:
                informacoes = json.load(file)
        else:
            informacoes = {}

        nova_mercadoria = {"NF": nf, "Fornecedor": fornecedor, "Data de Chegada": data_formatada, "Destinatario": Destinatario}

        # Adicione a nova mercadoria ao dicionário de informações
        informacoes[nf] = nova_mercadoria  # Use NF como chave

        # Atualize o arquivo JSON com os novos dados
        with open(arquivo_mes, "w", encoding="utf-8") as file:
            json.dump(informacoes, file, ensure_ascii=False, indent=4)

        # Atualize a planilha na janela principal
        atualizar_planilha(planilha, mes_escolhido)

        # Feche a janela atual
        janela_atual.destroy()
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def atualizar_planilha(planilha, mes_escolhido):
    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"

    if os.path.exists(arquivo_mes):
        with open(arquivo_mes, "r", encoding="utf-8") as file:
            informacoes = json.load(file)
        
        # Limpe a planilha antes de atualizá-la
        for item in planilha.get_children():
            planilha.delete(item)
        
        # Preencha a planilha com os dados do arquivo JSON
        for nf, dados in informacoes.items():
            planilha.insert("", "end", values=(nf, dados["Fornecedor"], dados["Data de Chegada"], dados["Destinatario"]))


def deletar_dados():
    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"

    if os.path.exists(arquivo_mes):
        mensagem = f"Tem certeza de que deseja excluir os dados do mês de {mes_escolhido}?"
        resposta = messagebox.askyesno("Confirmar Exclusão", mensagem)
        if resposta:
            os.remove(arquivo_mes)
            messagebox.showinfo("Sucesso", f"Os dados do mês de {mes_escolhido} foram excluídos com sucesso.")
    else:
        messagebox.showwarning("Aviso", f"O arquivo para o mês de {mes_escolhido} não existe.")

meses_informacoes = {
    "Janeiro": {"Descrição": "Este é o mês de Janeiro.", "Outras Informações": "Algumas informações adicionais."},
    "Fevereiro": {"Descrição": "Este é o mês de Fevereiro.", "Outras Informações": "Mais informações aqui."},
}

planilha = None
janela = tk.Tk()
janela.title("Checar Mercadorias")
centralizar_janela(janela,400,200)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 14), foreground="blue")
style.configure("TFrame", background="#e1e1e1")
style.configure("TCombobox", font=("Helvetica", 12), justify="center")

pergunta_label = ttk.Label(janela, text="Checar Mercadorias de que Mês?")
pergunta_label.pack(pady=10)

container = ttk.Frame(janela)
container.pack(pady=10)

mes_var = tk.StringVar()
mes_var.set("Janeiro")
meses = list(meses_informacoes.keys())

mes_dropdown = ttk.Combobox(container, textvariable=mes_var, values=meses, state="readonly")
mes_dropdown.pack(side="left")

ok_button = ttk.Button(janela, text="OK", command=abrir_nova_janela)
ok_button.pack(pady=10)

deletar_button = ttk.Button(janela, text="Deletar Dados", command=deletar_dados)
deletar_button.pack(pady=10)

fechar_button = ttk.Button(janela, text="Fechar", command=janela.quit)
fechar_button.pack(pady=10)

janela.mainloop()
