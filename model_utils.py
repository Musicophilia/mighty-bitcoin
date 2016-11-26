# Functions which Brandon will implement
from __future__ import division
import math

blocks_per_period = 144
asic_recuperation_period = 250
block_reward = 12.5

def btc_to_usd_exchange_rate(time, fraction_of_btc_stolen):
    # Attack time, if applicable, is 0
    # This function is modeled after tanh.
    # After an attack the btc-to-usd rate drops dramatically.
    # Assuming no further attacks, the rate slowly recovers.
    # |   _ _ __
    # |  /
    # | /
    # |/
    # notice the free fall and then tanh(>=0)
    default_btc_to_usd_rate = 730 # current bitcoin rate
    if fraction_of_btc_stolen == 0.0:
        return default_btc_to_usd_rate # assume rate is constant
    else:
        # Crude assumption: rate decreases by (k * fraction_of_btc_stolen) %.
        k = 1.0 # constant factor multiplied to decrease rate.
        lower_bound_rate = (1.0 - k*fraction_of_btc_stolen) * default_btc_to_usd_rate
        # Crude assumption: rate can __fully__ recover.
        upper_bound_rate = 1.0 * default_btc_to_usd_rate
        # Since attack time = 0, any time post attack is positive.
        # And so, second derivative of rate is negative.
        # This ranges from 0 to 1.
        # Modifying tanh to account for fraction_of_btc_stolen.
        # The higher the fraction_of_btc_stolen, the longer it takes to recover.
        tanh = math.tanh((1 - fraction_of_btc_stolen) * time)
        delta_rate = tanh * (upper_bound_rate - lower_bound_rate)
        new_btc_to_usd = lower_bound_rate + delta_rate
        return new_btc_to_usd

def mining_asic_sell_price(mining_power, fraction_of_btc_stolen, sell_machines_time,
                           discount_rate):
    future_utility_adjustment = 1
    if discount_rate < 1:
        future_utility_adjustment = (1 - discount_rate ** (asic_recuperation_period + 1)) \
                                    / (1 - discount_rate)
    return mining_power * block_reward * blocks_per_period * \
           btc_to_usd_exchange_rate(sell_machines_time, fraction_of_btc_stolen) * \
           future_utility_adjustment
