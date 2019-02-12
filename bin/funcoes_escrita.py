import os
import funcoes_leitura as leitura

def cria_relatorio(professor,diretorio):
    """
    Recebe um professor e cria um arquivo .tex com o seu relatorio.
    """

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    with open("../config/base.tex","r") as padrao:
        with open(diretorio + 'relatorio.tex','w') as saida:
            professor.totex(diretorio + 'professor.tex')
            for l in padrao:
                saida.write(l)
            saida.write('\\include{professor}')
            saida.write('\\end{document}')

def cria_relatorio_geral(professores,diretorio):
    """
    Recebe uma lista de objetos do tipo Professor e constroi um arquivo .tex
    com todos os relatorios. Utiliza um arquivo chamado 'base.tex' como base
    para carregar os pacotes e similares.
    """

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    count = 1
    with open("../config/base.tex","r") as padrao:
        with open(diretorio + 'relatorio_geral.tex','w') as saida:
            for l in padrao:
                saida.write(l)
            for p in professores:
                p.totex(diretorio + str(count) + '.tex')
                saida.write('\\include{' + str(count) + '}\n')
                count += 1
            saida.write('\\end{document}')


####################################################################################################################
####################                  Funcao              escreve dat                      #########################
####################################################################################################################

def escreve_dat(professores,turmas,grupos,pre_atribuidas,arquivo):
	with open(arquivo,"w") as f:
                constantes = leitura.ler_conf('../config/constantes.cnf')

                for param in constantes:
                    f.write("param " + param + " := " + constantes[param] + ";\n\n")

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

		f.write("set T_PRE := ")
		for (p,t) in pre_atribuidas:
			f.write(t.id()+" ")
		f.write(";\n\n")		

		f.write("set P := ")
		for p in professores:
			f.write(p.id() + " ")
		f.write(";\n\n")

		#Vincula as turmas ao grupos
		f.write("param turma_grupo := \n")
		for t in turmas:
			if t.grupo is not None:
				f.write(t.id() + " " + t.grupo.id + " 1\n")
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

                f.write("param ch := \n")
                for t in turmas:
                    f.write(t.id() + " " + str(t.carga_horaria()) + "\n")
                f.write(";\n\n")

                f.write("param ch1 := \n")
                for t in turmas:
                    f.write(t.id() + " ")
                    if t.semestralidade == 1:
                        f.write(str(t.carga_horaria()) + "\n")
                    else:
                        f.write("0\n")
                f.write(";\n\n")

                f.write("param ch2 := \n")
                for t in turmas:
                    f.write(t.id() + " ")
                    if t.semestralidade == 2:
                        f.write(str(t.carga_horaria()) + "\n")
                    else:
                        f.write("0\n")
                f.write(";\n\n")

		f.write("param temporario := \n")
		for p in professores:
			if p.temporario:
				f.write(p.id() + " 1\n")
		f.write(";\n\n")

		f.write("param inapto := \n")
		for p in professores:
			for g in p.inapto:
				f.write(p.id() + " " + g + " 1\n")
		f.write(";\n\n")

		f.write("param impedimento := \n")
		for p in professores:
			for d in range(2,8):
				for h in range(1,15):
					if p.impedimentos[h][d]:
						for s in range (1,3):
							f.write(p.id() + " " + str(s) + " " + str(d) + " " + str(h) + " 1\n")
		f.write(";\n\n")

                f.write("param pref_janelas := \n")
                for p in professores:
                    if p.pref_janelas:
                        f.write(p.id() + " 1\n")
                f.write(";\n\n")

		f.write("param pref_grupo := \n")
		for p in professores:
			for g in p.pref_grupos.keys():
				f.write(p.id() + " " + g + " " + str(p.pref_grupos[g]) + "\n")
		f.write(";\n\n")
		
		f.write("param pref_hor := \n")
		for p in professores:
			for d in range(2,8):
				for h in range(1,15):
					f.write(p.id() + " " + str(d) + " " + str(h) + " " + str(p.pref_horarios[h,d]) + "\n")
		f.write(";\n\n")
		
		f.write("param pre_atribuida :=\n")
		for (p,t) in pre_atribuidas:
			f.write(p.id() + " " + t.id() + " 1\n")
		f.write(";\n\n")
		
		f.write("param chprevia1 :=\n")
		for p in professores:
			if p.chprevia1 > 0:
				f.write(p.id() + " " + str(p.chprevia1) + "\n")
		f.write(";\n\n")
		
		f.write("param chprevia2 :=\n")
		for p in professores:
			if p.chprevia2 > 0:
				f.write(p.id() + " " + str(p.chprevia2) + "\n")
		f.write(";\n\n")
		
		f.write("param licenca :=\n")
		for p in professores:
			if p.licenca1:
				f.write(p.id() + " 1 1\n")
			if p.licenca2:
				f.write(p.id() + " 2 1\n")
		f.write(";\n\n")
		
		f.write("param peso_disciplinas := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_disciplinas) + "\n")
		f.write(";\n\n")
		
		f.write("param peso_horario := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_horario) + "\n")
		f.write(";\n\n")

		f.write("param peso_cargahor := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_cargahor) + "\n")
		f.write(";\n\n")

		f.write("param peso_distintas := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_distintas) + "\n")
		f.write(";\n\n")

		f.write("param peso_janelas := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_janelas) + "\n")
		f.write(";\n\n")

		f.write("param peso_numdisc := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_numdisc) + "\n")
		f.write(";\n\n")

		f.write("param peso_manha_noite := \n")
		for p in professores:
			f.write(p.id() + " " + str(p.peso_manha_noite) + "\n")
		f.write(";\n\n")
		
		f.write("param chmax := \n")
		for p in professores:
			if p.chmax != None:
				f.write(p.id() + " " + str(p.chmax) + "\n")
		f.write(";\n\n")
		
		f.write("param chmax1 := \n")
		for p in professores:
			if p.chmax1 != None:
				f.write(p.id() + " " + str(p.chmax1) + "\n")
		f.write(";\n\n")
		
		f.write("param chmax2 := \n")
		for p in professores:
			if p.chmax2 != None:
				f.write(p.id() + " " + str(p.chmax2) + "\n")
		f.write(";\n\nend;\n")		

####################################################################################################################
####################                  Funcao              escreve atribuicoes              #########################
####################################################################################################################

def escreve_atribuicoes(professores, turmas, arquivo):
	with open(arquivo,"w") as f:
                for p in professores:
                    for t in p.turmas_a_lecionar:
                        # TODO: trocar p.matricula por p.id()
                        f.write(str(p.matricula) + '\t' + p.nome() + '\t' + str(t.codigo) + '\t' + \
                                str(t.turma) + '\t' + t.nome + '\n')
                        # TODO: trocar p.matricula por p.id()
                        for fant in t.turmas_clientes:
                            f.write(str(p.matricula) + '\t' + p.nome() + '\t' + str(fant.codigo) + '\t' + \
                                    str(fant.turma) + '\t' + fant.nome + '\n')


####################################################################################################################
####################                  Funcao              escreve disciplinas              #########################
####################################################################################################################

def escreve_disciplinas(professores, turmas, arquivo):
    with open(arquivo,"w") as f:
        for t in turmas:
            f.write(t.nome + '\t' + str(t.codigo) + '\t' + str(t.turma) + '\t')
            for p in professores:
                if t in p.turmas_a_lecionar:
                    f.write(p.nome())
            f.write('\t' + 'S' + str(t.semestralidade))
            f.write('\n')

            for fant in t.turmas_clientes:
                f.write(fant.nome + '\t' + str(fant.codigo) + '\t' + str(fant.turma) + '\t')
                for p in professores:
                    if t in p.turmas_a_lecionar:
                        f.write(p.nome())
                f.write('\t' + 'S' + str(t.semestralidade))
                f.write('\n')



####################################################################################################################
####################                  Funcao              atualiza dat2                    #########################
####################################################################################################################

def atualiza_dat2(professores,arquivo):
    """
    Esta funcao serve para remover professores e preparar para
    uma nova rodada. A ser incluida na nova versao do alforria
    """

    listap = []

    # Leitura dos professores ja excluidos

    with open(arquivo,'r') as f:
        l = f.readline().split()

        if len(l) > 3:
            for nome in l[3:]:
                for p in professores:
                    if p.nome() == nome:
                        listap.append(p)

    professores.sort(key=lambda x: x.insatisfacao,reverse=True)

    # Procura o proximo insatisfeito que nao foi excluido

    i = 0
    while (i < len(professores)) and (professores[i] in listap):
        i = i + 1

    maxinsat = - 100
    if i < len(professores):
        maxinsat = professores[i].insatisfacao
        listap.append(professores[i])

    # Gera o novo arquivo

    print "Professores retirados da funcao objetivo:"
    for p in listap:
        print "\t{0:50s} insat: {1:10.7f}".format(p.nome(), p.insatisfacao)

    with open(arquivo,'w') as f:

        f.write('set P_OUT :=')
        for p in listap:
            f.write(' ' + p.nome())
        f.write(' ;\n\n')

        f.write('param ub_insat :=\n')
        for p in listap:
            f.write(p.nome() + ' ' + str(max(maxinsat, p.insatisfacao)) + '\n')
        f.write(';\n\n')

    # Antes de sair, ordena os professores por nome
    professores.sort(key=lambda x: x.nome())
