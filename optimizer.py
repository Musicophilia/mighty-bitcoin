import matplotlib.pyplot as plt
from models import *

# Compute the attack utility over withdraw/sell time
default_btc_f_stolen  = 0.000008
default_btc_f_owned_0 = 0
default_mining_power  = 0.2
default_discount_rate = 0.9995

num_days = 30

def optimal_attack_utility(btc_f_stolen = default_btc_f_stolen,
                           btc_f_owned_0 = default_btc_f_owned_0,
                           mining_power = default_mining_power,
                           discount_rate = default_discount_rate,
                           plot = False):
    attack_utility_list = []
    for t in xrange(num_days):
        withdraw_btc_delta = t
        sell_machines_delta = withdraw_btc_delta
        attack_utility = get_attack_utility(btc_f_stolen=btc_f_stolen,
                                            btc_f_owned_0=btc_f_owned_0,
                                            mining_power=mining_power,
                                            discount_rate=discount_rate,
                                            withdraw_btc_delta=withdraw_btc_delta,
                                            sell_machines_delta=sell_machines_delta)
        if plot:
            print "Attack utility at t = %d: %f" % (t, attack_utility)
        attack_utility_list.append(attack_utility)
    if plot:
        plt.plot(range(num_days), attack_utility_list)
        plt.xlabel('Withdraw Time Delta After Attack (in Days)')
        plt.ylabel('Attack Utility')
        plt.show()
    max_attack_utility = max(attack_utility_list)
    optimal_withdraw_time = attack_utility_list.index(max_attack_utility)
    return max_attack_utility, optimal_withdraw_time

if __name__ == '__main__':
    max_attack_utility, optimal_withdraw_time = optimal_attack_utility(plot=True)
    print "Max utility possible:", max_attack_utility
    print "Optimal time to withdraw BTC after attack:", optimal_withdraw_time


