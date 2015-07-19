"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    def __init__(self):
        
        self.total_cookies = 0.0
        self.current_cookies = 0.0
        self.current_time = 0.0
        self.current_cps = 1.0
        self.history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return_string_1 = "Total cookies: " + str(self.total_cookies)
        return_string_2 = "Current cookies: " + str(self.current_cookies)
        return_string_3 = "Time: " + str(self.current_time)
        return_string_4 = "CPS: " + str(self.current_cps)
        all_strings = return_string_1 + "\n" + return_string_2 + "\n" + \
            return_string_3 + "\n" + return_string_4 + "\n"
        return all_strings
    
    def get_cookies(self):
        """
        Returns current number of cookies as float
        (not total number of cookies)
        """
        return self.current_cookies
    
    def get_cps(self):
        """
        Get current CPS as float
        """
        return self.current_cps
    
    def get_time(self):
        """
        Get current time as float
        """
        return self.current_time
    
    def get_history(self):
        """
        Return history list -- a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]
        """
        return self.history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies) as rounded float
        """
        time_until = 0.0
        if self.current_cookies < cookies:
            cookie_delta = cookies - self.current_cookies
            time_until = math.ceil(cookie_delta/ self.current_cps)
        return time_until
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        Do nothing if time <= 0.0
        
        """
        if time > 0.0:
            self.current_time += time
            additional_cookies = time * self.current_cps
            self.current_cookies += additional_cookies
            self.total_cookies += additional_cookies
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Do nothing if you cannot afford the item
        """
        if self.current_cookies >= cost:
            self.current_cookies -= cost
            self.current_cps += additional_cps
            state_tuple = (self.current_time, item_name, cost, 
                self.total_cookies)
            self.history.append(state_tuple)
    
def simulate_clicker(build_info, duration, strategy):
    """
    Runs a Cookie Clicker game for the given duration with 
    the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clone = build_info.clone()
    CS = ClickerState()
    time_to_wait = 0.0
    while CS.get_time() <= duration:
        time_left = duration - CS.get_time()
        item = strategy(CS.get_cookies(), CS.get_cps(), CS.get_history(), 
            time_left, clone)
        if item == None:
            CS.wait(time_left)
            break
        else:
            item_cost = clone.get_cost(item)
            item_cps = clone.get_cps(item)
            if item_cost <= CS.get_cookies():
                time_to_wait = 0.0
            else:
                time_to_wait = CS.time_until(item_cost)
            if duration < (CS.get_time() + time_to_wait):
                time_left = duration - CS.get_time()
                CS.wait(time_left)
                break
            CS.wait(time_to_wait)
            CS.buy_item(item, item_cost, item_cps)
            clone.update_item(item)
    return CS

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always picks the Cursor.
    """
    cursor_cost = build_info.get_cost("Cursor")
    possible_cookies = cookies + cps * time_left
    if possible_cookies >= cursor_cost:
        return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always returns None

    This is a pointless strategy that will never buy anything, but 
    can be used to debug simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    all_items = build_info.build_items()
    cheapest_item = None
    cheapest_item_cost = build_info.get_cost(all_items[0])
    possible_cookies = cookies + cps * time_left
    for item in all_items:
        item_cost = build_info.get_cost(item)
        if item_cost <= possible_cookies:
            if item_cost < cheapest_item_cost:
                cheapest_item = item
                cheapest_item_cost = item_cost
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    all_items = build_info.build_items()
    expensive_item = None
    max_item_cost = build_info.get_cost(all_items[0])
    possible_cookies = cookies + cps * time_left
    for item in all_items:
        item_cost = build_info.get_cost(item)
        if item_cost <= possible_cookies:
            if item_cost > max_item_cost:
                expensive_item = item
                max_item_cost = item_cost
    return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    My best strategy thus far.
    """
    all_items_ = build_info.build_items()
    all_items = list(all_items_)
    best_item = None
    possible_cookies = cookies + cps * time_left
    min_score = float('inf')
    for item in all_items:
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        if item_cost <= possible_cookies:
            score_weight1 = float(1.0 / item_cps)
            score_weight2 = float(1.0 / cps)
            score = item_cost * (score_weight1 + .90 * score_weight2)
            if score < min_score:
                best_item = item
                min_score = score
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Runs a simulation for the given time with the given strategy. Prints final
    strategy statistics to the console and graphs the time versus total cookies.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, " Strategy:", state

    # Plot total cookies over time
    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [
        history], True)

def run():
    """
    Run the simulator for all the strategies.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()