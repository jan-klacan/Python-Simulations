# Simulation of forest fires in Python
## This text is for the Forest_Fire_Simulation.py. 
The simulation is based on The Big Book of Small Python Projects by Al Sweigart (2021). Check "Project 29, Forest Fire Sim". My code builds directly on the chapter's code. I added the following, some of which are based on the suggested exercises in the chapter:
- added lakes that spawn in the initial forest grid based on the initial lake coverage probability
- divided trees into 2 types (pine and oak), which have their respective probabilities to catch fire spontaneously and to catch fire from neighboring trees
- implemented user input prompts so users can adjust the values for the parameters mentioned above, and also adjust the:
    - initial tree coverage
    - tree grow chance during forest updates
    - length of the pause between iterations
- expanded the legend that is displayed below the running simulation

Enjoy.