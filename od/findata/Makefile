all: fig4 tab1 prep

prep:
	mkdir -p results

short: fig4-short tab1-short


experiments-short:
	python3 ./run-fig4.py --out results/fig4ab.csv --bits=2,8 --traces-nums=500,2000,5000 --trials=3 --traces-lens=1000,4000
	python3 ./run-fig4.py --out results/fig4c.csv  --bits=1,2 --traces-lens=1000 --traces-nums=400,600 --trials=3 --monitors=hnl,hnl-stred --traces-no-stuttering
	$(MAKE) fig4-plot


experiments:
	python3 ./run.py --out results/out.csv
	#python3 ./run.py --out results/fig4c.csv --bits=1,2,4 --traces-lens=1000 --traces-nums=200,400,600,800 --monitors=ehl,ehl-stred
	#$(MAKE) fig4-plot


tab1:
	python3 ./run-tab1.py --out results/tab1.csv
	$(MAKE) tab1-show

tab1-short:
	python3 ./run-tab1.py --out results/tab1.csv --trials=3
	$(MAKE) tab1-show


IFM_RESULTS_DIR=../ifm24/od/results
plots: prep
	cd plots && ./plot.py $(IFM_RESULTS_DIR)/fig4ab.csv $(IFM_RESULTS_DIR)/fig4c.csv && cp plot.pdf ../fig4.pdf


tab1-show:
	cd plots && ./tab.py ../results/tab1.csv  | tee ../results/tab1.txt


original:
	cd plots && ./plot.py ../csv_from_paper/fig4ab.csv ../results/fig4c.csv && cp plot.pdf ../results/fig4.pdf
	cd plots && ./tab.py ../csv_from_paper/tab1.csv | tee ../results/tab1.txt
