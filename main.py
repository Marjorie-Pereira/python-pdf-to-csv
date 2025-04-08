import pdfplumber
import csv
import zipfile
def retirarAbreviacoes(tupla):
    if(tupla.__contains__('OD')):
        od_index = tupla.index('OD')
        tupla.remove('OD')
        tupla.insert(od_index, 'Seg. Odontológica')
    if(tupla.__contains__('AMB')):  
        amb_index = tupla.index('AMB')
        tupla.remove('AMB')
        tupla.insert(amb_index, 'Seg. Ambulatorial')
        
def substituirCharEmString(char, tupla, novoChar=' '):
    for i in range(len(tupla)):
        if char in tupla[i]:
            tupla[i] = tupla[i].replace(char, novoChar)

dados_tabela = []
with pdfplumber.open('../teste/arquivosGov/anexos/anexoI.pdf') as pdf:
    pagina_inicio = pdf.pages[2]
    ultima_pagina = pdf.pages[-1]
    tabela_primeira_pagina = pagina_inicio.extract_table()
    cabecalho = tabela_primeira_pagina[0]
    retirarAbreviacoes(cabecalho)
    
    for page in range(pagina_inicio.page_number, ultima_pagina.page_number + 1):
        print(f'Extraindo dados da página {page}...')
        table_page = pdf.pages[page - 1]
        table = table_page.extract_table()
        table_data = table.copy()
        table_data.pop(0)
        
        for linha in table_data:
            retirarAbreviacoes(linha)
            substituirCharEmString('\u03b1', linha, 'α')
            substituirCharEmString('\u03b2', linha, 'β')
            dados_tabela.append(linha)

nome_arquivo = "tabela_estruturada.csv"
with open(nome_arquivo, 'w', encoding='utf-8-sig', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(cabecalho)
    csv_writer.writerows(dados_tabela)
print(f'Dados salvos em {nome_arquivo}')

with zipfile.ZipFile('Teste_Marjorie_Pereira.zip', 'w') as zip:
    zip.write('tabela_estruturada.csv')