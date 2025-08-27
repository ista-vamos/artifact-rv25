all: prep

prep:
	mkdir -p results
	./generate-ehl.sh
	./generate-shl.sh

short: fig4-short tab1-short


run-short:
	python3 ./run.py --out results/out.csv --bits=8 --traces-nums=1000,2000,4000 --trials=3 --traces-lens=1000


run:
	python3 ./run.py --out results/out.csv



# IFM_RESULTS_DIR=../ifm24/od/results
# plots: prep
# 	cd plots && ./plot.py $(IFM_RESULTS_DIR)/fig4ab.csv $(IFM_RESULTS_DIR)/fig4c.csv && cp plot.pdf ../fig4.pdf
# 
# 
# tab1-show:
# 	cd plots && ./tab.py ../results/tab1.csv  | tee ../results/tab1.txt
# 
# 
# original:
# 	cd plots && ./plot.py ../csv_from_paper/fig4ab.csv ../results/fig4c.csv && cp plot.pdf ../results/fig4.pdf
# 	cd plots && ./tab.py ../csv_from_paper/tab1.csv | tee ../results/tab1.txt
