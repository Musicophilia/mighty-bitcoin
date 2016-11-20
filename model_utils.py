# Functions which Brandon will implement

def btc_to_usd_exchange_rate(time, attack_happened):
    # time is absolute time
    # TODO: Replace with something that makes sense
    if attack_happened:
        return 200
    else:
        return 500

def get_sell_price_per_machine(btc_to_usd_machine, sell_machines_time):
    # TODO: Replace with something that makes sense
    return btc_to_usd_machine * sell_machines_time
