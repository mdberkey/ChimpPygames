These programs are for conducting expirements and gathering data for primate research running on a
Raspberry PI 4, Elo Touchscreen, Ontrak Relay I/O interface, and a custom Pellet Dispenser.

-SETUP-
0. Make sure Raspberry Pi is connected to the internet (for downloads)
1. Make sure the ChimpPygames folder is in the Desktop
2. Right Click on "setup.sh" in ChimpPygames
3. Click on "Properties" (at the bottom)
4. Click on "Permissions" tab
5. Change the permissions of "Execute:" from "Nobody" to "Anyone" from the dropdown menu
6. Click "ok"
7. Double Click "setup.sh"
8. Select "Execute in Terminal"
9. Wait for the terminal shell to display "setup complete" then hit enter
10. If no errors occured then everything should be set up and ready to run.

-HOW TO USE- (after setup)
1. Make sure touchscreen, relay, and pellet dispenser are all plugged in correctly (Relay Output wires should be in K1 sockets).
2. Edit the globalParameters.dat file in the PygameTools folder to alter parameters for every program
2. Open the folder corresponding to the desired experiment (PygameTools, venv, and reqs are not experiments).
3. Edit the desired parameters in parameters.dat in the folder and save the file.
4. Double click on the <experiment_name>.sh file, a box should pop up, then click "execute" to begin the experiments.
    * can also click on "execute using terminal" to see any errors
5. After the expirement is done or exited manually, open the results.csv file to gather data from the experiment/s.

*Important Notes*
- Press ESC, Q, or DOWNKEY to stop and exit the experiment.
- Data is recorded every trial during an expirement. So data is saved even if one exits the expirement early.
- The experiments will simply add new data on top of any data already present within results.csv so be sure to clear it from time
  to time.
- parameters.dat must be saved after changing variables for them to take effect
- Read the parameters.dat closely and be sure to save it with the correct value format or else and error might occur
- If a program wont run, check that the parameters are completley correct
- Touchscreen calibration: xinput set-prop 7 'Coordinate Transformation Matrix' 1 0 0.015 0 1 0.075 0 0 1

Author: Michael Berkey (mberkey@wisc.edu)