from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, merge_completers
import logging

import funcoes_leitura as leitura
import funcoes_escrita as escrita
import check

_PATHS_PATH = u'../config/paths.cnf'
_ALFCFG_PATH = u'../config/alforria.cnf'
_CONST_PATH = u'../config/constantes.cnf'

_alforria_completer = WordCompleter([
    'attribute', 'set_paths', 'set_config', 'load', 'to_pdf', 'check', 'verbosity', 'show', 'professor'
    ], ignore_case=True)

_session = None

# Configura nivel de saida

logger = logging.getLogger('alforria')

logger.addHandler(logging.StreamHandler())

logger.setLevel(logging.ERROR)

professores = None

grupos = None

turmas = None

pre_atribuidas = None

_professor_search_name = dict()

_course_search_id = dict()

def _load_() :
    """

    This function loads all the data.

    """

    global _PATHS_PATH, _ALFCFG_PATH
    global professores, grupos, turmas, pre_atribuidas
    global _professor_search_name, _course_search_id

    paths = leitura.ler_conf(_PATHS_PATH)
    configuracoes = leitura.ler_conf(_ALFCFG_PATH)

    # Carrega os grupos de disciplinas
    grupos = leitura.ler_grupos(paths["GRUPOSPATH"])

    # Carrega os professores e suas preferencias e ajusta os valores dados
    # às preferências para que fiquem entre 0 e 10.
    professores = leitura.ler_pref(paths["PREFPATH"], grupos,
                                   int(configuracoes["MAXIMPEDIMENTOS"]))

    # Updates the names of professors to the autocompleter
    names = []
    
    for p in professores:
        
        p.ajustar()

        names.append(p.nome())

    # Cria uma lista de busca dos professores por nome, para agilizar
    # a busca
    _professor_search_name = dict(
        [(p.nome(), p) for p in professores]
    )

    global _session

    if _session is not None:

        _session.completer = merge_completers([_session.completer, WordCompleter(names)])
        
    # Carrega as turmas de disciplinas do ano e elimina as disciplinas
    # fantasmas (turmas com números diferentes que são, na verdade, a
    # mesma turma)

    turmas = leitura.ler_sar(paths["SARPATH"], grupos)

    turmas = leitura.caca_fantasmas(paths["FANTPATH"], turmas)

    # Updates the names of the courses to the autocompleter

    names = [t.id() for t in turmas]

    if _session is not None:

        _session.completer = merge_completers([_session.completer, WordCompleter(names)])

    # Cria uma lista de busca de turmas por id
    # (NOME_TURMA_SEMESTRALIDADE) para agilizar as buscas

    _course_search_id = dict(
        [(t.id(), t) for t in turmas]
    )
        
    # Carrega o arquivo de disciplinas pre-atribuidas
    pre_atribuidas = leitura.ler_pre_atribuidas(paths["ATRIBPATH"], paths["FANTPATH"],
                                                professores, turmas)


def _set_log_level_(level):

    """

    This function changes the log level for Alforria.

    """

    global logger
    
    v = int(cmds[1])

    if v < 1:

        logger.setLevel(logging.ERROR)

    elif v == 1:

        logger.setLevel(logging.INFO)

    else:

        logger.setLevel(logging.DEBUG)

    print('Changed logger level')
    
    
def _attribute_(*args):
    """This function attributes courses to professors and professors to
    courses, according to the specified files or according to the arguments.

    """

    global pre_atribuidas, professores, turmas

    if pre_atribuidas is None or professores is None or turmas is None:

        print("Necessary to load data first.")

    nargs = len(args)

    if nargs == 0:

        for (p, t) in pre_atribuidas:

            p.turmas_a_lecionar.append(t)

            t.professor = p
            
    elif nargs >= 2:

        name = args[0]

        cour = args[1:]

        if name not in _professor_search_name:

            logger.error("Nao encontrado docente: %s", name)

            return
        
        p = _professor_search_name[name]

        for c in cour:

            if c not in _course_search_id:

                logger.error("Nao encontrada turma: %s", c)

                continue

            t = _course_search_id[c]

            p.add_course(t)

            t.add_professor(p)

            # Se a disciplina anual, sabemos S1 e S2 estao
            # vinculados. Desta forma, procuramos S2 na lista de
            # turmas
            
            if t.vinculada and t.semestralidade == 1:

                cvinc = c.replace("S1", "S2")
                
                if cvinc not in _course_search_id:

                    logger.error("Nao encontrada turma vinculada: %s", cvinc)

                    continue

                tvinc = _course_search_id[cvinc]

                p.add_course(tvinc)

                tvinc.add_professor(p)

    else:

        logger.error("Uso: attribute [professor turma1 turma2 ...].")


def _show_(*args):

    global professores, turmas, _professor_search_name, _course_search_id
    
    if len(args) != 1:

        print("Usage: show <professor ou turma>")

        return

    if professores is None or turmas is None:

        print("Necessary to load data first.")

        return

    name = args[0]

    if name not in _professor_search_name:

        if name not in _course_search_id:

            logger.error("Nao encontrado: %s.", name)

        else:
            
            print(_course_search_id[name])

    else:

        print(_professor_search_name[name].display())


def _save_csv_(*args):
    """
    This function saves the relations professors and classes.
    """

    global _ALFCFG_PATH
    global professores, turmas

    configuracoes = leitura.ler_conf(_ALFCFG_PATH)

    fname = configuracoes["RELDIR"] + "/atribuicoes.csv"

    if len(args) > 1:

        logger.error("Usage: save [fname]")

    elif len(args) == 1:

        fname = configuracoes["RELDIR"] + "/" + args[0]
    
    escrita.escreve_atribuicoes(professores, turmas, fname)


def _to_pdf_():

    global _ALFCFG_PATH
    global professores

    if professores is not None:

        configuracoes = leitura.ler_conf(_ALFCFG_PATH)

        prof_ord = sorted(professores, key=lambda x: x.nome())

        escrita.cria_relatorio_geral(prof_ord, configuracoes["RELDIR"])

        print("Report created in directory %s" % configuracoes["RELDIR"])

    else:

        print("Necessary to load data first.")


def _check_(*args):

    global _CONST_PATH, professores, _professor_search_name, _course_search_id

    constantes = leitura.ler_conf(_CONST_PATH)

    if professores is None:

        print("Necessary to load data first.")

        return

    if len(args) == 0:

        for p in professores:

            check.check_p(p, constantes)

    elif len(args) == 1:

        name = args[0]

        if name not in _professor_search_name:

            logger.error("Nao encontrado: %s.", name)

        else:

            check.check_p(_professor_search_name[name], constantes)

    elif len(args) >= 2:

        name = args[0]

        cour = args[1:]

        if name not in _professor_search_name:

            logger.error("Nao encontrado: %s.", name)

            return

        clist = [_course_search_id[c] for c in cour if c in _course_search_id]

        clist2 = [_course_search_id[(c.id()).replace("S1", "S2")] \
                  for c in clist \
                  if (c.vinculada and c.semestralidade == 1)]

        clist.extend(clist2)
                  
        if len(clist) == 0:

            logger.error("Nao encontrada nenhuma disciplina.")

            return

        check.check_p_c(_professor_search_name[name],
                        clist, constantes)

    else:

        logger.error("Uso: check [professor [turma1 turma2 ...]]")

        
def parse_command(command):

    """

    This function parses the commands and calls the correct functions.

    """

    global _PATHS_PATH
    global _ALFCFG_PATH
    global professores

    cmds = command.split()

    if len(cmds) > 0:

        if cmds[0] == u'load':

            _load_()

        elif cmds[0] == u'verbosity':

            if len(cmds) == 2:
                _set_log_level_(cmds[1])
            else:
                print("Usage: %s log_level" % cmds[0])
            
        elif cmds[0] == u'set_paths':

            _PATHS_PATH = cmds[1]

        elif cmds[0] == u'set_config':

            _ALFCFG_PATH = cmds[1]

        elif cmds[0] == u'attribute':

            _attribute_(*cmds[1:])

        elif cmds[0] == u'to_pdf':

            _to_pdf_()
            
        elif cmds[0] == u'show':

            _show_(*cmds[1:])

        elif cmds[0] == u'check':

            _check_(*cmds[1:])

        elif cmds[0] == u'save':

            _save_csv_(*cmds[1:])

        else:

            print("Unknown command %s" % cmds[0])

                                           
def mainfunc():

    global _session

    _session = PromptSession(completer=_alforria_completer)

    while True:

        try:

            command = _session.prompt('> ')

        except KeyboardInterrupt:

            continue

        except EOFError:

            break

        else:

            parse_command(command)

    print("Exiting.")

if __name__ == '__main__':

    mainfunc()
        

    

