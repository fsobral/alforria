#!/usr/bin/python
#coding=utf8

import funcoes_leitura as leitura
import funcoes_escrita as escrita
import check
import argparse

parser = argparse.ArgumentParser(description = \
                                 'Compara dois SARs de anos distintos')
parser.add_argument('files', help = 'Caminho completo para cada um dos ' \
                    'SARs em formato txt', nargs = 2)

args = parser.parse_args()

# Le os caminhos onde se encontram os arquivos de dados

paths = leitura.ler_conf('../config/paths.cnf')

GRUPOSPATH = paths['GRUPOSPATH']
PREFPATH = paths['PREFPATH']
SARPATH = paths['SARPATH']
ATRIBPATH = paths['ATRIBPATH']
FANTPATH = paths['FANTPATH']
DATPATH = paths['DATPATH']
SOLPATH = paths['SOLPATH']

# Carrega o arquivo de configuracoes do programa. Nesse caso pega o
# numero maximo de impedimentos que estao no programa e o nome do
# diretorio de criacao dos relatorios.

configuracoes = leitura.ler_conf('../config/alforria.cnf')

MAXIMPEDIMENTOS = int(configuracoes['MAXIMPEDIMENTOS'])


# Carrega os grupos de disciplinas
grupos = leitura.ler_grupos(GRUPOSPATH)

# Carrega os professores e suas preferencias e ajusta os valores dados
# às preferências para que fiquem entre 0 e 10.
professores = leitura.ler_pref(PREFPATH,grupos,MAXIMPEDIMENTOS)
for p in professores:
    p.ajustar()

# Carrega as turmas de disciplinas do ano e elimina as disciplinas
# fantasmas (turmas com números diferentes que são, na verdade, a
# mesma turma)

turmas1 = leitura.ler_sar(args.files[0], [])

turmas2 = leitura.ler_sar(args.files[1], [])

for t1 in turmas1:
    existe = False
    for t2 in turmas2:
        if t1.id() == t2.id():
            existe = True
            if len( [(d,h) for (d,h) in t1.horarios \
                     if (d,h) not in t2.horarios] ) > 0 or \
                        t1.carga_horaria() != t2.carga_horaria():
                print(t1.id() + " " + t1.nome + \
                      " com horarios diferentes nos SARs.")
                print("\t" + str(t1))
                print("\t" + str(t2))

    if not existe:
        print(t1.id() + " " + t1.nome + " nao encontrada no segundo SAR.")
