import poker_functions as p
from fractions import Fraction
from collections import Counter


class Player:
    def __init__(self, number, cards=[]):
        if len(cards) > 0:
            cards = p.make_card(cards)
        else:
            cards = []
        self.number = number
        self.cards = cards
        self.hand = None
        self.starting_cards = None
        self.wins = 0

    def __str__(self):
        return "player_" + str(self.number)

def dedupe(board):
    duplicate = False
    c = Counter(board)
    for card in board:
        if c[card] > 1:
            duplicate = True
            return duplicate
    return duplicate


def validate_card(check):
    """Detect invalid cards in a passed collection"""
    valid = True
    deck = p.generate_deck()
    valid_cards = [card.name for card in deck]
    for card in check:
        if card not in valid_cards:
            valid = False
            return valid
    return valid


def convert_and_update(deck, cards):
    if len(cards) == 0:
        return deck, cards
    else:
        cards = p.make_card(cards)
        for card in cards:
            deck.update_deck(card)
        return deck, cards

#####     SIMULATIONS     #####
def evaluate_hand(hole_cards, flop=[], turn=[], river=[]):
    board = flop + turn + river
    hand = None
    if len(hole_cards + board) < 5:
        return hand
    else:
        for func in p.HAND_REGISTRY:
            func = func(hole_cards, board)
            if not func:
                continue
            else:
                return func


def score_game(contestants):
    #  TODO make this more elegant by functionizing repeated code.
    """Application will determine the highest hand, including low and kicker for each player in player_list"""
    high = ['flush', 'straight', 'straight_flush']
    kick = ['4ok']
    hi_lo = ['boat']
    hi_lo_kick = ['2pair', 'hc', '3ok', 'pair']
    high_hand = max(contestants, key=lambda x: x.hand.hand_value)  # contestant with highest hand
    same_high_hand = [player for player in contestants if player.hand.hand_value == high_hand.hand.hand_value]
    if len(same_high_hand) == 1:
        same_high_hand[0].wins += 1
        return contestants
    elif high_hand.hand.type in high:
        high_card = max(same_high_hand, key=lambda x: x.hand.high_value)
        same_high_card = [player for player in same_high_hand if player.hand.high_value == high_card.hand.high_value]
        if len(same_high_card) == 1:
            high_card.wins += 1
            return contestants
        else:
            return contestants
    elif high_hand.hand.type in hi_lo:
        over = max(same_high_hand, key=lambda x: x.hand.high_value) # Highest pair in hand
        same_over = [player for player in same_high_hand if player.hand.high_value == over.hand.high_value]
        if len(same_over) == 1:
            over.wins += 1
            return contestants
        else:
            under = max(same_over, key=lambda x: x.hand.low_value) # lowest pair in hand
            same_under = [player for player in same_over if player.hand.low_value == under.hand.low_value]
            if len(same_under) == 1:
                under.wins += 1
                return contestants
            else:
                return contestants
    elif high_hand.hand.type in hi_lo_kick:
        over = max(same_high_hand, key=lambda x: x.hand.high_value)  # Highest pair in hand
        same_over = [player for player in same_high_hand if player.hand.high_value == over.hand.high_value]
        if len(same_over) == 1:
            over.wins += 1
            return contestants
        else:
            under = max(same_over, key=lambda x: x.hand.low_value)  # lowest pair in hand
            same_under = [player for player in same_over if player.hand.low_value == under.hand.low_value]
            if len(same_under) == 1:
                under.wins += 1
                return contestants
            else:
                kicker = max(same_under, key=lambda x: x.hand.kicker)
                same_kicker = [player for player in same_under if player.hand.kicker == kicker.hand.kicker]
                if len(same_kicker) == 1:
                    kicker.wins += 1
                    return contestants
                else:
                    return contestants
    elif high_hand.hand.type in kick:
        low_val = max(same_high_hand, key=lambda x: x.hand.low_value)
        same_low_val = [player for player in same_high_hand if player.hand.low_value == low_val.hand.low_value]
        if len(same_low_val) == 1:
            low_val.wins += 1
            return contestants
        else:
            return contestants


def simulation_one_player(hole, flop=[], turn=[], river=[], sims=100000):
    full_board = 7 # number of cards required to run sim
    passed_cards = len(hole) + len(flop) + len(turn) + len(river)
    passed_flop = [item for item in flop]
    high_cards = 0
    pairs = 0
    two_pairs = 0
    trips = 0
    straights = 0
    flushes = 0
    boats = 0
    quads = 0
    straight_flushes = 0
    invalid = 0
    for i in range(sims):
        deck = p.generate_deck()
        deck, hole = convert_and_update(deck, hole)
        deck, flop = convert_and_update(deck, flop)
        deck, turn = convert_and_update(deck, turn)
        deck, river = convert_and_update(deck, river)
        j = full_board - passed_cards
        for k in range(j):  # Add additional cards to make a full board of 7
            deal, deck = deck.deal_card()
            flop.append(deal)  # Adding to flop because it shouldn't matter, will revert flop back at end of loop
        hand = evaluate_hand(hole, flop, turn, river)
        if hand.type == 'straight_flush':
            straight_flushes += 1
        elif hand.type == '4ok':
            quads += 1
        elif hand.type == 'boat':
            boats += 1
        elif hand.type == 'flush':
            flushes += 1
        elif hand.type == 'straight':
            straights += 1
        elif hand.type == '3ok':
            trips += 1
        elif hand.type == '2pair':
            two_pairs += 1
        elif hand.type == 'pair':
            pairs += 1
        elif hand.type == 'hc':
            high_cards += 1
        else:
            invalid += 1
        i += 1
        flop = [item for item in passed_flop] # Reset flop back to original
    return sims, high_cards, pairs, two_pairs, trips, straights, flushes, boats, quads, straight_flushes


def simulation_multiplayer(hole_one, hole_two=[], hole_three=[], hole_four=[], hole_five=[], hole_six=[],
                           flop = [], turn = [], river = [], opponents=2, sims=10000):
    contestant_hands = [hole_one, hole_two, hole_three, hole_four, hole_five, hole_six]
    contestants = []
    flop = p.make_card(flop)
    turn = p.make_card(turn)
    river = p.make_card(river)
    passed_flop_stable = [card for card in flop]
    for n in range(opponents):
        player_name = 'opponent' + str(n+1)
        player_name = Player(n, contestant_hands[n])
        contestants.append(player_name)
    i = 0
    passed_board = len(flop) + len(turn) + len(river)
    full_board = 5
    k = full_board - passed_board
    for i in range(sims):
        deck = p.generate_deck()
        for contestant in contestants:  # TODO move assigning Player.starting_cards to init
            if len(contestant.cards) == 2:
                contestant.starting_cards = True
                for card in contestant.cards:
                    deck.update_deck(card)  # remove known hole cards from deck
            else:
                contestant.starting_cards = False
                hole_cards = []
                for j in range(2):
                    deal, deck = deck.deal_card()
                    hole_cards.append(deal)
                contestant.cards = hole_cards #  assign new hole cards if not passed
        for l in range(k):  # complete the board as needed
            deal, deck = deck.deal_card()
            flop.append(deal)
        for contestant in contestants:
            hand = evaluate_hand(contestant.cards, flop, turn, river)
            contestant.hand = hand
        #  Compare hand values in contestants
        contestants = score_game(contestants)
        i += 1
        #  Revert to starting state
        flop = [card for card in passed_flop_stable]
        for contestant in contestants:
            if contestant.starting_cards is False:
                contestant.cards = []
        hole_cards = []
    return contestants



#  TODO for single and mult: find and return most likely hand.  Return number of outs and odds.

#####     MATH     #####
def percent(hits, sims):
    percent = round((hits / sims) * 100,0)
    return percent

def ratio(hits, sims):
    """Return a ratio (e.g. 3:5) for two input numbers"""
    percent = round((hits / sims),2)
    fraction = str(Fraction(percent).limit_denominator())
    fraction = fraction.replace('/', ':')
    return fraction


#####     REFERENCE     #####
outs = {'1':('46:1','45:1',"22:1"),
        '2':('22:1','22:1','11:1'),
        '3':('15:1', '14:1', '7:1'),
        '4':('11:1','10:1','5:1'),
        '5':('8.5:1', '8:1','4:1'),
        '6':('7:1','7:1','3:1'),
        '7':('6:1','6:1','2.5:1'),
        '8':('5:1','5:1','2.5:1'),
        '9':('4:1','4:1','2:1'),
        '10':('3.5:1','3.5:1','1.5:1'),
        '11':('3.3:1','3.2:1','1.5:1'),
        '12':('3:1','3:1','1.2:1'),
        }


rank_value = p.rank_value