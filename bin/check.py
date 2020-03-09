#!/usr/bin/python
# coding=utf8

import funcoes_leitura
import funcoes_escrita
import logging


"""
17-03-21 Francisco
- Tratamento de professores da pós
"""

"""
16-01-28 Francisco
- Refatoracao
- Aumentamos a ch. maxima do professor quando ha estouro por pre-atribuicao
"""

def check_p(p):

        """This function checks if professor 'p' has a feasible set of
        attributed courses. Unlike the original 'check' function, it
        DOES NOT change any attribute of the professor.

        Returns True if OK or False otherwise.

        """

        logger = logging.getLogger('alforria')

        ok = True

        for t in p.turmas_a_lecionar:

                for (d, h) in t.horarios:

                        if p.impedimentos[d][h] == 1:

                                logger.error(
                                        "AVISO: Professor " + str(p.nome()) +
                                        " no dia e horario " + str((d, h)) +
                                        " com impedimento e disciplina " +
                                        "pre-atribuida " + str(t.id()) + "."
                                )

                                ok = False
                        
                if p.licenca1 and t.semestralidade == 1:
                        
                        logger.error("\tProfessor %s com disciplina %s pre-atribuida e " +
                                    "com licenca.", p.nome(), t.id())
                        
                        ok = False

                if p.licenca2 and t.semestralidade == 2:
                        
                        logger.error("\tProfessor %s com disciplina %s pre-atribuida e " +
                                    "com licenca.", p.nome(), t.id())
                        
                        ok = False

                if t.grupo is not None and t.grupo.id in p.inapto:

                        logger.info("\tProfessor %s inapto para grupo %s de" +
                                    "disciplina pre-atribuida %s.",
                                    p.nome(), t.grupo.id, t.id())

                        ok = False

        return ok


                

############################################################################################################################
#########################################                LER AQUIVO DE FANTASMAS            ################################
############################################################################################################################


def ler_fantasmas(arquivo):

        fantasmas = []
        with open(arquivo, "r") as fonte:

                for linha in fonte:

                        tok = linha.split()

                        fantasmas.append((int(tok[0]), int(tok[1])))

        return fantasmas

############################################################################################################################
#########################################        LIMPA E VERIFICA INCONSISTENCIAS           ################################
############################################################################################################################


def checkdata(professores, turmas, pre_atribuidas, FANTPATH):

        logger = logging.getLogger('alforria')

        constantes = funcoes_leitura.ler_conf('../config/constantes.cnf')

        fantasmas = ler_fantasmas(FANTPATH)

        # Verifica pre-atribuidas duplicadas
        # ----------------------------------

        logger.info("\n")
        logger.info("Checando pre-atribuidas duplicadas")
        logger.info("----------------------------------\n")

        check_duplicadas(pre_atribuidas)

        # Verifica impedimentos e etc
        # ---------------------------

        logger.info("\n")
        logger.info("Checando impedimentos e etc...")
        logger.info("------------------------------\n")

        p_ajustar = set()

        # Nao ha necessidade de remover impedimentos, pois o proprio
        # modelo ignora inconsistencias causadas por disciplinas
        # pre-atribuidas. Ou seja, uma pre-atribuida tem sempre
        # preferencia.
        for (p, t) in pre_atribuidas:

                for (d, h) in t.horarios:

                        if p.impedimentos[h][d] == 1:

                                logger.warning(
                                        "AVISO: Professor " + str(p.nome()) +
                                        " no dia e horario " + str((d, h)) +
                                        " com impedimento e disciplina " +
                                        "pre-atribuida " + str(t.id()) +
                                        ". O impedimento NÃO será removido.\n"
                                )

                                # p.impedimentos[h][d]=0

                                # Eh necessario reajustar os limites
                                # quando removemos o impedimento
                                # p_ajustar.add(p)

        for p in p_ajustar:

                p.ajustar()

        i = 0

        while (i < len(pre_atribuidas) - 1):

                pi = pre_atribuidas[i][0]
                ti = pre_atribuidas[i][1]
                j = i+1

                while (j < len(pre_atribuidas)):

                        conflito = False
                        pj = pre_atribuidas[j][0]
                        tj = pre_atribuidas[j][1]

                        if pi == pj and ti != tj and \
                           int(ti.semestralidade) == int(tj.semestralidade):

                                for x in ti.horarios:

                                        if x in tj.horarios:

                                                conflito = True

                                                break
                        if conflito:

                                logger.warning(
                                        "AVISO: Professor " + pi.nome() +
                                        " com 2 disciplinas pre-atribuidas conflitantes: " +
                                        str(ti.id()) + " e " + str(tj.id()) + ".")

                                iguais = True

                                for x in ti.horarios:
                                        if x not in tj.horarios:
                                                iguais = False
                                                break
                                for x in tj.horarios:
                                        if x not in ti.horarios:
                                                iguais = False
                                                break
                                if iguais:
                                        logger.warning("\tAs turmas apresentam os mesmos horarios.")
                                        k = 0
                                        while(k<len(turmas)):
                                                if int(turmas[k].codigo)==int(tj.codigo) and int(turmas[k].turma)==int(tj.turma) \
                                                   and turmas[k].semestralidade == tj.semestralidade:
                                                        tj.eh_cliente = True
                                                        ti.turmas_clientes.append(tj)
                                                        print("\t" + str(turmas[k].id())+ " foi deletada e redefinida como fantasma.")
                                                        del turmas[k]
                                                else:
                                                        k+=1
                                        del pre_atribuidas[j]
                                else:
                                        logger.error(
                                                "\tERRO: Dados inconsistentes" +
                                                " para professor %s\n", pi.nome()
                                        )

                                        j += 1
                        else:

                                j += 1
                i += 1

        i=0
        while(i<len(pre_atribuidas)-1):
                j=i+1
                while(j<len(pre_atribuidas)):
                        if pre_atribuidas[i][1]==pre_atribuidas[j][1]:
                                del pre_atribuidas[j]
                                print("Mesma disciplina pre atribuida em duplicata: " + \
                                        str(pre_atribuidas[i][1].id()) + " atribuida a "+ \
                                        str(pre_atribuidas[i][0].id())+" e " + \
                                        str(pre_atribuidas[i][1].id())+". Segunda associaçao removida.")
                        else:
                                j+=1
                i+=1

        # Verifica licencas
        # -----------------

        print("\n")
        print("Checando licencas")
        print("-----------------\n")

        check_licencas(pre_atribuidas)

        # Verifica inaptidoes
        # -------------------

        print("\n")
        print("Checando inaptidoes")
        print("-------------------\n")

        check_inaptidao(pre_atribuidas)

        # Verifica cargas horarias
        # ------------------------

        print("\n")
        print("Checando cargas horarias")
        print("------------------------\n")

        p_fantasma = check_ch(professores,turmas,pre_atribuidas,constantes)
        
        # Devolve a lista de professores fantasmas (para fins de relatorio)
        return p_fantasma
        
############################################################################################################################
#########################################                AUXILIARES                         ################################
############################################################################################################################

def check_duplicadas(pre_atribuidas):
        
        i=0
        while(i<len(pre_atribuidas)-1):
                j=i+1
                while(j<len(pre_atribuidas)):
                        if pre_atribuidas[i][1]==pre_atribuidas[j][1]:
                                print("AVISO: Disciplina " + str(pre_atribuidas[i][1].id()) + " pre-atribuida em duplicata a:\n" + \
                                        "\t" + str(pre_atribuidas[i][0].id()) + "\n" + \
                                        "\t" + str(pre_atribuidas[j][0].id()) + ".\nSegunda associaçao removida.")
                                del pre_atribuidas[j]
                        else:
                                j+=1
                i+=1


def check_ch(professores, turmas, pre_atribuidas, constantes):

        # Esta funcao supoe que as inconsistencias com licencas ja
        # foram removidas. Sua funcao eh consertar possiveis
        # incompatibilidades com a carga horaria.

        logger = logging.getLogger('alforria')

        p_fantasma = []
        for p in professores:

                if p.temporario:
                        chmaxsem = int(constantes['chmax_temporario_semestral'])
                        chmaxanual = int(constantes['chmax_temporario_anual'])
                        chminanualgrad = int(constantes['chmin_graduacao'])
                        chminanual = int(constantes['chmin_temporario_anual'])
                else:
                        chmaxsem = int(constantes['chmax_efetivo_semestral'])
                        chmaxanual = int(constantes['chmax_efetivo_anual'])
                        chminanualgrad = int(constantes['chmin_graduacao'])
                        chminanual = int(constantes['chmin_efetivo_anual'])

                if p.licenca1 or p.licenca2:
                        chminanualgrad /= 2

                soma = p.chprevia1 + p.chprevia2
                soma1 = p.chprevia1
                soma2 = p.chprevia2

                chgrad = 0
                for (p1, t1) in [(p2, t2) for
                                 (p2, t2) in pre_atribuidas if p == p2]:

                        ch = t1.carga_horaria()
                        soma += ch
                        chgrad += ch

                        if t1.semestralidade == 1:
                                soma1 += ch
                        else:
                                soma2 += ch

                logger.debug("\t%s carga total pre-atribuida: %d.\n",
                             p.nome(), soma)

                # Ha poucas disciplinas com 2 horas, entao eh melhor
                # remover o professor caso sua carga horaria chegue
                # proxima do maximo
                #
                # Professor eh removido quando
                #
                # - Deu o minimo de horas para a graduacao
                # - Estourou o maximo de horas OU eh da POS

                if (soma >= (chmaxanual - 2) and chgrad >= chminanualgrad) or \
                   ((chgrad >= chminanualgrad) and
                    ((p.licenca1 and soma2 >= chmaxsem) or
                     (p.licenca2 and soma1 >= chmaxsem))):

                        logger.info("Pre-atribuição atinge carga horária máxima" +
                                    " anual de %s. Professor e disciplinas " +
                                    "pre-atribuidas serao removidos do problema.",
                                    p.nome())

                        p.carga_horaria = soma

                        p_fantasma.append(p)

                        for (p1, t1) in [(p2, t2) for (p2, t2) in pre_atribuidas if p == p2]:

                                p.turmas_a_lecionar.append(t1)

                                turmas.remove(t1)

                                pre_atribuidas.remove((p1, t1))

                                logger.info("\tRemovida turma %s", t1.id())

                        continue

                # Se professor esta de licenca, zera carga horaria previa

                if p.licenca1:
                        p.chprevia1 = 0

                if p.licenca2:
                        p.chprevia2 = 0

                if chgrad < chminanualgrad:
                        p.chmax = max(chmaxanual, soma + max(4, chminanualgrad - chgrad))

                        if p.pos:
                                p.chmax = max(chminanual, soma + max(4, chminanualgrad - chgrad))

                        if not p.licenca1:
                                p.chmax1 = max(chmaxsem, soma1 + max(4, chminanualgrad - chgrad))
                        if not p.licenca2:
                                p.chmax2 = max(chmaxsem, soma2 + max(4, chminanualgrad - chgrad))

                else:
                        if not p.licenca1 and soma1 > chmaxsem:
                                logger.info("Pre-atribuição viola carga horária " +
                                            "máxima do 1o sem. de %s. Aumentando " +
                                            "ch. maxima do semestre para %d", p.nome(), soma1)
                                p.chmax1 = soma1
                                p.chmax = max(chmaxanual, soma1)

                        if not p.licenca2 and soma2 > chmaxsem:
                                logger.info("Pre-atribuição viola carga horária " +
                                            "máxima do 2o sem. de %s. Aumentando " +
                                            "ch. maxima do semestre para %d", p.nome(), soma2)
                                p.chmax2 = soma2
                                p.chmax = max(chmaxanual, soma2)

        # Remove professores fantasmas
        for p in p_fantasma:
                p.fantasma = True
                professores.remove(p)

        return p_fantasma


def check_nao_atribuidas(turmas):

        logger = logging.getLogger('alforria')

        logger.info("\n")
        logger.info("Checando turmas sem professor")
        logger.info("-----------------------------\n")

        for t in turmas:

                if t.professor is None:

                        logger.warning("\t%15s sem professor", t.id())


def check_licencas(pre_atribuidas):

        logger = logging.getLogger('alforria')

        for (p, t) in pre_atribuidas:

                if p.licenca1 and t.semestralidade == 1:
                        logger.info("\tProfessor %s com disciplina %s pre-atribuida e " +
                                    "com licenca.\n\t\tLicenca SEMESTRE 1 removida.",
                                    p.nome(), t.id())
                        p.licenca1 = False

                if p.licenca2 and t.semestralidade == 2:
                        logger.info("\tProfessor %s com disciplina %s pre-atribuida e " +
                                    "com licenca.\n\t\tLicenca SEMESTRE 2 removida.",
                                    p.nome(), t.id())
                        p.licenca2 = False


def check_inaptidao(pre_atribuidas):

        logger = logging.getLogger('alforria')

        for (p, t) in pre_atribuidas:

                if t.grupo is not None and t.grupo.id in p.inapto:

                        logger.info("\tProfessor %s inapto para grupo %s de" +
                                    "disciplina pre-atribuida %s.\n\t\t" +
                                    "Inaptidao removida.",
                                    p.nome(), t.grupo.id, t.id())

                        p.inapto.remove(t.grupo.id)

############################################################################################################################
#########################################                IMPRIME ESTATISTICAS               ################################
############################################################################################################################
        
        
def estatisticas(professores,turmas):

        # Contabiliza carga horaria da graduacao

        chtotal=[0,0,0] #chtotal[i]: charga horaria total do semestre i
        for t in turmas:
                chtotal[t.semestralidade] += t.carga_horaria()

        n_efetivos1=0
        n_efetivos2=0
        n_temporarios1=0
        n_temporarios2=0
        ch_previa_tt1=0
        ch_previa_tt2=0
        ch_efetivos = 0
        ch_temporarios = 0
        for p in professores:
                if p.temporario:
                        if not p.licenca1:
                                n_temporarios1+=1
                        if not p.licenca2:
                                n_temporarios2+=1
                        ch_temporarios += p.carga_horaria_atrib()
                else:
                        if not p.licenca1:
                                n_efetivos1+=1
                        if not p.licenca2:
                                n_efetivos2+=1
                        ch_efetivos += p.carga_horaria_atrib()
                ch_previa_tt1+=p.chprevia1
                ch_previa_tt2+=p.chprevia2
        print("\nEstatisticas" + \
              "\n------------\n")
        print("Coeficiente de dobro - 1o sem: {0:4d}".format((chtotal[1]+ch_previa_tt1)/(n_efetivos1+2*n_temporarios1)))
        print("Coeficiente de dobro - 2o sem: {0:4d}".format((chtotal[2]+ch_previa_tt2)/(n_efetivos2+2*n_temporarios2)))
        print("Carga horaria:")
        print("\t1o sem = " + str(chtotal[1]) + ", professores: " + str(n_efetivos1) + \
                " efetivos e " + str(n_temporarios1) + " temporarios")
        print("\t2o sem = " + str(chtotal[2]) + ", professores: " + str(n_efetivos2) + \
                " efetivos e " + str(n_temporarios2) + " temporarios")
        print("Carga horaria previa total:")
        print("\t1o sem = " + str(ch_previa_tt1))
        print("\t2o sem = " + str(ch_previa_tt2))
        print("")
        print("Carga horaria total graduacao: " + str(chtotal[1] + chtotal[2]))
        print("\tEfetivos: " + str(ch_efetivos))
        print("\tTemporarios: " + str(chtotal[1] + chtotal[2] - ch_efetivos) +
              " (" + str(ch_temporarios) + ")")
