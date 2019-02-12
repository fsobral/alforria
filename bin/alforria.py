#!/usr/bin/python
#coding=utf8

"""
14-08-08 Francisco
Criacao de todo o arquivo alforria.dat (chamara alforria.aut.dat para evitar aborrecimentos)
"""

import unidecode
import funcoes_leitura

TEMPORARIO = 'TEMPORARIO'
COMPACTO = 'COMPACTO'
ESPARSO = 'ESPARSO'
SIM = 'SIM'

def uniformize(s,encode='utf8'):
    return unidecode.unidecode(s.decode(encode)).upper()

CONVERT_DAY = {'SEG':2, 'TER':3, 'QUA':4, 'QUI':5, 'SEX':6, 'SAB':7}
CONVERT_TIME = {'07:45 - 09:15':(1,2),        \
                    '09:30 - 12:10':(3,4,5),  \
                    '13:30 - 15:10':(6,7),    \
                    '15:30 - 18:00':(8,9,10), \
                    '19:30 - 21:10':(11,12),  \
                    '21:20 - 23:00':(13,14)}
CONVERT_POS = {1:(1,2),        \
               2:(3,4,5),  \
               3:(6,7),    \
               4:(8,9,10), \
               5:(11,12),  \
               6:(13,14)}

GRUPOSPATH = "../dados/grupos.txt"
PREFPATH = "../dados/preferencias.tsv"
SARPATH = "../dados/ensalamento.txt"

grupos = funcoes_leitura.ler_grupos(GRUPOSPATH)
preferencias = funcoes_leitura.ler_pref(PREFPATH,grupos,5)
turmas = funcoes_leitura.ler_sar(SARPATH,grupos)

for p in preferencias:
    p.ajustar()

with open("alforria.aut.dat","w") as f:

    f.write("set G := ")
    for g in grupos:
        f.write(g.id + " ")
    f.write(";\n\n")

    f.write("set G_CANONICOS := ")
    for g in grupos:
        if g.canonico:
            f.write(g.id + " ")
    f.write(";\n\n")

    f.write("set T := ")
    for t in turmas:
        f.write(t.id() + " ")
    f.write(";\n\n")

    f.write("set P := ")
    for p in preferencias:
        f.write(p.id() + " ")
    f.write(";\n\n")

    f.write("param turma_grupo := \n")
    for t in turmas:
        f.write(t.id() + " " + t.grupo + " 1\n")
    f.write(";\n\n")

    # Supoe que se uma disciplina eh vinculada, seu vinculo eh a
    # disciplina seguinte
    f.write("param vinculadas := \n")
    vinc = False
    for t in turmas:
        if vinc:
            f.write(t.id() + " 1\n")
            vinc = False
        elif t.vinculada:
            f.write(t.id() + " ")
            vinc = True
    f.write(";\n\n")

    f.write("param c := \n")
    for t in turmas:
        for (d,h) in t.horarios:
            f.write(t.id() + " " + str(t.semestralidade) + " " + str(d) + " " + str(h) + " 1\n")
    f.write(";\n\n")

    f.write("param temporario := \n")
    for p in preferencias:
        if p.temporario:
            f.write(p.id() + " 1\n")
    f.write(";\n\n")

    f.write("param inapto := \n")
    for p in preferencias:
        for g in p.inapto:
            f.write(p.id() + " " + g + " 1\n")
    f.write(";\n\n")

    f.write("param impedimento := \n")
    for p in preferencias:
        for d in range(2,8):
            for h in range(1,15):
                if p.impedimentos[h][d]:
                    for s in range (1,3):
                        f.write(p.id() + " " + str(s) + " " + str(d) + " " + str(h) + " 1\n")
        if p.pref_reuniao:
            for h in range(1,6):
                if not p.impedimentos[h][3]:
                    for s in range (1,3):
                        f.write(p.id() + " " + str(s) + " 3 " + str(h) + " 1\n")
    f.write(";\n\n")

    f.write("param pref_grupo := \n")
    for p in preferencias:
        for g in p.pref_grupos.keys():
            f.write(p.id() + " " + g + " " + str(p.pref_grupos[g]) + "\n")
    f.write(";\n\n")

    ## Falta colocar as preferencias!
