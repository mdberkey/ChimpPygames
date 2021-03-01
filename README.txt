These programs are for conducting expirements and gathering data for primate research running on a Raspberry PI 4, Elo Touchscreen, Ontrak Relay I/O interface, and a custom Pellet Dispenser.

- SETUP -
1. Make sure Raspberry PI is connected to the internet by checking the wifi/ethernet symbol in the top right corner.
2. Open Terminal on Raspberry PI by clicking the raspberry button in the top left corner > Accessories > Terminal
3. Update apt by entering into the terminal: sudo apt update
4. After it has finished, download/update git by entering into the terminal: sudo apt install git
5. After it has finished, download the ChimpPygames repo by entering into the terminal: git clone https://github.com/mdberkey/ChimpPygames.git
6. After it has finished change directory into ChimpPygames by entering into the terminal: cd ChimpPygames
7. Start the setup by entering into the terminal: make setup
8. Wait for the terminal shell to display "setup complete" then hit enter
9. The ChimpPygames folder should appear on the desktop.
10. If no errors occured then everything should be set up and ready to run.

- HOW TO USE - (after setup)
1. Make sure touchscreen, relay, and pellet dispenser are all plugged in correctly (Dispencer Relay Output wires should be in K1 sockets).
2. Edit the globalParameters.dat file in the ChimpPygames/PygameTools folder to alter parameters for every program.
3. Open Terminal on Raspberry PI and enter: cd Desktop/ChimpPygames
4. Start the program by entering into the terminal: make
5. A list of commands should appear in the terminal which contain every expirement.
6. Before starting however, one should make sure the parameters are set right:
         1. Open the ChimpPygames folder on the desktop and then the corresponding folder to the desired experiment.
         2. Edit the desired parameters in parameters.dat in the folder and SAVE the file.

- ALTERNATIVE METHOD TO USE - (old way)
1. Open the ChimpPygames folder on the desktop and then the corresponding folder to the desired experiment.
2. Double click on the <experiment_name>.sh file, a box should pop up, then click "execute" to begin the experiments.
5. After the expirement is done or exited manually, open the results.csv file to gather data from the experiment/s.

- HOW TO UPDATE -
1. Make sure Raspberry is connected to internet.
2. Open Terminal and enter: cd Desktop/ChimpPygames
3. Enter into the Terminal: git pull
4. run setup.sh by double clicking on the file and clicking execute
5. After it has completed, ChimpPygames should be updated.

*Important Notes*
- Press ESC, Q, or DOWNKEY to stop and exit the experiment.
- Data is recorded every trial during an expirement. So data is saved even if one exits the expirement early.
- The experiments will simply add new data on top of any data already present within results.csv so be sure to clear it from time to time. See the ecsv command.
- parameters.dat MUST be saved after changing variables for them to take effect
- Read the parameters.dat closely and be sure to save it with the correct value format or else an error might occur
- If a program wont run, check that the parameters are completley correct
- Touchscreen calibration: xinput set-prop 7 'Coordinate Transformation Matrix' 1 0 0.015 0 1 0.075 0 0 1

Author: Michael Berkey (mberkey@wisc.edu)
