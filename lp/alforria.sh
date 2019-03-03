#/bin/bash

# Numero de threads. Deixe vazio para usar todas
NUM_THREADS=3

# Criterio de parada. Termina quando o GAP ficar abaixo desse valor
MIPGAP=0.6

# Inicializa o arquivo de excluidos
echo "set P_OUT := ;" > alforria2.dat

python ../bin/antes.py

if [ $# -gt 0 ]; then
    if [ $1 -gt "1" ]; then

    echo "Entrou"

    # Numero de iteracoes do processo
    NUM_ITERACOES=$1

    # Prepara para a primeira fase de otimizacao
    #cat alforria_restr.mod fobj1.mod > alforria.mod
    cat alforria_restr.mod fobj2.mod > alforria.mod

    for i in `seq 1 ${NUM_ITERACOES}`; do

	time nice -n 19 glpsol -m alforria.mod -d alforria.dat -d alforria2.dat --check --wlp alforria.lp;
	time nice -n 19 gurobi_cl Threads=${NUM_THREADS} MIPGap=${MIPGAP} ResultFile=alforria.sol alforria.lp;

	python ../bin/depois.py;

    done;

fi;

fi

# Prepara para a segunda fase de otimizacao
cat alforria_restr.mod fobj2.mod > alforria.mod

time nice -n 19 glpsol -m alforria.mod -d alforria.dat -d alforria2.dat --check --wlp alforria.lp;
time nice -n 19 gurobi_cl Threads=${NUM_THREADS} MIPGap=${MIPGAP} ResultFile=alforria.sol alforria.lp;

python ../bin/depois.py;
