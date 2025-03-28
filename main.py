import random
import matplotlib.pyplot as plt

# adds 10% chance per hit
# can go above 100%, triggering a T2 crit with above 100% chance
# resets after 6 T2 crits

# example: 120% chance means 20% chance to trigger a T2 crit
# example: 200% chance means 100% chance to trigger a T2 crit

def plotting(list_1, list_2, name):
    # plot results
    plt.plot(list_1, list_2)
    plt.xlabel('Crit Chance without Enervate')
    plt.ylabel(name)
    plt.title('Average crit chance vs starting crit chance')
    plt.savefig('./data/' + name + '.png')
    plt.clf()

def run_shooting(starting_crit_chance, crit_chance_per_hit, sample_size, logfile):
    # starting crit chance
    crit_chance = starting_crit_chance
    # number of hits
    hits = 0

    # store number of crits in list with index = tier
    crits = [0, 0, 0, 0]
    # count t2 crits since last reset / beginning
    crits_for_reset = 0


    while hits < sample_size:
        # roll for crit chance
        roll = random.random()
    
        if roll < (crit_chance - 2):
            crits[3] += 1
            crits_for_reset += 1
        elif roll < (crit_chance - 1):
            crits[2] += 1
            crits_for_reset += 1
        elif roll < crit_chance:
            crits[1] += 1
        else:
            crits[0] += 1

        # reset crit chance after 6 T2 crits
        if crits_for_reset >= 6:
            crits_for_reset = 0
            crit_chance = starting_crit_chance
        
        # increase hit count and crit chance
        hits += 1
        crit_chance += crit_chance_per_hit

    # calculate average crit chance over all hits by number of crits done
    total_crits = crits[1] + crits[2] * 2 + crits[3] * 3
    average_crit_chance = total_crits / hits

    # logfile.write results
    logfile.write("Results:")
    logfile.write(f'Average crit chance: {100 * average_crit_chance:.2f}%\n')
    logfile.write(f'Percentage of T0 crits: {crits[0] / hits * 100:.2f}%\n')
    logfile.write(f'Percentage of T1 crits: {crits[1] / hits * 100:.2f}%\n')
    logfile.write(f'Percentage of T2 crits: {crits[2] / hits * 100:.2f}%\n')
    logfile.write(f'Percentage of T3 crits: {crits[3] / hits * 100:.2f}%\n')

    return average_crit_chance
    

def evaluate_results(crit_average_history, starting_crit_chance_list):
    # evaluate results
    
    # calculate absolute crit gain for each starting crit chance (difference to starting crit chance)
    crit_gain = [0] * len(crit_average_history)
    for i in range(len(crit_average_history)):
        crit_gain[i] = crit_average_history[i] - starting_crit_chance_list[i]
    
    # calculate relative crit gain for each starting crit chance
    crit_gain_relative = [0] * len(crit_average_history)
    for i in range(len(crit_average_history)):
        crit_gain_relative[i] = crit_gain[i] / starting_crit_chance_list[i] if starting_crit_chance_list[i] != 0 else 0

    # calculate crit mod payoff. meaning how much crit chances comes from the starting crit chance
    # assuming youre using creeping bulseye
    crit_mod_payoff = [0] * len(crit_average_history)
    for i in range(len(crit_average_history)):
        crit_mod_payoff[i] = (2/3) * starting_crit_chance_list[i] / crit_average_history[i] if crit_average_history[i] != 0 else 0

    return crit_gain, crit_gain_relative, crit_mod_payoff



def finalize_log_and_plot(logfile, crit_average_history, starting_crit_chance_list, crit_gain, crit_gain_relative, crit_mod_payoff):
    # logfile.write average crit chance for each starting crit chance
    logfile.write("\n\n\n")
    logfile.write("Average crit chance for each starting crit chance:\n")
    for i in range(len(crit_average_history)):
        logfile.write(f'Starting crit chance: {100 * starting_crit_chance_list[i]:.2f}% - Average crit chance: {100 * crit_average_history[i]:.2f}%\n')
    # plot average crit chance for each starting crit chance
    plotting(starting_crit_chance_list, crit_average_history, "Average_crit_chance")

    # logfile.write absolute crit gain for each starting crit chance
    logfile.write("\n\n\n")
    logfile.write("Absolute crit gain for each starting crit chance:\n")
    for i in range(len(crit_average_history)):
        logfile.write(f'Starting crit chance: {100 * starting_crit_chance_list[i]:.2f}% - Absolute crit gain: {100 * crit_gain[i]:.2f} added %\n')
    # plot absolute crit gain for each starting crit chance
    plotting(starting_crit_chance_list, crit_gain, "Absolute_crit_gain")

    # logfile.write relative crit gain for each starting crit chance
    logfile.write("\n\n\n")
    logfile.write("Relative crit gain for each starting crit chance:\n")
    for i in range(len(crit_average_history)):
        logfile.write(f'Starting crit chance: {100 * starting_crit_chance_list[i]:.2f}% - Relative crit gain: {100 * crit_gain_relative[i]:.2f}%\n')
    # plot relative crit gain for each starting crit chance
    plotting(starting_crit_chance_list, crit_gain_relative, "Relative_crit_gain")

    # logfile.write crit mod payoff for each starting crit chance
    logfile.write("\n\n\n")
    logfile.write("Crit mod payoff for each starting crit chance:\n")
    for i in range(len(crit_average_history)):
        logfile.write(f'Starting crit chance: {100 * starting_crit_chance_list[i]:.2f}% - Crit mod payoff: {100 * crit_mod_payoff[i]:.2f}%\n')
    # plot crit mod payoff for each starting crit chance
    plotting(starting_crit_chance_list, crit_mod_payoff, "Crit_mod_payoff")



def main():
    # logfile
    logfile = open("./data/log.txt", "w")

    # sample size
    sample_size = 100000
    # starting crit chance
    starting_crit_chance_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # crit chance per hit
    crit_chance_per_hit = 0.1
    # storage for average crit chance
    crit_average_history = []

    # run simulation for each starting crit chance
    for i in starting_crit_chance_list:
        logfile.write(f"\nStarting crit chance: {i * 100}%\n")
        starting_crit_chance = i
        crit_average_history.append(run_shooting(starting_crit_chance, crit_chance_per_hit, sample_size, logfile))

    # evaluate results
    crit_gain, crit_gain_relative, crit_mod_payoff = evaluate_results(crit_average_history, starting_crit_chance_list)

    # finaliize log and plot
    finalize_log_and_plot(logfile, crit_average_history, starting_crit_chance_list, crit_gain, crit_gain_relative, crit_mod_payoff)
    
    # close logfile
    logfile.close()


if __name__ == "__main__":
    main()
    print("Simulation finished. Check Data folder for results.")