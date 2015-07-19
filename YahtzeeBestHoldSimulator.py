"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of outcomes of 
    given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute and return the maximal score as integer for a Yahtzee hand according 
    to the upper section of the Yahtzee score card.

    hand: full yahtzee hand
    """
    scores_dict = {}
    if type(hand) == int or len(hand) == 0:
        raise TypeError("The length of hand must be > 0 to calculate a score")
    elif len(hand) >= 1:
        for val in hand:
            if scores_dict.get(val) != None:
                scores_dict[val] += val
            else:
                scores_dict[val] = val
        max_score = max(scores_dict.values())
        return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [side for side in range(1, num_die_sides + 1)]
    all_sequences = gen_all_sequences(outcomes, num_free_dice)
    
    seq_occurr = {}
    for seq in all_sequences:
        sort_seq = tuple(sorted(seq))
        if seq_occurr.get(sort_seq) == None:
            seq_occurr[sort_seq] = 1
        else:
            seq_occurr[sort_seq] += 1

    all_outcomes = len(all_sequences)
    expected_val = 0.0

    for seq in seq_occurr.keys():
        prob_seq = float(seq_occurr[seq]) / float(all_outcomes)
        seq = list(seq)
        for item in held_dice:
            seq.append(item)
        seq = tuple(sorted(seq))
        expected_val += prob_seq * score(seq)

    return expected_val
        
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    sorted_all_seq = []
    for length in range(1, len(hand) + 1):
        all_seq = gen_all_sequences(hand, length)
        for seq in all_seq:
            sorted_all_seq.append(tuple(sorted(seq)))
    set_all_seq = set(sorted_all_seq)
    holds = list(set_all_seq)
    removed_seq = False
    for seq in set_all_seq:
        temp = list(hand)
        for val in seq:
            if removed_seq == False:
                if val not in temp:
                    holds.remove(seq)
                    removed_seq = True
                else:
                    temp.remove(val)
        removed_seq = False
    set_holds = set(holds)
    set_holds.add(())
    return set_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_score = 0.0
    hold_optimal = ()
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        expected_val = expected_value(hold, num_die_sides, num_free_dice)
        if expected_val > max_score:
            max_score = expected_val
            hold_optimal = hold
    return (max_score, hold_optimal)

def best_move(hand):
    """
    Compute the dice to hold and expected score for an example hand

    hand: Yahtzee hand of 5 cards represented as a tuple of 5 integers [1, 6]
    """
    num_die_sides = 6
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, \
        "with expected score", hand_score
    
best_move((1, 1, 1, 5, 6))
 
    



