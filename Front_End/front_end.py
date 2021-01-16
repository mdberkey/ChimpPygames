import subprocess
import sys
import os
sys.path.append(os.path.join("home", "pi", "Desktop", "ChimpPygames"))

"""
Basic work in progress command line UI
"""

class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

cmd_dict = {
        "tt1": "TrainingTaskP1.sh",
        "tt2": "TrainingTaskP2.sh",
        "tcd": "TwoChoiceDiscrim.sh",
        "mts": "MatchToSample.sh",
        "dmts": "DelayedMatchToSample.sh",
        "ot": "OddityTesting.sh",
        "drt": "DelayedResponseTask.sh",
        "ssar": "SocialStimuli.sh",
        }

wd_dict = {
        "tt1": "Training_Task",
        "tt2": "Training_Task",
        "tcd": "Two_Choice_Discrimination",
        "mts": "Match_To_Sample",
        "dmts": "Delayed_Match_To_Sample",
        "ot": "Oddity_Testing",
        "drt": "Delayed_Response_Task",
        "ssar": "Social_Stimuli_As_Rewards",
        }

"""
Main frontend program. Allows user to run all expirements and clear csv files.
"""
def main():
    """
    Main frontend program. Allows user to run all expirements and clear csv files.
    """
    print(pcolors.HEADER + "Please choose an expirement to run by entering the corresponding abreviation or q to exit program:" + pcolors.ENDC)
    while True:
        print("\ntt1  : Training_Task_1")
        print("tt2  : Training_Task_2")
        print("tcd  : Two_Choice_Discimination")
        print("mts  : Match_To_Sample")
        print("dmts : Delayed_Match_To_Sample")
        print("ot   : Oddity_Testing")
        print("drt  : Delayed_Response_Task")
        print("ssar : Social_Stimuli_As_Rewards")
        print("ecsv : Empties ALL results.csv files")  
        print("q    : Exits Program\n")
    
        usrInput = input(pcolors.OKCYAN + "Enter command: " + pcolors.ENDC)
        if usrInput == "q":
            print(pcolors.WARNING + "Exiting program...")
            exit()
        elif usrInput == "ecsv":
            print(pcolors.WARNING + "### WARNING ###")
            print("ALL results.csv files within ChimpPygames will cleared and any data not stored outside will be lost!")
            print("### WARNING ###" + pcolors.ENDC)
            promptInput = input(pcolors.OKCYAN + "Do you want to continue? (enter y to continue or anything else to exit): " + pcolors.ENDC)
            if(promptInput == 'y'):
                print(pcolors.OKGREEN + "Clearing all results.csv files..." + pcolors.ENDC)
                empty_csv()
                print(pcolors.OKBLUE + "Files cleared." + pcolors.ENDC)
            else:
                print(pcolors.OKBLUE + "Exited prompt." + pcolors.ENDC)
                continue
        elif not usrInput in cmd_dict:
            print(pcolors.FAIL + "Command invalid: Please enter a valid command." + pcolors.ENDC)
        else:
            print(pcolors.OKGREEN + "Starting " + wd_dict.get(usrInput) + pcolors.ENDC)
            subprocess.call(['sh', cmd_dict.get(usrInput)], cwd = wd_dict.get(usrInput))
            print(pcolors.OKBLUE + "Exited " + wd_dict.get(usrInput) + pcolors.ENDC)

def empty_csv():
    """
    empties all csv files in ChimpPygames
    """
    fname = "results.csv"
    for cmd in wd_dict:
        os.chdir(wd_dict.get(cmd))
        print(os.getcwd())
        f = open(fname, "w+")
        f.close()
        os.chdir('../')
    os.chdir(wd_dict.get("tt1"))
    f = open("resultsP1.csv", "w+")
    f.close()
    f = open("resultsP2.csv", "+w")
    f.close()
    os.chdir('../')


main()

