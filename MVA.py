@@ -39,14 +39,121 @@ def criar_novo_registro(mes):
        json.dump({}, file)

def exibir_informacoes(mes, informacoes):

    global planilha
    global janela_atual
    global arquivo_mes

    arquivo_mes = f"{mes}.json"

    def editar_dados():
        # Esta função será chamada quando o usuário escolher "Editar Dados" na janela de contexto.
        selected_item = planilha.selection()
        if selected_item:
            # Obtém os valores da linha selecionada
            selected_values = planilha.item(selected_item, 'values')
            nf, fornecedor, data, destinatario = selected_values

            # Cria uma nova janela para editar os dados
            editar_janela = tk.Toplevel(janela_atual)
            editar_janela.title(f"Editar Dados da NF: {nf}")

            # Crie e configure os campos para edição
            nf_label = ttk.Label(editar_janela, text="Nota Fiscal:")
            nf_label.pack(pady=5)

            nf_entry = ttk.Entry(editar_janela)
            nf_entry.insert(0, nf)
            nf_entry.pack(pady=5)

            fornecedor_label = ttk.Label(editar_janela, text="Fornecedor:")
            fornecedor_label.pack(pady=5)

            fornecedor_entry = ttk.Entry(editar_janela)
            fornecedor_entry.insert(0, fornecedor)
            fornecedor_entry.pack(pady=5)

            data_label = ttk.Label(editar_janela, text="Data de Chegada (dd/mm/yyyy):")
            data_label.pack(pady=5)

            data_entry = ttk.Entry(editar_janela)
            data_entry.insert(0, data)
            data_entry.pack(pady=5)

            destinatario_label = ttk.Label(editar_janela, text="Destinatario:")
            destinatario_label.pack(pady=5)

            destinatario_combobox = ttk.Combobox(editar_janela, values=["MVA", "Eletronica Horizonte"], state="readonly")
            destinatario_combobox.set(destinatario)
            destinatario_combobox.pack(pady=5)

            # Função para salvar as edições
            def salvar_edicao():
                nova_nf = nf_entry.get()
                novo_fornecedor = fornecedor_entry.get()
                nova_data = data_entry.get()
                novo_destinatario = destinatario_combobox.get()

                if nova_nf and novo_fornecedor and nova_data and novo_destinatario:
                    try:
                        data_formatada = datetime.strptime(nova_data, "%d/%m/%Y").strftime("%d/%m/%Y")
                    except ValueError:
                        messagebox.showerror("Erro", "Formato de data inválido. Use dd/mm/yyyy.")
                        return
                    
                    if nova_nf != nf:
                        # Crie uma cópia do dicionário com a nova chave e exclua a chave antiga
                        informacoes[nova_nf] = informacoes.pop(nf)

                    # Atualize os dados no dicionário de informações
                    informacoes[nova_nf].update ({
                        "NF": nova_nf,
                        "Fornecedor": novo_fornecedor,
                        "Data de Chegada": data_formatada,
                        "Destinatario": novo_destinatario
                        
                    })

                    # Atualize a planilha
                    planilha.item(selected_item, values=(nova_nf, novo_fornecedor, data_formatada, novo_destinatario))

                    # Atualize o arquivo JSON
                    with open(arquivo_mes, "w", encoding="utf-8") as file:
                        json.dump(informacoes, file, ensure_ascii=False, indent=4)

                    editar_janela.destroy()
                else:
                    messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

            # Botão para salvar as edições
            salvar_button = ttk.Button(editar_janela, text="Salvar Edição", command=salvar_edicao)
            salvar_button.pack(pady=10)

        else:
            messagebox.showwarning("Aviso", "Selecione uma linha para editar.")

    def excluir_dados():
        # Esta função será chamada quando o usuário escolher "Excluir Dados" na janela de contexto.
        selected_item = planilha.selection()
        if selected_item:
            nf = planilha.item(selected_item, 'values')[0]

            # Exclua a entrada no dicionário de informações
            del informacoes[nf]

            # Atualize a planilha removendo a linha
            planilha.delete(selected_item)

            # Atualize o arquivo JSON
            with open(arquivo_mes, "w", encoding="utf-8") as file:
                json.dump(informacoes, file, ensure_ascii=False, indent=4)

        else:
            messagebox.showwarning("Aviso", "Selecione uma linha para excluir.")

    janela_atual = tk.Toplevel(janela)
    janela_atual.title(f"Informações de {mes}")
    janela_atual.geometry("600x400")
    centralizar_janela(janela_atual,600,400)
    centralizar_janela(janela_atual, 600, 400)

    planilha = ttk.Treeview(janela_atual, columns=("NF", "Fornecedor", "Data de Chegada", "Destinatario"))
    planilha.heading("NF", text="NF")
@ -55,18 +162,30 @@ def exibir_informacoes(mes, informacoes):
    planilha.heading("Destinatario", text="Destinatario")

    planilha.column("#0", width=0, stretch="NO")
    planilha.column("NF", width=120, stretch="NO")
    planilha.column("Fornecedor", width=120, stretch="NO")
    planilha.column("Data de Chegada", width=120, stretch="NO")
    planilha.column("Destinatario", width=120, stretch="NO")
    planilha.column("NF", width=120, stretch="NO", anchor="center")
    planilha.column("Fornecedor", width=120, stretch="NO", anchor="center")
    planilha.column("Data de Chegada", width=120, stretch="NO", anchor="center")
    planilha.column("Destinatario", width=120, stretch="NO", anchor="center")

    planilha.bind("<Button-1>", lambda e: "break")
    planilha.bind("<Double-1>", lambda e: mostrar_menu_contexto(e, editar_dados, excluir_dados))

    planilha.pack(padx=20, pady=20)

    adicionar_mercadoria_button = ttk.Button(janela_atual, text="Adicionar Mercadoria", command=adicionar_nova_mercadoria)
    adicionar_mercadoria_button.pack(pady=10)

    # Preencha a planilha com os dados do arquivo JSON
    planilha.delete(*planilha.get_children())  # Limpe a planilha para preenchê-la novamente
    for nf, dados in informacoes.items():
        planilha.insert("", "end", values=(nf, dados["Fornecedor"], dados["Data de Chegada"], dados["Destinatario"]))

# Função para mostrar um menu de contexto
def mostrar_menu_contexto(event, editar_func, excluir_func):
    menu = tk.Menu(janela_atual, tearoff=0)
    menu.add_command(label="Editar Dados", command=editar_func)
    menu.add_command(label="Excluir Dados", command=excluir_func)
    menu.post(event.x_root, event.y_root)

def adicionar_nova_mercadoria():
    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"
@ -100,18 +219,16 @@ def adicionar_nova_mercadoria():
    Destinatario_label = ttk.Label(nova_janela, text="Destinatario:")
    Destinatario_label.pack(pady=5)

    Destinatario_combobox = ttk.Combobox(nova_janela, values=["MVA", "Eletronica Horizonte"])
    Destinatario_combobox = ttk.Combobox(nova_janela, values=["MVA", "Eletronica Horizonte"], state="readonly")
    Destinatario_combobox.pack(pady=5)

    salvar_button = ttk.Button(nova_janela, text="Salvar", command=lambda: salvar_nova_mercadoria(nf_entry.get(), fornecedor_entry.get(), data_entry.get(), Destinatario_combobox.get()))

    salvar_button.pack(pady=10)

    # Após a janela de edição ser fechada, atualize a planilha
    nova_janela.protocol("WM_DELETE_WINDOW", lambda: atualizar_planilha())


def salvar_nova_mercadoria(nf, fornecedor, data, Destinatario):
    global arquivo_mes

    mes_escolhido = mes_var.get()
    arquivo_mes = f"{mes_escolhido}.json"

@ -137,31 +254,11 @@ def salvar_nova_mercadoria(nf, fornecedor, data, Destinatario):
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
@ -176,14 +273,26 @@ def deletar_dados():
        messagebox.showwarning("Aviso", f"O arquivo para o mês de {mes_escolhido} não existe.")

meses_informacoes = {
    "Janeiro": {"Descrição": "Este é o mês de Janeiro.", "Outras Informações": "Algumas informações adicionais."},
    "Fevereiro": {"Descrição": "Este é o mês de Fevereiro.", "Outras Informações": "Mais informações aqui."},
    "Janeiro": {},
    "Fevereiro": {},
    "Março": {},
    "Abril": {},
    "Maio": {},
    "Junho": {},
    "Julho": {},
    "Agosto": {},
    "Setembro": {},
    "Outubro": {},
    "Novembro": {},
    "Dezembro": {}
}

arquivo_mes = None
planilha = None

janela = tk.Tk()
janela.title("Checar Mercadorias")
centralizar_janela(janela,400,200)
centralizar_janela(janela, 400, 200)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))
@ -201,8 +310,8 @@ mes_var = tk.StringVar()
mes_var.set("Janeiro")
meses = list(meses_informacoes.keys())

mes_dropdown = ttk.Combobox(container, textvariable=mes_var, values=meses, state="readonly")
mes_dropdown.pack(side="left")
mes_dropdown = ttk.Combobox(container, textvariable=mes_var, values=meses, state="readonly", style="TCombobox")
mes_dropdown.pack(side="left", anchor="center", fill="both")

ok_button = ttk.Button(janela, text="OK", command=abrir_nova_janela)
ok_button.pack(pady=10)
@ -213,4 +322,4 @@ deletar_button.pack(pady=10)
fechar_button = ttk.Button(janela, text="Fechar", command=janela.quit)
fechar_button.pack(pady=10)

janela.mainloop()
janela.mainloop()
