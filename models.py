from __future__ import division
import math

from model_utils import *
########################################################################################################################


class utility_model(object):
    def __init__(self, btc_f_stolen = 0.05, btc_f_owned_0 = 0.10, total_btc = 16000000,
            attack_time = 0, withdraw_btc_delta = 1, sell_machines_delta = 2,
            mining_power = 0.2, discount_rate = 1.0):
        assert 0 <= btc_f_stolen + btc_f_owned_0 < 1        
        self.btc_f_stolen = btc_f_stolen
        self.btc_f_owned_0 = btc_f_owned_0
        self.total_btc = total_btc
        self.attack_time = attack_time
        self.withdraw_btc_delta = withdraw_btc_delta
        self.sell_machines_delta = sell_machines_delta
        self.mining_power = mining_power
        self.discount_rate = discount_rate

    def _get_attack_value(self):
        btc_owned_post_attack = (self.btc_f_stolen + self.btc_f_owned_0) * self.total_btc
        btc_to_usd_withdraw = btc_to_usd_exchange_rate(self.attack_time + self.withdraw_btc_delta,
                                                       self.btc_f_stolen)
        btc_value_post_attack = btc_owned_post_attack * btc_to_usd_withdraw * \
                                math.pow(self.discount_rate, self.withdraw_btc_delta)

        sell_machines_time = self.attack_time + self.sell_machines_delta
        asic_price = mining_asic_sell_price(self.mining_power, self.btc_f_stolen, sell_machines_time,
                                            self.discount_rate)
        machine_sell_price_post_attack = asic_price * math.pow(self.discount_rate, self.sell_machines_delta)

        attack_value = btc_value_post_attack + machine_sell_price_post_attack
        return attack_value

    def _get_no_attack_value(self):
        btc_to_usd = btc_to_usd_exchange_rate(time=0, btc_f_stolen=0.0)
        btc_value = (self.btc_f_owned_0 * self.total_btc) * btc_to_usd

        asic_price = mining_asic_sell_price(mining_power=self.mining_power, btc_f_stolen=0.0,
                                            sell_machines_time=0, discount_rate=self.discount_rate)

        no_attack_value = btc_value + asic_price
        return no_attack_value


    def compute_attack_utility(self):
        attack_value = self._get_attack_value()
        no_attack_value = self._get_no_attack_value()

        utility = attack_value - no_attack_value
        return utility

def get_attack_utility():
    model = utility_model(btc_f_stolen = 0.05, btc_f_owned_0 = 0.10, total_btc = 16000000,
            attack_time = 0, withdraw_btc_delta = 1, sell_machines_delta = 2,
            mining_power = 0.2, discount_rate = 1.0)
    return model.compute_attack_utility()

if __name__ == "__main__":
    attack_utility = get_attack_utility()
    print attack_utility

