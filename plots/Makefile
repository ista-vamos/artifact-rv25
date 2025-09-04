RESULTS_DIR=../results

all: plot-ehl-shl plot-ifm tab

prep:
	mkdir -p $(RESULTS_DIR)


IFM_RESULTS_DIR=../experiments/ifm24/results
plot-ifm: prep
	./plot-ifm.py $(IFM_RESULTS_DIR)/out.csv && cp plot.pdf $(RESULTS_DIR)/ifm_plot.pdf
	cp $(IFM_RESULTS_DIR)/out.csv $(RESULTS_DIR)/ifm.csv

EHL_SHL_RESULTS_DIR=../experiments/ehl-shl/results
plot-ehl-shl: prep
	./plot-ehl-shl.py $(EHL_SHL_RESULTS_DIR)/out.csv  && cp plot.pdf $(RESULTS_DIR)/ehl-shl_plot.pdf
	cp $(EHL_SHL_RESULTS_DIR)/out.csv $(RESULTS_DIR)/ehl-shl.csv

OPENSSL_RESULTS_DIR=../experiments/openssl/results
tab:
	./tab.py $(OPENSSL_RESULTS_DIR)/out.csv | tee ../results/openssl_tab.txt

