# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:36:15 2020

@author: rezen
"""
#%% BIBLIOTECAS UTILIZADAS

import pandas as pd #manipulação de séries

import re #expressões regulares

#%%MÓDULO DE LEITURA

def leitura(arq_fon, arq_pal):
    consoantes = "b c ç d f g j k l m n p q r s t v w x z"
    vogais = "a e i o u y á ã â à é ê í ó õ ô ú"
    
    palavras = []
    divisao_silabica = []
    canonicidade = []
    
    #leitura das palavras e verificação da canonicidade
    for linha in arq_pal:
        palavra = linha.replace("-", "")
        palavra = palavra.replace("\n", "")
        
        palavras.append(palavra)
        
        silabas = linha.replace("\n", "")
        
        divisao_silabica.append(silabas)
        
        letras = list(palavra)
        
        if len(letras) % 2 == 0:
            canonicidade.append(verificaCanonicidade(letras, 1, "C", consoantes, vogais))
        else:
            canonicidade.append("Não canônica")
    
        

    tonicidade = []
    
    #leitura dos fonemas e classificação da tonicidade
    for linha in arq_fon:
        fonetica = linha.replace("\n", "")
        fonetica = fonetica.split(".")
        
        num_silabas = len(fonetica)
        for silaba in fonetica:
            if re.search("ˈ", silaba):
                break
                    
            num_silabas-=1
            
        if num_silabas == 1:
            tonicidade.append("Oxítona")
        elif num_silabas == 2:
            tonicidade.append("Paroxítona")
        elif num_silabas == 3:
            tonicidade.append("Proparoxítona")
        else:
            tonicidade.append("s/n")
    
    #organização dos dados e suas características relevantes para análise
    tab = {"Palavra" : palavras, "Divisão silábica" : divisao_silabica , "Canonicidade" : canonicidade, "Tonicidade" : tonicidade}
    
    data_frame = pd.DataFrame(tab)
    data_frame.index = ["%s" % i for i in data_frame.index + 1]
    
    arq_fon.close()
    arq_pal.close()
    
    return data_frame

#verificação da canonicidade
def verificaCanonicidade(letras, i, tipo, consoantes, vogais):
    if re.search(letras[0], vogais):
        return "Não canônica"
    else:
        if len(letras) == i:
            return "Canônica"
        else:
            if tipo == "C" and re.search(letras[i], vogais):
                return verificaCanonicidade(letras, i+1, "V", consoantes, vogais)
            elif tipo == "V" and re.search(letras[i], consoantes):
                return verificaCanonicidade(letras, i+1, "C", consoantes, vogais)
            else:
                return "Não canônica"

#%% MÓDULO DE INTERFACE

print("CRIANDO PSEUDO-PALAVRAS - VERSÃO ALPHA")

sucesso = True

try:
    arq_fon = open("dic_data_fonetica.txt", encoding = "utf-8")
    arq_pal = open("dic_data_palavra.txt", encoding = "utf-8")
except:
    print("Arquivo(s) não encontrado(s)")
    
    sucesso = False
    
if sucesso:
    data_frame = leitura(arq_fon, arq_pal)
    
    teste = True
    while teste:
        canonicidade = input("INFORME A CANONICIDADE - (1) CANÔNICA (2) NÃO CANÔNICA: ")
    
        if canonicidade != "1" and canonicidade != "2":
            print("Digite 1 ou 2.")
        else:
            teste = False
            
    print()
    
    teste = True
    while teste:
        tonicidade = input("INFORME A TONICIDADE - (1) OXÍTONA (2) PAROXÍTONA (3) PROPAROXÍTONA: ")
    
        if tonicidade != "1" and tonicidade != "2" and tonicidade != "3":
            print("Digite 1, 2 ou 3.")
        else:
            teste = False
            
    print()
            
    if canonicidade == "1":
        canonicidade = "Canônica"
    else:
        canonicidade = "Não canônica"
        
    if tonicidade == "1":
        tonicidade = "Oxítona"
    elif tonicidade == "2":
        tonicidade = "Paroxítona"
    else:
        tonicidade = "Proparoxítona"
        
    palavras_buscadas = []
        
    for i in data_frame.itertuples():
        if i.Canonicidade == canonicidade and i.Tonicidade == tonicidade:
            palavras_buscadas.append(i.Palavra)
            
    tab = {"Palavras buscadas" : palavras_buscadas}
    
    df_palavras_buscadas = pd.DataFrame(tab)
    df_palavras_buscadas.index = ["%s" % i for i in df_palavras_buscadas.index + 1]
    
    print(df_palavras_buscadas)