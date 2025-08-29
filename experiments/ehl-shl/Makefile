all: prep

prep: ehl-8b/monitor shl-le/monitor
	mkdir -p results

ehl-8b/monitor:
	./generate-ehl.sh

shl-le/monitor:
	./generate-shl.sh


run-short: prep
	python3 ./run.py --out results/out.csv --traces-nums=1000,2000,4000 --trials=3 --traces-lens=1000


run: prep
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
