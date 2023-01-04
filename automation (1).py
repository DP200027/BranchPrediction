import os

GEM5_HOME_DIR='/home/011/s/sx/sxm210368/branchpred/gem5'
PREDICTOR='/home/011/s/sx/sxm210368/branchpred/gem5/src/cpu/pred'
BASESIMPLECPU='/home/011/s/sx/sxm210368/branchpred/gem5/src/cpu/simple/BaseSimpleCPU.py'
BENCHMARKS='/home/011/s/sx/sxm210368/branchpred/gem5/m5out'
f = open(GEM5_HOME_DIR+'/results.txt', 'a') 

def build():
    os.chdir(GEM5_HOME_DIR)
    os.system('scons build/X86/gem5.opt')

def updateBranchPredictor():
	x = input ("Enter the section of the file to be updated: 1-BTBEntries 2-LocalBP 3-TournamentBP 4-BiModeBP\n")
	if (x==1):
		y = input("Enter Number of BTB Entries:")
		os.system('sed -i "s/BTB_VALUE/'+str(y)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')
	if (x==2):
		y = input("Enter local predictor size:")
		os.system('sed -i "s/LBP_LOCAL_PRED_SIZE/'+str(y)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')
	if (x==3):
		a = input("Enter local predictor size:")
		os.system('sed -i "s/TBP_LOCAL_PRED_SIZE/'+str(a)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')
		b = input("Enter global predictor size:")
		os.system('sed -i "s/TBP_GLOBAL_PRED_SIZE/'+str(b)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')
		c = input("Enter choice predictor size:")
		os.system('sed -i "s/TBP_CHOICE_PRED_SIZE/'+str(c)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')
	if (x==4):
		b = input("Enter global predictor size:")
		os.system('sed -i "s/BIBP_GLOBAL_PRED_SIZE/'+str(b)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')
		c = input("Enter choice predictor size:")
		os.system('sed -i "s/BIBP_CHOICE_PRED_SIZE/'+str(c)+'/g" '+PREDICTOR+'/BranchPredictorChanged.py')

def updateCPU():
	x = input("Enter the branch predictor to be used: 1-LocalBP 2-TournamentBP 3-BiModeBP\n")
	if(x==1):
		os.system('sed -i "51s/TournamentBP/LocalBP/" '+BASESIMPLECPU)
		os.system('sed -i "51s/BiModeBP/LocalBP/" '+BASESIMPLECPU)
		f.write('Using LocalBP\n')
		
	if(x==2):
		os.system('sed -i "51s/LocalBP/TournamentBP/" '+BASESIMPLECPU)
		os.system('sed -i "51s/BiModeBP/TournamentBP/" '+BASESIMPLECPU)
		f.write('Using TournamentBP\n')
	if(x==3):
		os.system('sed -i "51s/TournamentBP/BiModeBP/" '+BASESIMPLECPU)
		os.system('sed -i "51s/LocalBP/BiModeBP/" '+BASESIMPLECPU)
		f.write('Using BiModeBP\n')
	else:
		print("INvalid input")

def createCopyOfBranchPredictorfile():
	os.system('vi '+PREDICTOR+'BranchPredictorChanged.py')
	os.system('cp '+PREDICTOR+'/BranchPredictor.py '+PREDICTOR+'BranchPredictorChanged.py')

def benchmarks():
	x = input("Enter the benchmark to be used: 1-429.mcf 2-401.bzip2\n")
	if(x==1):
		os.chdir(BENCHMARKS+'/429.mcf')
		os.system('sh runGem5.sh')
		f.write('Using benchmark 429.mcf\n')
		fr = open(BENCHMARKS+'/429.mcf/m5out/stats.txt', 'r') 
		BTBMissPct = fr.readlines()[282]
		f.write(BTBMissPct+"\n")
		#BranchMispredPercent = fr.readlines()[316]
		#f.write(BranchMispredPercent+"\n")
	if(x==2):
		os.chdir(BENCHMARKS+'/401.bzip2')
		os.system('sh runGem5.sh')
		f.write('Using benchmark 401.bzip2\n')
		fr = open(BENCHMARKS+'/401.bzip2/m5out/stats.txt', 'r') 
		BTBMissPct = fr.readlines()[292]
		f.write(BTBMissPct)
		#BranchMispredPercent = fr.readlines()[327]
		#f.write(BranchMispredPercent+"\n")
	else:
		print("Invalid input")


for x in range(4):
	updateBranchPredictor()
build()
for x in range(3):
	updateCPU()
	build()
	os.system('./build/X86/gem5.opt ./configs/example/se.py -c ./tests/testprogs/hello/bin/x86/linux/hello')
	f_config = open(GEM5_HOME_DIR+'/m5out/config.ini', 'r') 
	config = f_config.readlines()[87:103]
	for line in config:
		f.write(line)
	for y in range(2):
		benchmarks()
	f.write('\n')
