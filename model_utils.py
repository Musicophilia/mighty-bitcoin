# Functions which Brandon will implement

def btc_to_usd_exchange_rate(time, fraction_of_btc_stolen):
    # time is absolute time
    # TODO: Replace with something that makes sense
    if fraction_of_btc_stolen > 0.0000001:
        return 200
    else:
        return 500

def get_sell_price_per_machine(btc_to_usd_machine, sell_machines_time):
    # TODO: Replace with something that makes sense
    return btc_to_usd_machine * sell_machines_time
