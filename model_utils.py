# Functions which Brandon will implement
from __future__ import division

blocks_per_period = 144
asic_recuperation_period = 250
block_reward = 12.5

def btc_to_usd_exchange_rate(time, fraction_of_btc_stolen):
    # time is absolute time
    # TODO: Replace with something that makes sense
    if fraction_of_btc_stolen > 0.0000001:
        return 200
    else:
        return 500

def mining_asic_sell_price(mining_power, fraction_of_btc_stolen, sell_machines_time,
                           discount_rate):
    future_utility_adjustment = 1
    if discount_rate < 1:
        future_utility_adjustment = (1 - discount_rate ** (asic_recuperation_period + 1)) \
                                    / (1 - discount_rate)
    return mining_power * block_reward * blocks_per_period * \
           btc_to_usd_exchange_rate(sell_machines_time, fraction_of_btc_stolen) * \
           future_utility_adjustment
