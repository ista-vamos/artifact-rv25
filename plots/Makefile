RESULTS_DIR=../results

all: plot-ehl-shl plot-ifm plot-openssl

prep:
	mkdir -p $(RESULTS_DIR)


IFM_RESULTS_DIR=../experiments/ifm24/results
plot-ifm: prep
	./plot-ifm.py $(IFM_RESULTS_DIR)/out.csv && cp plot-1.pdf $(RESULTS_DIR)/ifm_plot.pdf

EHL_SHL_RESULTS_DIR=../experiments/ehl-shl/results
plot-ehl-shl: prep
	./plot-ehl-shl.py $(EHL_SHL_RESULTS_DIR)/out.csv  && cp plot.pdf $(RESULTS_DIR)/ehl-shl_plot.pdf

plot-join: prep
	./plot-join.py $(IFM_RESULTS_DIR)/out.csv $(FINDATA_RESULTS_DIR)/out.csv  && cp plot.pdf $(RESULTS_DIR)/plot.pdf



OPENSSL_RESULTS_DIR=../experiments/openssl/results
plot-openssl: prep
	./plot-openssl.py $(OPENSSL_RESULTS_DIR)/out.csv  && cp plot.pdf $(RESULTS_DIR)/openssl_plot.pdf



#tab1:
#	./tab.py ../results/tab1.csv  | tee ../results/tab1.txt


# original:
# 	cd plots && ./plot.py ../csv_from_paper/fig4ab.csv ../results/fig4c.csv && cp plot.pdf ../results/fig4.pdf
# 	cd plots && ./tab.py ../csv_from_paper/tab1.csv | tee ../results/tab1.txt
