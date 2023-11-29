import pandas as pd
import tkinter as tk
from tkinter import ttk

def on_button_click():
    # Obter os valores dos Entry
    coluna_selecionada = combo_colunas.get()
    valor_filtro = entry_valor_filtro.get()

    # Filtrar os dados com base na coluna e valor fornecidos
    resultados = df[df[coluna_selecionada].astype(str).str.contains(valor_filtro, case=False, na=False)]

    # Atualizar o Text Widget com os resultados
    text_resultados.delete(1.0, tk.END)  # Limpar o Text Widget
    text_resultados.insert(tk.END, resultados.head().to_string(index=False))

# Caminho do arquivo CSV
file_path = "C:/Users/PC/Desktop/Dados_near_earth_objects/near_earth_objects_28_11_2023_22_43_54.csv"

# Ler o arquivo CSV para um DataFrame
df = pd.read_csv(file_path)

# Criar a janela principal
root = tk.Tk()
root.title("Busca de Dados")

# Configurar o redimensionamento responsivo da janela principal
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

# Criar e organizar os widgets na janela
label_instrucao = tk.Label(root, text="Escolha uma coluna e digite um valor para filtrar:")
label_coluna = tk.Label(root, text="Coluna:")
options_colunas = [
    "ID do Objeto",
    "Nome do Objeto",
    "Diâmetro Mínimo Estimado em Km",
    "Diâmetro Máximo Estimado em Km",
    "Data de Aproximação Mais Próxima",
    "Distância Mínima Estimada de Aproximação em Km",
    "Velocidade Relativa à Terra em Km/h",
    "Potencialmente Perigoso"
]
combo_colunas = ttk.Combobox(root, values=options_colunas)
label_valor_filtro = tk.Label(root, text="Valor:")
entry_valor_filtro = ttk.Entry(root)
button_buscar = tk.Button(root, text="Buscar", command=on_button_click)
text_resultados = tk.Text(root, height=20, width=120)

label_instrucao.grid(row=0, column=0, columnspan=2, pady=10)
label_coluna.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
combo_colunas.grid(row=1, column=1, padx=5, pady=5)
label_valor_filtro.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
entry_valor_filtro.grid(row=2, column=1, padx=5, pady=5)
button_buscar.grid(row=3, column=0, columnspan=2, pady=10)
text_resultados.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

# Iniciar o loop de eventos da GUI
root.mainloop()
