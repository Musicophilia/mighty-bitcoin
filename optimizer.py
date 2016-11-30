import matplotlib.pyplot as plt
from models import *

# Compute the attack utility over withdraw/sell time
btc_f_stolen = 0.005
btc_f_owned_0 = 0.01
mining_power = 0.1
discount_rate = 0.99

num_days = 30

def run_optimizer():
    attack_utility_list = []
    for t in xrange(num_days):
        withdraw_btc_delta = t
        sell_machines_delta = withdraw_btc_delta
        model_t = utility_model(btc_f_stolen=btc_f_stolen,
                                btc_f_owned_0=btc_f_owned_0,
                                mining_power=mining_power,
                                discount_rate=discount_rate,
                                withdraw_btc_delta=withdraw_btc_delta,
                                sell_machines_delta=sell_machines_delta)
        attack_utility = model_t.compute_attack_utility()
        print "Attack utility at t = %d: %f" % (t, attack_utility)
        attack_utility_list.append(attack_utility)
    plt.plot(range(num_days), attack_utility_list)
    plt.xlabel('Withdraw Time Delta After Attack (in Days)')
    plt.ylabel('Attack Utility')
    plt.show()
    max_attack_utility = max(attack_utility_list)
    optimal_withdraw_time = attack_utility_list.index(max_attack_utility)
    return max_attack_utility, optimal_withdraw_time

if __name__ == '__main__':
    max_attack_utility, optimal_withdraw_time = run_optimizer()
    print "Max utility possible:", max_attack_utility
    print "Optimal time to withdraw BTC after attack:", optimal_withdraw_time


