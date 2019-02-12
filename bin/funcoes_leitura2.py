import classes
import funcoes_gerais

############################################################################################################################
#########################################                ler sar pos                        ################################
############################################################################################################################
def ler_sarpos(arquivo,turmas,professores):#Esta função tem que ser executada depois da remocao de duplicatas.
	with open(arquivo,"r") as fonte:
		for linha in fonte:
			tok=linha.split()
			if len(tok)>2:
				t=classes.Turma()
				t.codigo=tok[0]
				t.semestralidade=tok[1]
				t.nome=tok[2]
				t.pos=True
				t.carga_horaria_pos=tok[4]
				for p in professores:
					if funcoes_gerais.comparanomes(p.nome_completo,tok[4]):
						t.professor=p
						p.pre-atribuicoes.append(t)
						break

def ler_pre_atribuidas(arquivo,turmas,professores):#Esta função tem que ser executada depois da remocao de duplicatas.
	with open(arquivo,"r") as fonte:
		for linha in fonte:
			tok=linha.split()
			if len(tok)>2:
				professor=tok[0]
				codigo=tok[1]
				turma=tok[2]
				for t in turmas:
					if t.codigo==codigo and t.turma==turma:
						for p in professores:
							if funcoes_gerais.comparanomes(p.nome_completo,tok[4]):
							t.professor=p
							p.pre-atribuicoes.append(t)
							break

############################################################################################################################
#########################################               ler clientes                        ################################
############################################################################################################################
def ler_clientes(arquivo, turmas):
	with open(arquivo,"r") as fonte:
		for linha in fonte:
			if not linha.isspace()
				tok = linnha.split()
				temp=tok[1].split('-')
				codigo=temp[0] ####???? Eliminar lixo da string????
				turma=temp[1]
			if tok[0]=="servidor:"
				for servidor in turmas:
					if servidor.codigo==codigo and servidor.turma==turma
						break
			if tok[0]=="cliente:"
				for cliente in turmas:
					if cliente.codigo==codigo and cliente.turma==turma:
						cliente.eh_cliente=True
						servidor.clientes.append(cliente.codigo+"_"+cliente.turma+"_S"+cliente.semestralidade)