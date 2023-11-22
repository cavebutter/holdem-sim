import src.holdem_sim.simulation as s
from prettytable import PrettyTable


def single_hand_eval(hand, board):
    """
    Simulate the odds of each possible final hand, given a player's hand and board.
    Returns a PrettyTable with the results.

    Parameters:
    - hand (list): A list of two strings representing the player's hand.
    - board (list): A list of strings representing the cards on the board.

    Returns:
    - return_text (str): A string containing the odds of different final hands after running simulations.
    """
    board_str = ''
    for card in board:
        board_str += card + ' '
    sim = s.simulation_one_player(hand, board)
    hc_pct = s.percent(sim[1], sim[0])
    hc_ratio = s.ratio(sim[1], sim[0])
    pair_pct = s.percent(sim[2], sim[0])
    pair_ratio = s.ratio(sim[2], sim[0])
    two_pair_pct = s.percent(sim[3], sim[0])
    two_pair_ratio = s.ratio(sim[3], sim[0])
    three_ok_pct = s.percent(sim[4], sim[0])
    three_ok_ratio = s.ratio(sim[4], sim[0])
    straight_pct = s.percent(sim[5], sim[0])
    straight_ratio = s.ratio(sim[5], sim[0])
    flush_pct = s.percent(sim[6], sim[0])
    flush_ratio = s.ratio(sim[6], sim[0])
    boat_pct = s.percent(sim[7], sim[0])
    boat_ratio = s.ratio(sim[7], sim[0])
    quads_pct = s.percent(sim[8], sim[0])
    quads_ratio = s.ratio(sim[8], sim[0])
    strt_flush_pct = s.percent(sim[9], sim[0])
    strt_flush_ratio = s.ratio(sim[9], sim[0])

    hole_card_str = hand[0] + ' ' + hand[1]

    table = PrettyTable()
    table.field_names = ['Hole Cards', 'Board']
    table.add_row([hole_card_str, board_str])

    odds = PrettyTable()
    odds.add_column('Best Final Hand',
                    ['High Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House',
                     'Four of a Kind',
                     'Straight Flush'])
    odds.add_column('% Prob',
                    [hc_pct, pair_pct, two_pair_pct, three_ok_pct, straight_pct, flush_pct, boat_pct, quads_pct,
                     strt_flush_pct])
    odds.add_column('Odds',
                    [hc_ratio, pair_ratio, two_pair_ratio, three_ok_ratio, straight_ratio, flush_ratio, boat_ratio,
                     quads_ratio, strt_flush_ratio])

    return_text = "We ran your hand and board 100,000 times.  Here's the odds:\n" + table.get_string() + "\n" + odds.get_string()
    return return_text


def multi_hand_eval(hole_one, opponents, board=[], sims=10000):
    """
    Calculates the win percentage of the hero's hand in a multiplayer poker game.

    Parameters:
        hole_one (str): The hero's first hole card.
        opponents (List[str]): The list of opponents' hole cards.
        board (List[str], optional): The community cards on the board. Defaults to an empty list.
        sims (int, optional): The number of simulations to run. Defaults to 10000.

    Returns:
        str: A formatted string representing the win percentage of the hero's hand.
    """
    sim = s.simulation_multiplayer(hole_one, board, opponents=opponents, sims=sims)
    win_pct = s.percent(sim[0].wins, 10000)
    return_text = f"Hero's hand will win {win_pct}% of the time."
    return return_text

def hand_and_win_prob(hand, board, opponents, sims=10000):
    """
    Combines single_hand_eval and multi_hand_eval into one function.

    :param hand:
    :param board:
    :param opponents:
    :param sims:
    :return:
    """
    foo = single_hand_eval(hand, board)
    bar = multi_hand_eval(hand, opponents, board, sims)
    return_text = foo + "\n" + bar
    return return_text