#!/bin/bash
sudo apt-get update
sudo apt-get install python3

chmod +x Training_Task/TrainingTaskP1.sh
chmod +x Training_Task/TrainingTaskP2.sh
chmod +x Delayed_Match_To_Sample/DelayedMatchToSample.sh
chmod +x Delayed_Response_Task/DelayedResponseTask.sh
chmod +x Match_To_Sample/MatchToSample.sh
chmod +x Oddity_Testing/OddityTesting.sh
chmod +x Social_Stimuli_As_Rewards/SocialStimuli.sh
chmod +x Two_Choice_Discrimination/TwoChoiceDiscrim.sh
chmod +x PygameTools/pellet.sh

whiptail \
         --title "ChimpPygames Setup" \
         --msgbox "Setup Complete" 8 45
echo "setup complete"