#!/usr/bin/python3
#coding=utf8

import funcoes_leitura as leitura
import funcoes_escrita as escrita
import check

paths = leitura.ler_conf('../config/paths.cnf')

GRUPOSPATH = paths['GRUPOSPATH']
PREFPATH = paths['PREFPATH']
SARPATH = paths['SARPATH']
ATRIBPATH = paths['ATRIBPATH']
FANTPATH = paths['FANTPATH']
DAT2PATH = paths['DAT2PATH']
SOLPATH = paths['SOLPATH']

configuracoes = leitura.ler_conf('../config/alforria.cnf')

MAXIMPEDIMENTOS = int(configuracoes['MAXIMPEDIMENTOS'])
RELDIR = configuracoes['RELDIR']

grupos = leitura.ler_grupos(GRUPOSPATH)

professores = leitura.ler_pref(PREFPATH,grupos,MAXIMPEDIMENTOS)
for p in professores:
    p.ajustar()

turmas = leitura.ler_sar(SARPATH,grupos)

turmas = leitura.caca_fantasmas(FANTPATH,turmas)

leitura.ler_solucao(professores,turmas,SOLPATH)

pre_atribuidas = leitura.ler_pre_atribuidas(ATRIBPATH,FANTPATH,professores,turmas)

p_fantasmas = check.checkdata(professores,turmas,pre_atribuidas,FANTPATH)

professores.extend(p_fantasmas)

escrita.atualiza_dat2(professores,DAT2PATH)    

check.estatisticas(professores,turmas)

escrita.cria_relatorio_geral(professores,RELDIR)

escrita.escreve_disciplinas(professores, turmas, RELDIR + 'disciplinas.csv')

escrita.escreve_atribuicoes(professores, turmas, RELDIR + 'atribuicoes.csv')
