import random
import matplotlib.pyplot as plt

import functions as f

# adds 10% chance per hit
# can go above 100%, triggering a T2 crit with above 100% chance
# resets after 6 T2 crits

# example: 120% chance means 20% chance to trigger a T2 crit
# example: 200% chance means 100% chance to trigger a T2 crit



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
        crit_average_history.append(f.run_shooting(starting_crit_chance, crit_chance_per_hit, sample_size, logfile))

    # evaluate results
    crit_gain, crit_gain_relative, crit_mod_payoff = f.evaluate_results(crit_average_history, starting_crit_chance_list)

    # finaliize log and plot
    f.finalize_log_and_plot(logfile, crit_average_history, starting_crit_chance_list, crit_gain, crit_gain_relative, crit_mod_payoff)
    
    # close logfile
    logfile.close()


if __name__ == "__main__":
    main()
    print("Simulation finished. Check Data folder for results.")