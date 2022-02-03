import subprocess
import sys
import os

sys.path.append(os.path.join("home", "pi", "Desktop", "ChimpPygames"))

"""
Basic CLI UI
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
        "tcd": "SidesTask.sh",
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


def main():
    """
    Main frontend program. Allows user to run all tasks and clear csv files.
    """
    print(pcolors.HEADER + "Please choose an tasks to run by entering the corresponding abreviation or q to exit program:" + pcolors.ENDC)
    while True:
        print("\ntt1  : Training_Task_1")
        print("tt2  : Training_Task_2")
        print("tcd  : Two_Choice_Discimination")
        print("mts  : Match_To_Sample")
        print("dmts : Delayed_Match_To_Sample")
        print("ot   : Oddity_Testing")
        print("drt  : Delayed_Response_Task")
        print("ssar : Social_Stimuli_As_Rewards")
        print("test : Test cmd")  
        print("ecsv : Empties ALL results.csv files")  
        print("q    : Exits Program\n")
    
        userInput = input(pcolors.OKCYAN + "Enter command: " + pcolors.ENDC)
        if userInput == "q":
            print(pcolors.WARNING + "Exiting program...")
            exit()
        elif userInput == "test":
            print_params("Training_Task/parametersP1.dat")

            #file = open("Training_Task/parametersP1.dat")
            #print(loadtxt("Training_Task/parametersP1.dat"))
        elif userInput == "ecsv":
            msgStr = "ALL results.csv files within ChimpPygames will cleared and any data not stored outside will be lost!"
            
            if ynPrompt(msgStr, True):
                print(pcolors.OKGREEN + "Clearing all results.csv files..." + pcolors.ENDC)
                empty_csv()
                print(pcolors.OKBLUE + "Files cleared." + pcolors.ENDC)
            else:
                print(pcolors.OKBLUE + "Exited prompt." + pcolors.ENDC)
                continue
        elif not userInput in cmd_dict:
            print(pcolors.FAIL + "Command invalid: Please enter a valid command." + pcolors.ENDC)
        else:
            print_params(str(wd_dict.get(userInput)) + "/parameters.dat")
            if ynPrompt("Are all of the parameters above for the " 
                    + wd_dict.get(userInput) + " task set correctly?"):
                print(pcolors.OKGREEN + "Starting " + wd_dict.get(userInput) + pcolors.ENDC)
                subprocess.call(['sh', cmd_dict.get(userInput)], cwd = wd_dict.get(userInput))
                print(pcolors.OKBLUE + "Results Recorded. Exited " + wd_dict.get(userInput) + pcolors.ENDC)
            else:
                 print(pcolors.OKBLUE + "Exited prompt." + pcolors.ENDC)
                 continue

def ynPrompt(message="", warning=False):
    """
    Prompts the user with a yes or no question to continue with a message
    :param message: message displayed to user
    :param warning: puts warning labels around message if True and not if False
    """
    if warning:
        print(pcolors.WARNING + "### WARNING ###")
        print(message)
        print("### WARNING ###" + pcolors.ENDC)
    else:
        print(pcolors.WARNING + message + pcolors.ENDC)
    promptInput = input(pcolors.OKCYAN + "Do you want to continue? (enter y to continue or anything else to exit): " + pcolors.ENDC)
    if(promptInput == 'y'):
        return True
    else:
        return False

def print_params(filename):
    with open(filename) as file:
        for i,row in enumerate(file):
            if row[0] is "#":
                print(pcolors.OKBLUE + str(i) + " - " + row.rstrip() + pcolors.ENDC)
            else:
                print(pcolors.OKGREEN + str(i) + " - " + row.rstrip() + pcolors.ENDC)

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
    f = open("resultsP2.csv", "w+")
    f.close()
    os.chdir('../')


if __name__ == "__main__":
    main()

