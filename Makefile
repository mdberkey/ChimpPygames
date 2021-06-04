run:
	./program_run.sh

setup: moveRepo
	./setup.sh

moveRepo:
	cd .. && mv ChimpPygames Desktop && mkdir CPG_Data

