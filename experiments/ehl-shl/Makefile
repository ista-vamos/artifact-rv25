all: full

ehl-4b/monitor:
	./generate-ehl.sh 4b

ehl-8b/monitor:
	./generate-ehl.sh 8b

ehl-10b/monitor:
	./generate-ehl.sh 10b

ehl-12b/monitor:
	./generate-ehl.sh 12b

shl-le/monitor:
	./generate-shl.sh


short: shl-le/monitor ehl-10b/monitor 
	mkdir -p results
	python3 ./run.py --out results/out.csv --bits=10 --traces-nums=1000,2000,4000 --trials=3 --traces-lens=1000


full: shl-le/monitor ehl-4b/monitor ehl-8b/monitor ehl-10b/monitor ehl-12b/monitor
	mkdir -p results
	python3 ./run.py --out results/out.csv



# RESULTS_DIR=../../results
 
# original:
# 	cd plots && ./plot.py ../csv_from_paper/fig4ab.csv ../results/fig4c.csv && cp plot.pdf ../results/fig4.pdf
# 	cd plots && ./tab.py ../csv_from_paper/tab1.csv | tee ../results/tab1.txt
