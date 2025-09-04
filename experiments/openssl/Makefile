all: full

shl-eq/monitor:
	./generate-shl.sh


short: shl-eq/monitor
	mkdir -p results
	python3 ./run.py --out results/out.csv --traces-nums=1000,5000 --trials=3


full: shl-eq/monitor
	mkdir -p results
	python3 ./run.py --out results/out.csv


