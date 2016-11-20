import math

from model_utils import *
########################################################################################################################
def get_attack_value(btc_stolen=5, attack_time=0, withdraw_btc_delta=1, sell_machines_delta=2, mining_power=0.1,
                 discount_rate=1.0, btc_owned_before_attack=10, global_num_machines=10):
    btc_owned_post_attack = btc_stolen + btc_owned_before_attack
    btc_to_usd_withdraw = btc_to_usd_exchange_rate(attack_time + withdraw_btc_delta, attack_happened=True)
    btc_value_post_attack = btc_owned_post_attack * btc_to_usd_withdraw * \
                            math.pow(discount_rate, withdraw_btc_delta)

    sell_machines_time = attack_time + sell_machines_delta
    btc_to_usd_machine = btc_to_usd_exchange_rate(sell_machines_time, attack_happened=True)
    machine_sell_price_post_attack = mining_power * global_num_machines * \
                                     get_sell_price_per_machine(btc_to_usd_machine, sell_machines_time) * \
                                     math.pow(discount_rate, sell_machines_delta)

    attack_value = btc_value_post_attack + machine_sell_price_post_attack
    return attack_value

def get_no_attack_value(btc_owned=10, sell_time=0, mining_power=0.1, global_num_machines=10):
    btc_to_usd = btc_to_usd_exchange_rate(sell_time, attack_happened=False)
    btc_value = btc_owned * btc_to_usd


    machine_sell_price = mining_power * global_num_machines * \
                         get_sell_price_per_machine(btc_to_usd, sell_time)

    no_attack_value = btc_value + machine_sell_price
    return no_attack_value

def attack_utility(btc_stolen=5, attack_time=0, withdraw_btc_delta=1, sell_machines_delta=2, mining_power=0.1,
                   discount_rate=1.0, btc_owned_before_attack=10, global_num_machines=10):
    attack_value = get_attack_value(btc_stolen, attack_time, withdraw_btc_delta, sell_machines_delta, mining_power,
                         discount_rate, btc_owned_before_attack, global_num_machines)

    # comparing value of selling btc and machine at same time as attack
    sell_time = attack_time
    btc_owned = btc_owned_before_attack
    no_attack_value = get_no_attack_value(btc_owned, sell_time, mining_power, global_num_machines)

    utility = attack_value - no_attack_value
    return utility

if __name__ == '__main__':
    print attack_utility()


