# coding=utf8

"""
17-03-08 Francisco
- Adicionada uma nova coluna de TELEFONE nas preferencias dos professores.
- Leitura da carga horaria de turma do SAR
"""

"""
16-03-11 Francisco
- Modifiquei os valores de notas, de numericos para textuais
- Corrigi bugs
- Adicionei as observacoes
"""

"""
14-12-08 Francisco
- Adicionei a funcao ler_solucao_cbc
"""

"""
14-11-20 Francisco
- Adicionei a funcao ler_conf
- Consertei ler_solucao
- Consertei ler_sar (t.nomes estava errado)
"""

"""
14-11-11 Joao
*Acrescentei as funcoes caca_fantasmas e ler_solucoes
*Os blocos ler_grupos, ler_sar e ler_preferencias possuiam trechos de identação com espaços e outros com tabulações. Devido a diferenças entre editores isso pode ter ficado bagunçado. Padronizei para tabulações, mas existe uma pequena chance de ter desalinhado alguma coisa. Devemos prestar atenç~ao para manter o padr~ao em futuras ediçoes
*Alterei a funcao pre_atribuidas para não atribuir fantasmas

14-11-07 Francisco
Consertei varios erros associados a leitura das preferencias, a saber
 - Buracos no preenchimento detalhado e resumido
 - Problema com o caso "sem impedimento"
Adicionada funcao para ler disciplinas pre-atribuidas
"""

import numpy
import classes
import funcoes_gerais
import re

####################################################################################################################
####################                  Funcao              caca_fantasmas                   #########################
####################################################################################################################
#Remove os fantasmas da lista turmas
def caca_fantasmas(arquivo,turmas):
	with open(arquivo,"r") as fonte:

                print("\nRemovendo disciplinas fantasmas")
                print("-------------------------------\n")

		for (num_linha, linha) in enumerate(fonte, 1):
			fantasma=linha.split('\t')
			fantasma_inexistente=True
			i=0

			while(i<len(turmas)):
				if int(turmas[i].codigo) == int(fantasma[0]) and \
                                   int(turmas[i].turma)  == int(fantasma[1]) :
                                        print("Turma " + turmas[i].id() + " removida")
					del turmas[i]
					fantasma_inexistente = False
				else:
					i += 1
			if fantasma_inexistente:
				print("\nAVISO: Linha " + str(num_linha) + \
                                      " - Este fantasma nao existe:" + \
                                      fantasma[0] + "_" + fantasma[1] + ".\n")
	return turmas
####################################################################################################################
####################    Funcao                 ler_solucao              e auxiliares      #########################
####################################################################################################################
def ler_solucao(professores,turmas,arquivo):
	with open(arquivo,"r") as fonte:
		for linha in fonte:

                        # Pula as linhas que nao setam variaveis
                        if not '(' in linha: continue

			a=re.split("[()]", linha)

			b=a[1].split(',')
			professor=b[0]
			variavel=a[0]

                        if variavel == 'carga_horaria':
				for p in professores :
					if p.nome() == professor:
						p.carga_horaria=float(linha.split()[-1])
			elif variavel=="x":
                                turmaid = b[1].strip('\'')
				if float(a[-1].strip()) > 0.9:
                                        for t in turmas:
                                                if t.id() == turmaid:
                                                        break
                                        for p in professores:
                                                if p.nome()==professor:
                                                        p.turmas_a_lecionar.append(t)
                                                        break
			elif variavel=="insat":
				for p in professores :
					if p.nome() == professor:
						p.insatisfacao=float(linha.split()[-1])
			elif variavel=="insat_disciplinas":
				for p in professores:
					if p.nome() == professor :
						p.insat_disciplinas=float(linha.split()[-1])
			elif variavel=="insat_cargahor":
				for p in professores:
					if p.nome() == professor :
						p.insat_cargahor=float(linha.split()[-1])
			elif variavel=="insat_numdisc":
				for p in professores:
					if p.nome() == professor :
						p.insat_numdisc=float(linha.split()[-1])
			elif variavel=="insat_horario":
				for p in professores:
					if p.nome() == professor :
						p.insat_horario=float(linha.split()[-1])
			elif variavel=="insat_distintas":
				for p in professores:
					if p.nome() == professor :
						p.insat_distintas=float(linha.split()[-1])
			elif variavel=="insat_manha_noite":
				for p in professores:
					if p.nome() == professor :
						p.insat_manha_noite=float(linha.split()[-1])
			elif variavel=="insat_janelas":
				for p in professores:
					if p.nome() == professor :
						p.insat_janelas=float(linha.split()[-1])

####################################################################################################################
####################    Funcao                 ler_solucao_cbc          e auxiliares      #########################
####################################################################################################################
def ler_solucao_cbc(professores,turmas,arquivo):
	with open(arquivo,"r") as fonte:
		for linha in fonte:

                        # Pula as linhas que nao setam variaveis
                        if not '(' in linha: continue

			a=re.split("[()]", linha.split()[1])
			b=a[1].split(',')

			professor=b[0]
			variavel=a[0]

                        if variavel == 'carga_horaria':
				for p in professores :
					if p.nome() == professor:
						p.carga_horaria=float(linha.split()[-2])
			elif variavel=="x":
                                turmaid = b[1].strip('\'')
				if linha.split()[-2] == "1":
                                        for t in turmas:
                                                if t.id() == turmaid:
                                                        break
                                        for p in professores:
                                                if p.nome()==professor:
                                                        p.turmas_a_lecionar.append(t)
                                                        break
			elif variavel=="insat":
				for p in professores :
					if p.nome() == professor:
						p.insatisfacao=float(linha.split()[-2])
			elif variavel=="insat_disciplinas":
				for p in professores:
					if p.nome() == professor :
						p.insat_disciplinas=float(linha.split()[-2])
			elif variavel=="insat_cargahor":
				for p in professores:
					if p.nome() == professor :
						p.insat_cargahor=float(linha.split()[-2])
			elif variavel=="insat_numdisc":
				for p in professores:
					if p.nome() == professor :
						p.insat_numdisc=float(linha.split()[-2])
			elif variavel=="insat_horario":
				for p in professores:
					if p.nome() == professor :
						p.insat_horario=float(linha.split()[-2])
			elif variavel=="insat_distintas":
				for p in professores:
					if p.nome() == professor :
						p.insat_distintas=float(linha.split()[-2])
			elif variavel=="insat_manha_noite":
				for p in professores:
					if p.nome() == professor :
						p.insat_manha_noite=float(linha.split()[-2])
			elif variavel=="insat_janelas":
				for p in professores:
					if p.nome() == professor :
						p.insat_janelas=float(linha.split()[-2])

####################################################################################################################
####################    Funcao                 ler_grupos                e auxiliares      #########################
####################################################################################################################
def ler_grupos(arquivo): #Le os grupos do arquivo de grupos
	grupos = []
	with open(arquivo,"r") as fonte:
		for linha in fonte:
			if not linha.isspace():
				tok=linha.split()
				g=classes.Grupo()
				g.id = funcoes_gerais.uniformize(tok[1])
				if tok[0]=="C":
					g.canonico=True
				for i in tok[2:]:
					g.disciplinas.append(i)
				grupos.append(g)
	return grupos
####################################################################################################################
####################    Funcao                 ler_sar                   e auxiliares      #########################
####################################################################################################################
def sar_vale(linha): #Define se a linha lida do SAR possui informacoes relevantes
	if len(linha) < 10:
		 return False
	tok=linha.split()
	if len(tok)<10:
		return False
	if tok[0]=='DISC':
		 return False
	if tok[len(tok)-9] == 'MARINGA':
		 return True
#----------------------------------------------------------------------------------------------------------------------
def sar_primaria(linha): #Uma linha primaria e aquela que comeca uma nova turma, essa funcao as identifica
	if not sar_vale(linha):
		return False
	tok=linha.split()
	if len(tok[0])>2:
		return True
	return False
#----------------------------------------------------------------------------------------------------------------------      
def copia_turmas(origem):
	destino = classes.Turma()
	destino.codigo = origem.codigo
	destino.turma = origem.turma
	destino.nome = origem.nome
	destino.semestralidade = origem.semestralidade
	destino.horarios = list(origem.horarios) # Cria uma copia por valor
	destino.grupo = origem.grupo
	destino.professor = origem.professor
	destino.vinculada = origem.vinculada
        destino.ch = origem.ch
	return destino
#----------------------------------------------------------------------------------------------------------------------
def ler_sar(arquivo,grupos): #arquivo: arquivo do SAR, grupos: lista dos objetos grupos
	turmas = []
	anual=False
	with open(arquivo, "r") as fonte:
		for linha in fonte:
			tok=linha.split()
			if sar_primaria(linha):
				if anual: #se a ultima disciplina lida foi anual, sua correspondente no segundo semestre sera criada
					t = copia_turmas(turmas[-1])
					t.semestralidade = 2
					temp = str(t.codigo) + "_S2"
					for g in grupos:
						if temp in g.disciplinas:
							t.grupo=g
							break
					turmas.append(t)
				anual=False
				semestres=[]
				t=classes.Turma()
				turmas.append(t)
				t.codigo=tok[0]
				t.turma=tok[1]
				if tok[-4]=="A":
					t.semestralidade=1
					anual=True
					t.vinculada=True
				else:
					anual=False
					if tok[-4]=="S1":
						t.semestralidade=1
					else:
						t.semestralidade=2
				t.horarios.append((int(tok[-12]),int(tok[-11])))		
				t.nome=""
				for i in tok[2:-12]:
					t.nome=t.nome+" "+i
				temp=str(t.codigo)
				if anual:
					temp += "_S"+str(t.semestralidade)
				for g in grupos:
					if temp in g.disciplinas:
						t.grupo=g
						break
                                # Para a carga horaria, precisamos remover a virgula
                                t.ch = int(tok[-6].split(',')[0])
			else:
				if sar_vale(linha):
					turmas[-1].horarios.append((int(tok[0]),int(tok[1])))
		#fim do loop grande
		if anual: #se a ultima disciplina (de todas) lida foi anual, sua correspondente no segundo semestre sera criada
			t=classes.Turma()
			copia_turmas(turmas[len(turmas)],t)
			t.semestralidade=2
			temp=str(t.codigo)+"_S2"
			for g in grupos:
				if temp in g.disciplinas:
					t.grupo=g
					break
		return turmas
############################################################################################################################
#########################################                LER PREFERENCIAS                   ################################
############################################################################################################################
converter_horario = {'07:45 - 09:15':(1,2),   \
                    '09:30 - 12:10':(3,4,5),  \
                    '13:30 - 15:10':(6,7),    \
                    '15:30 - 18:00':(8,9,10), \
                    '19:30 - 21:10':(11,12),  \
                    '21:20 - 23:00':(13,14)}
#----------------------------------------------------------------------------------------------------------------------
converter_dia={'SEG':2, 'TER':3, 'QUA':4, 'QUI':5, 'SEX':6, 'SAB':7}
#----------------------------------------------------------------------------------------------------------------------
converter_codigo_de_horario= 	{1:(1,2),   \
				2:(3,4,5),  \
				3:(6,7),    \
				4:(8,9,10), \
				5:(11,12),  \
				6:(13,14)}
#----------------------------------------------------------------------------------------------------------------------
converter_periodo = {'MANHA' : (1,2,3,4,5),  \
                     'TARDE' : (6,7,8,9,10), \
                     'NOITE' : (11,12,13,14) }
#----------------------------------------------------------------------------------------------------------------------
converter_preferencia = { 'NAO GOSTARIA'          : 0,   \
                          'DESGOSTARIA LEVEMENTE' : 2.5, \
                          'INDIFERENTE'           : 5,   \
                          'GOSTARIA LEVEMENTE'    : 7.5, \
                          'GOSTARIA'              : 10   }
#----------------------------------------------------------------------------------------------------------------------
def ler_pref(form,grupos,max_impedimentos):
	professores = []
	with open(form, "r") as f:
		for l in f:
			p = classes.Professor()
			tokens = iter(l.split('\t'))
			tokens.next()# Pula timestamp
			p.nome_completo = funcoes_gerais.uniformize(tokens.next()) # Identificacao
			p.matricula = int(tokens.next()) # Identificacao Unica
                        # Jeito tosco de remover duplicatas
                        # TODO: melhorar isso
                        for i in professores:
                                if i.matricula == p.matricula:
                                        print 'AVISO: Professores ' + i.nome() + ' e ' + p.nome() + \
                                                ' com mesma matrícula. Eliminando entrada antiga.\n'
                                        professores.remove(i)
			p.email = tokens.next()
                        p.tel = tokens.next()
			chp1 = tokens.next()
			chp2 = tokens.next()
			if chp1=='':
				chp1='0'
			if chp2=='':
				chp2="0"
			p.chprevia1 = int(chp1)
			p.chprevia2 = int(chp2)                        
			p.discriminacao_chprevia = tokens.next()
			w = funcoes_gerais.uniformize(tokens.next())# Licença
			if "PRIMEIRO" in w:
				p.licenca1 = True
			if "SEGUNDO" in w:
				p.licenca2 = True
			if "ANUAL" in w:
				continue
			w = funcoes_gerais.uniformize(tokens.next())# Temporario
			if w == 'TEMPORARIO':
				p.temporario = True
			p.peso_disciplinas_bruto = float(tokens.next())
			p.peso_horario_bruto = float(tokens.next())
			p.peso_cargahor = float(tokens.next())
			p.peso_distintas = float(tokens.next())
			p.peso_numdisc = float(tokens.next())
			p.peso_manha_noite = float(tokens.next())
			p.peso_janelas_bruto = float(tokens.next())
			# Inaptidao em grupos
			w = funcoes_gerais.uniformize(tokens.next())
			if len(w) > 0:
				p.inapto = w.split(', ')
			# Preferencia por grupos
			for g in grupos:
				if g.canonico:
					s = tokens.next()
					if len(s) > 0:	#se a preferencia foi preenchida
						p.pref_grupos_bruto[g.id] = int(s)
					else: #se não, atribuir default 5
						p.pref_grupos_bruto[g.id] = 5
			# Reuniao departamento
			w = funcoes_gerais.uniformize(tokens.next())
			if 'SIM' in w:
						p.pref_reuniao = True
			# Preferencia compacto/esparso (define o respectivo peso como zero se nao especificado)
			w = funcoes_gerais.uniformize(tokens.next())
			p.peso_janelas=p.peso_janelas_bruto
			if 'ESPARSOS' in w:
				p.pref_janelas = True
			elif 'COMPACTOS' not in w:
				p.peso_janelas = 0 #Zera peso_janelas se a Preferencia nao for informada
			for i in range(0,max_impedimentos):
				dia = funcoes_gerais.uniformize(tokens.next())
				periodo = funcoes_gerais.uniformize(tokens.next())
				justificativa = funcoes_gerais.uniformize(tokens.next())
				#guarda os dados do impedimento como string para conferencia posterior
				p.lista_impedimentos.append(dia+", "+periodo+", "+justificativa)
				#se o dia e periodo foram corretamente preenchidos, marca a respectiva posicao na matriz como 1
				if len(dia) > 0 and not dia.isspace() and dia != "SEM IMPEDIMENTO" and \
					len(periodo) > 0 and not periodo.isspace() and periodo != "SEM IMPEDIMENTO": 
					for h in converter_periodo[periodo]:
						p.impedimentos[h,converter_dia[dia]]=1
			#Comeca o prechimento das tabelas de horario	
			w = funcoes_gerais.uniformize(tokens.next())
			m = numpy.zeros((15, 8))
			if 'DETALHADO' in w:
				for d in range(2,8):
					periodos = ['MANHA', 'TARDE', 'NOITE']
					if d == 7:
						periodos = ['MANHA', 'TARDE']
					for i in periodos:
						pref = funcoes_gerais.uniformize(tokens.next())
						for h in converter_periodo[i]:
							if len(pref) == 0:
								pref = 'INDIFERENTE'
							p.pref_horarios_bruto[h,d] = converter_preferencia[pref]
                                for i in range(0, 5): # Pula as posicoes em branco do formulario
                                        tokens.next()
			else:
				for i in range(0,3 * 5 + 2): #pula as posicoes em branco do formulario
					tokens.next()
				for i in ['MANHA', 'TARDE', 'NOITE']: #le as preferencias para os dias da semana
					pref = funcoes_gerais.uniformize(tokens.next())
					for h in converter_periodo[i]:
						for d in range(2,7): #grava uma copia em cada dia da semana
							if len(pref) == 0:
								pref = 'INDIFERENTE'
							p.pref_horarios_bruto[h,d] = converter_preferencia[pref]
				for i in ['MANHA', 'TARDE']: #lendo as preferencias do sabado
					pref = funcoes_gerais.uniformize(tokens.next())
					for h in converter_periodo[i]:
						if len(pref) == 0:
							pref = 'INDIFERENTE'
                                                p.pref_horarios_bruto[h,d + 1] = converter_preferencia[pref]
                        # Professor tem reducao de carga para a pos?
                        p.pos = tokens.next() == 'S'
                        # Tudo o que vier depois daqui eh considerado comentario.
                        for obs in tokens:
                                p.observacoes += obs
                                
			professores.append(p)
	return professores


############################################################################################################################
#########################################                LER PRE-ATRIBUIDAS                 ################################
############################################################################################################################
def ler_pre_atribuidas(arquivo, arquivo_de_fantasmas, professores, turmas):

        """
        Devolve uma lista de pares (professor,turma) pre atribuidos
        """

        print("\nCarregando pre-atribuidas")
        print("---------------------------\n")

        fantasma = []

        with open(arquivo_de_fantasmas, "r") as fant:

                for linha in fant:

                        tok = linha.split("\t")

                        fantasma.append((tok[0], tok[1]))

        with open(arquivo, "r") as f:

                linha = 1

                pre_atribuidas = []

                for l in f:

                        if len(l) < 0 or l.isspace():
                                continue

                        tokens = iter(l.split("\t"))

                        try:

                                matricula = int(tokens.next())

                                nome_professor = tokens.next()

                                cod_disciplina = tokens.next()

                                turma = tokens.next()

                                nome_disciplina = tokens.next().rstrip()

                        except Exception:

                                s = 'AVISO: Ignorando linha ' + str(linha) + \
                                    ' em PRE-ATRIBUIDAS.'

                                print(s)

                                linha += 1

                                continue

                        for p in professores:
                                if p.matricula == matricula:
                                        encontrada = False
                                        for t in turmas:
                                                # Nao precisa se preocupar com a semestralidade, pois
                                                # o codigo e a turma vao bater duas vezes, em caso de
                                                # disciplina anual
                                                if t.codigo == cod_disciplina and \
                                                   t.turma == turma:
                                                        encontrada = True
                                                        if not (cod_disciplina, turma) in fantasma:       
                                                               pre_atribuidas.append((p, t))
                                        if not encontrada:
                                            if not (cod_disciplina, turma) in fantasma:
                                                s = "AVISO: Disciplina " + cod_disciplina + \
                                                    " turma " + turma + " (" + nome_disciplina + \
                                                    ") nao encontrada."
                                                print(s)
                                        break
                        else:
                                s = "AVISO: Linha " + str(linha) + ": matricula " + str(matricula) + " "
                                s += "(professor " + nome_professor +")" + " nao encontrada!"
                                print(s)

                        linha += 1

        return pre_atribuidas

############################################################################################################################
#########################################                LER AQUIVO DE CONFIGURACAO         ################################
############################################################################################################################

def ler_conf(arquivo):
        """
        Le o arquivo de configuracao e devolve um mapa {PARAMETRO:VALOR}com os parametros lidos
        """

        param = {}
        linha = 1
        
        with open(arquivo,'r') as f:
                for l in f:
                        if l.isspace() or l.startswith("#"):
                                continue

                        tokens = l.split()

                        if len(tokens) == 2:
                                param[tokens[0]] = tokens[1]
                        else:
                                print("\nLER_CONF.PY Erro na linha " + str(linha) + "\n")

                        linha += 1

        return param