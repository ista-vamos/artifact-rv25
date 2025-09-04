all: full

short:
	make -C experiments/ehl-shl short
	make -C experiments/ifm24 short
	make -C experiments/openssl short
	make -C plots -k

full:
	make -C experiments/ehl-shl full
	make -C experiments/ifm24 full
	make -C experiments/openssl full
	make -C plots -k

