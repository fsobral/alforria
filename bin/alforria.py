from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
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

# Configura nivel de saida

logger = logging.getLogger('alforria')

logger.addHandler(logging.StreamHandler())

logger.setLevel(logging.ERROR)

professores = None

grupos = None

turmas = None

pre_atribuidas = None

def _load_() :
    """

    This function loads all the data.

    """

    global _PATHS_PATH
    global _ALFCFG_PATH
    global professores
    global grupos
    global turmas
    global pre_atribuidas

    paths = leitura.ler_conf(_PATHS_PATH)
    configuracoes = leitura.ler_conf(_ALFCFG_PATH)

    # Carrega os grupos de disciplinas
    grupos = leitura.ler_grupos(paths["GRUPOSPATH"])

    # Carrega os professores e suas preferencias e ajusta os valores dados
    # às preferências para que fiquem entre 0 e 10.
    professores = leitura.ler_pref(paths["PREFPATH"], grupos,
                                   int(configuracoes["MAXIMPEDIMENTOS"]))
    for p in professores:
        p.ajustar()

    # Carrega as turmas de disciplinas do ano e elimina as disciplinas
    # fantasmas (turmas com números diferentes que são, na verdade, a
    # mesma turma)

    turmas = leitura.ler_sar(paths["SARPATH"], grupos)

    turmas = leitura.caca_fantasmas(paths["FANTPATH"], turmas)

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

    global pre_atribuidas
    global professores
    global turmas

    if pre_atribuidas is None or professores is None or turmas is None:

        print("Necessary to load data first.")

    nargs = len(args)

    if nargs == 0:

        for (p, t) in pre_atribuidas:

            p.turmas_a_lecionar.append(t)

            t.professor = p
            
    elif nargs == 3:

        name = args[0]

        tcod = args[1]

        ttur = args[2]
        
        for p in professores:

            if name == p.nome():

                for t in turmas:

                    if tcod == t.codigo and ttur == t.turma:

                        p.add_course(t)

                        t.add_professor(p)

    else:

        logger.error("Usage: attribute [professor cod turma].")


def _show_(*args):

    global professores
    global turmas
    
    if len(args) != 2 and len(args) != 3:

        print("Usage: show professor <name>")
        print("Usage: show turma <codigo> <turma>")

        return

    if professores is None or turmas is None:

        print("Necessary to load data first.")

        return

    if args[0] == u'professor':

        name = args[1]

        for p in professores:

            if name in p.nome():

                print(p)

    elif args[0] == u'turma':

        cod = args[1]

        tur = None
        
        if len(args) == 3:

            tur = args[2]

        for t in turmas:

            if t.codigo == cod:

                if tur is None:

                    print(t)

                elif t.turma == tur:

                    print(t)

    else:

        print("Usage: show professor <name>")
        print("Usage: show turma <codigo> <turma>")


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

    global _CONST_PATH
    global professores

    constantes = leitura.ler_conf(_CONST_PATH)

    if professores is None:

        print("Necessary to load data first.")

        return

    if len(args) == 0:

        for p in professores:

            check.check_p(p, constantes)

    elif len(args) == 1:

        name = args[0]

        for p in [p1 for p1 in professores if name in p1.nome()]:

            check.check_p(p, constantes)

        
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

        else:

            print("Unknown command %s" % cmds[0])

                                           
def mainfunc():

    session = PromptSession(completer=_alforria_completer)

    while True:

        try:

            command = session.prompt('> ')

        except KeyboardInterrupt:

            continue

        except EOFError:

            break

        else:

            parse_command(command)

    print("Exiting.")

if __name__ == '__main__':

    mainfunc()
        

    

