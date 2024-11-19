import random, sys, time, bext


# BLOCK 1 (HARD-CODED INPUTS): Parameters for the grid dimensions and visual 'icons' for all possible grid cell candidates.
width = 79  
height = 22  

pine_tree = "A"  
oak_tree = "P"  
fire = "M"  
lake = "O"  
empty = " "   


# BLOCK 2 (FUNCTION): Handles numeric input validation within a range, returns a default value if the input is not filled in.
def get_value_input(prompt, default_value) :
    while True :
        try :
            user_value = input(prompt)
            if not user_value :
                return default_value
            user_value = float(user_value)
            if 0 <= user_value <= 100 :
                return user_value
            else :
                print("The number must be between 0 and 100.")
        except ValueError :
            print("Please enter a valid number.")


# BLOCK 3 (FUNCTION): Handles user input, initializes the forest, and updates the state of the forest grid with each iteration.
def main_cycle() :
    
    global initial_tree_coverage, initial_lake_coverage
    global tree_growth_chance, spontaneous_fire_chance_pine, spontaneous_fire_chance_oak
    global catch_fire_from_spreading_chance_pine, catch_fire_from_spreading_chance_oak
    global pause_length
    
    bext.bg("cyan")
    bext.fg("black")
    print("This is a basic simulation of forest fires based on Sweigart (2021) - Big Book of Small Python Projects.")
    print("I added basic user input prompts and some parameters that extend the scope of the simulation.")
    print("You will be prompted to input values for these as well as for the parameters that were already in the original simulation.")
    print("You can also skip filling in the values by pressing Enter. In that case, the simulation will run on default inputs.")
    print("Start by entering the initial tree coverage below. Have fun!")
    bext.bg("reset")
    bext.fg("reset")
    initial_tree_coverage = get_value_input("Enter initial tree coverage in the forest (%, 0 - 100): ", 2)  
    initial_lake_coverage = get_value_input("Enter initial lake coverage in the forest (%, 0 - 100): ", 0.3)  
    tree_growth_chance = get_value_input("Enter tree growth probability at each iteration (%, 0 - 100): ", 0.75)
    spontaneous_fire_chance_pine = get_value_input("Enter probability that a pine tree will catch fire spontanenously at each iteration (%, 0 - 100): ", 0.5)
    spontaneous_fire_chance_oak = get_value_input("Enter probability that an oak tree will catch fire spontaneously at each iteration (%, 0 - 100): ", 0.5) 
    catch_fire_from_spreading_chance_pine = get_value_input("Enter probability that a pine tree will catch fire from a neighboring burning tree at each iteration (%, 0 - 100): ", 75) 
    catch_fire_from_spreading_chance_oak = get_value_input("Enter probability that an oak tree will catch fire from a neighboring burning tree at each iteration (%, 0 - 100): ", 65)
    pause_length = get_value_input("Enter the length of pause between iterations (seconds, 0 - 100): ", 0.15)  
    
    initial_tree_coverage /= 100
    initial_lake_coverage /= 100
    tree_growth_chance /= 100 
    spontaneous_fire_chance_pine /= 100 
    spontaneous_fire_chance_oak /= 100
    catch_fire_from_spreading_chance_pine /= 100
    catch_fire_from_spreading_chance_oak /= 100
    
    forest = createNewForest()  
    bext.clear()  

    while True :  
        displayForest(forest)  

        nextForest = {"width":forest["width"],
                      "height":forest["height"]}  
        
        for x in range(forest["width"]) :  
            for y in range(forest["height"]) :
                if (x,y) in nextForest :  
                    continue  
                if ((forest[(x,y)] == empty)  
                    and (random.random() <= tree_growth_chance)) :  
                    nextForest[(x,y)] = random.choice([pine_tree, oak_tree])  
                elif ((forest[(x,y)] == pine_tree)  
                    and (random.random() <= spontaneous_fire_chance_pine)) :  
                    nextForest[(x,y)] = fire  
                elif ((forest[(x,y)] == oak_tree)  
                    and (random.random() <= spontaneous_fire_chance_oak)) : 
                    nextForest[(x,y)] = fire
                elif forest[(x,y)] == fire :  
                    for ix in range(-1,2) :  
                        for iy in range(-1,2) :
                            if (forest.get((x+ix, y+iy)) == pine_tree
                                and (random.random() <= catch_fire_from_spreading_chance_pine)) :
                                nextForest[(x+ix, y+iy)] = fire
                            elif (forest.get((x+ix, y+iy)) == oak_tree
                                and (random.random() <= catch_fire_from_spreading_chance_oak)) :
                                nextForest[(x+ix, y+iy)] = fire
                            elif forest.get((x+ix, y+iy)) == lake :
                                continue
                        nextForest[(x,y)] = empty  
                else :
                    nextForest[(x,y)] = forest[(x,y)]  
        forest = nextForest  

        time.sleep(pause_length)  


# BLOCK 4 (FUNCTION): Called within main_cycle() to create the initial forest grid. 
# Randomly places pine trees, oak trees, lakes, or empty spaces according to set probabilities.
def createNewForest() :
    forest = {"width":width, "height":height}  
    for x in range(width) :  
        for y in range(height) :  
            if (random.random() <= initial_tree_coverage) :  
                forest[(x,y)] = random.choice([pine_tree, oak_tree])  
            elif (random.random() <= initial_lake_coverage) :  
                forest[(x,y)] = lake  
            else :
                forest[(x,y)] = empty
    return forest


# BLOCK 5 (FUNCTION): Called within main_cycle() to set cursor position, color-code the output, and print a legend and probabilities to the screen.
def displayForest(forest) :
    bext.goto(0,0)  
    for y in range(forest["height"]) :
        for x in range (forest["width"]) :
            if forest[(x,y)] == pine_tree :
                bext.fg("green")  
                print(pine_tree, end= "")  
            elif forest[(x,y)] == oak_tree :
                bext.fg("yellow")
                print(oak_tree, end= "")
            elif forest[(x,y)] == fire :
                bext.fg("red")  
                print(fire, end= "")
            elif forest[(x,y)] == lake :
                bext.fg("cyan")
                print(lake, end= "")
            elif forest[(x,y)] == empty :
                print(empty, end= "")
        print()
    bext.fg("reset")
    print("Legend: ", end= "")
    bext.fg("green")
    print("Pine tree ", end= "")
    bext.fg("yellow")
    print("Oak tree ", end= "")
    bext.fg("cyan")
    print("Lake ", end= "")
    bext.fg("red")
    print("Fire")
    bext.fg("reset")
    print("Tree growth probability: {}% ".format(tree_growth_chance*100))  
    print("Probability of catching fire spontaneously - pine: {}% ".format(spontaneous_fire_chance_pine*100))
    print("Probability of catching fire spontaneously - oak: {}% ".format(spontaneous_fire_chance_oak*100))
    print("Probability that a pine tree will catch fire from a neighboring burning tree: {}% ".format(catch_fire_from_spreading_chance_pine*100))
    print("Probability that an oak tree will catch fire from a neighboring burning tree: {}% ".format(catch_fire_from_spreading_chance_oak*100))
    print("Ctrl-C TO QUIT")


# BLOCK 6 (IF BLOCK): Checks if the script is ran directly and not within another script - if so, calls main_cycle(), and makes sure that Ctrl-C exits the program.
if __name__ == "__main__" :  
    try :
        main_cycle()  
    except KeyboardInterrupt :  
        sys.exit()