import random
from collections import Counter
from dataclasses import dataclass

CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
RANK_VALUE = dict(zip(RANKS, CARD_VALUES))
VALUE_RANK = dict(zip(CARD_VALUES, RANKS))
SUITS = ['c', 'd', 'h', 's']
HAND_VALUES = {'hc': 1,
               'pair': 2,
               '2pair': 3,
               '3ok': 4,
               'straight': 5,
               'flush': 6,
               'boat': 7,
               '4ok': 8,
               'straight_flush': 9
               }

HAND_REGISTRY = []

#####     CLASSES     #####

@dataclass
class Card:
    """
    A playing card.

    Cards are instantiated with a two-character string indicating rank and suit of the card.
    """
    def __init__(self, card_str):
        """
        Initializing a Card.

        Rank is the first character in passed string. (2-9, T, J, Q, K, A)
        Suit is the second character in passed string (c, d, h. s)
        Value is derived from the value corresponding to rank key in RANK_VALUE dict

        Parameters
        -----------
        card_str : str
            Two character string - Rank suit
        """
        self.rank = str(card_str[0])
        self.suit = card_str[1]
        self.name = self.rank + self.suit
        self.value = RANK_VALUE[self.rank]

    def __str__(self):
        return self.name


    def __getitem__(self, item):
        if item == 'rank':
            return self.rank
        elif item == 'suit':
            return self.suit
        elif item == 'name':
            return self.name
        elif item == 'value':
            return self.value


@dataclass()
class Hand:
    def __init__(self, type, high_value, low_value = 0, kicker=0):
        """
        A five-card poker hand.
        value refers to the value of the hand itself and is derived from the value associated with the type key in HAND_VALUES dict
        high_rank, low_rank, kicker_rank are derived from the values of the high_value, low_value, and kicker keys in the VALUE_RANK dict.

        Parameters
        ----------
        type : str
            name of hand (e.g. pair)
        high_value : int
            the value of high card in straight or flush, the set in full house, the top pair in 2pair, etc
        low_value : int
            default = 0. the value of the next highest card in the hand.  The kicker.
        kicker : int
            default = 0. the value of the next highest card in the hand.  Yes, this is confusing.
        """
        if kicker in CARD_VALUES:
            kicker_rank = VALUE_RANK[kicker]
        else:
            kicker_rank = 0
        if low_value in CARD_VALUES:
            low_rank = VALUE_RANK[low_value]
        else:
            low_rank = 0
        self.type = type
        self.hand_value = HAND_VALUES[type]
        self.kicker = kicker
        self.kicker_rank = kicker_rank
        self.high_value = high_value
        self.high_rank = VALUE_RANK[self.high_value]
        self.low_value = low_value
        self.low_rank = low_rank

    def __str__(self):
        return self.type + '-' + self.high_rank

    def __getitem__(self, item):
        if item == 'type':
            return self.type
        elif item == 'hand_value':
            return self.high_value
        elif item == 'kicker':
            return self.kicker
        elif item == 'kicker_rank':
            return self.kicker_rank
        elif item == 'high_value':
            return self.high_value
        elif item == 'high_rank':
            return self.high_rank
        elif item == 'low_value':
            return self.low_value
        elif item == 'low_rank':
            return self.low_rank


class Deck(list):
    """
    A deck of Cards.

    Instantiated by the function generate_deck().  Behaves like a list with a few additional methods specific to
    playing cards.
    """
    def __init__(self, deck):
        self.deck = deck

    def __getitem__(self, item):
        return self.deck[item]

    def __iter__(self):
        for elem in self.deck:
            yield elem

    def __len__(self):
        return len(self.deck)

    def deal_card(self):
        """Select a random card from the deck.  Return the card and the deck with the card removed

        Returns
        -------
        card : Card
        self : Deck

        Examples:
        ---------
        card, deck = deck.deal_card()
        """
        i = random.randint(0, len(self)-1)
        card = self[i]
        self.deck.pop(i)
        return card, self

    def update_deck(self, card):
        """
        Remove passed card from deck

        Parameters
        ----------
        card : Card

        Returns
        -------
        self : Deck
        """
        deck_names = [card.name for card in self.deck]
        if isinstance(card, Card):
            card_name = card.name
        else:
            card_name = card
        deck_idx = deck_names.index(card_name)
        self.deck.pop(deck_idx)


#####     USEFUL FUNCTIONS     #####

def register(func):
    """Add a function to the hand register"""
    HAND_REGISTRY.append(func)
    return func


def make_card(input_list):
    """
    Input_list is either a list of Card objects or string Objects.  If Cards, return the cards.
    If string, convert to Card and return

    Parameters
    -----------
    input_list : list
        Can be either a list of card strings or Card objects.  If strings, they are converted to Cards and returned.
        If Cards, input_list is returned unchanged.

    Returns
    --------
    card_list : list
        list of newly created Card objects
    or
    input_list : list
       unchanged list of Card objects

    Examples
    --------
    list_of_Card_objects = make_card(list_of_strings)
    """
    if len(input_list) == 0:
        return input_list
    elif isinstance(input_list[0], Card):
        return input_list
    else:
        card_list = [Card(card) for card in input_list]
        return card_list


def generate_deck():
    """
    Create a full deck of cards.

    Returns
    -------
    deck : Deck
        list-like object of 52 Card objects

    Examples
    --------
    mydeck = generate_deck()

    """
    deck = []
    for rank in RANKS:
        for suit in SUITS:
            card_str = rank + suit
            _card = Card(card_str)
            deck.append(_card)
    deck = Deck(deck)
    return deck


#####     POKER     #####
def find_multiple(hand, board, n=2):
    """
    Is there a pair, three of a kind, four of a kind?

    Checks a passed hand, board, and type of multiple (e.g. pair, three of a kind, four of a kind) for the existence
    of that type of multiple.  If that type of multiple does not exist, False is returned.  If it does, a Hand object
    is returned with high_value, low_value, and kicker values.

    Parameters
    -----------
    hand : list
        list of either Cards or card strings
    board : list
        list of either Cards or card strings
    n : int
        type of multiple (2 for pair, 3 for three of a kind, 4 for four of a kind)
    """
    hand = make_card(hand)
    board = make_card(board)
    multiple = False
    multiple_hand = None
    total_hand = hand + board
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in set(values):
        if c[value] == 2 and n == 2:
            multiple = True
            hand_type = 'pair'
            high_value = value
            low_value = max([value for value in values if value != high_value])
            kicker = max([value for value in values if value not in [high_value, low_value]])
            multiple_hand = Hand(hand_type, high_value, low_value=low_value, kicker=kicker)
            return multiple_hand
        elif c[value] == 3 and n == 3:
            multiple = True
            hand_type = '3ok'
            high_value = value
            low_value = max([foo for foo in values if foo != high_value])
            kicker = max([bar for bar in values if bar not in [high_value, low_value]])
            multiple_hand = Hand(hand_type, high_value, low_value=low_value, kicker=kicker)
            return multiple_hand
        elif c[value] == 4 and n == 4:
            multiple = True
            hand_type = '4ok'
            high_value = value
            low_value = max([value for value in values if value != high_value])
            multiple_hand = Hand(hand_type, high_value, low_value=low_value)
            return multiple_hand
    return multiple


def evaluate_straight(values):
    """
    Evaluates a list of card values to determine whether there are 5 consecutive values.

    List of integers are evaluated from high to low to see if there are 5 consecutive values.  Low straights are
    accounted for by adding 14 at the low end of the list.  If 5 consecutive values are present, True is returned along
    with a list of 5 consecutive values.  Else, False is returned along with an empty list.

    A component of find_straight().  Not meant for independent use.

    Parameters
    ----------
    values : list

    Returns:
    --------
    straight : bool
    straight_hand_values : list
    """
    straight = False
    count = 0
    straight_hand_values = []
    sranks = [bit for bit in reversed(range(2, 15))]
    sranks.append(14)
    for rank in sranks:
        if rank in values:
            count += 1
            straight_hand_values.append(rank)
            if count == 5:
                straight = True
                return straight, straight_hand_values
        else:
            count = 0
            straight_hand_values = []
    return straight, straight_hand_values


@register
def find_straight_flush(hand, board):
    """
    Find a straight flush in a given hand/board combination.

    Hand and board are first evaluated to find a flush.  If flush, then the flush-suited cards are evaluated for
    a straight.  If straight, then return a straight_flush Hand.  If either are false, then False is returned.

    Parameters
    -----------
    hand : list
        list of Cards or card strings
    board : list
        list of Cards or card strings
    """
    hand = make_card(hand)
    board = make_card(board)
    straight_flush = False
    flush = find_flush(hand, board)
    if flush:
        total_hand = hand + board
        total_hand = [card for card in total_hand]
        hand_suits = [card.suit for card in total_hand]
        c = Counter(hand_suits)
        flush_suit = c.most_common(1)[0][0]
        flush_hand = [card.value for card in total_hand if card.suit == flush_suit]
        straight_flush, straight_hand = evaluate_straight(flush_hand)
        if straight_flush:
            high_value = max(straight_hand)
            hand_type = 'straight_flush'
            straight_flush_hand = Hand(hand_type,high_value)
            return straight_flush_hand
        else:
            return straight_flush
    else:
        return straight_flush


@register
def find_quads(hand, board):
    """
    Calls find_multiple() to find four of a kind.

    Parameters
    -----------
    hand : list
    board : list

    Returns
    -------
    bool | Hand

    """
    quads = find_multiple(hand, board, n=4)
    return quads


@register
def find_full_house(hand, board):
    """
    Is there a full house?

    Hand and board are first evaluated for 3 of a kind.  If three of a kind is present, the remaining cards are
    evaluated for a pair.  If both three of a kind and a pair are present, then a 'boat' Hand is returned.  Else,
    False is returned.

    Parameters
    ----------
    hand : list
        list of Cards or strings
    board : list
        list of Cards or strings
    """
    hand = make_card(hand)
    board = make_card(board)
    boat = False
    boat_hand = None
    total_hand = hand + board
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in set(values):
        if c[value] == 3:
            high_value = value
            c.pop(value)
            for value in set(values):
                if c[value] > 1:
                    low_value = value
                    kicker = max([value for value in values if value != high_value and value != low_value])
                    boat_hand = Hand('boat', high_value, low_value=low_value, kicker=kicker)
                    boat = True
                    return boat_hand
    return boat


@register
def find_flush(hand, board):
    """
    Does any combination of 5 cards in hand or on board amount to 5 of the same suit

    Count the SUITS in the passed cards.  If the count of any suit equals 5, then a flush hand is returned.  If not,
    False is returned.

    Parameters
    ----------
    hand : list
        list of Cards or strings
    board : list
        list of Cards or strings
    """
    hand = make_card(hand)
    board = make_card(board)
    total_hand = hand + board
    total_hand_suits = [card.suit for card in total_hand]
    flush = False
    c = Counter(total_hand_suits)
    for suit in total_hand_suits:
        if c[suit] >= 5:
            flush = True
    if flush:
        flush_cards = [card for card in total_hand if card.suit == c.most_common(1)[0][0]]
        high_value = max([card.value for card in flush_cards])
        flush_hand = Hand('flush', high_value)
        return flush_hand
    else:
        return flush


@register
def find_straight(hand, board):
    """
    Find a straight in a given hand/board combination

    Passed hand and board are evaluated, high to low, to determine whether there are 5 consecutive cards.  If there
    are 5 consecutive cards, a straight Hand is returned.  If not, False is returned.

    Parameters
    -----------
    hand : list
        list of Cards or strings
    board : list
        list of Cards or strings
    """
    hand = make_card(hand)
    board = make_card(board)
    straight = False
    straight_hand = None
    high_value = 2
    reqd_hand_size = 5  # required hand size gives us some flexibility at the cost of more lines.  could be more efficient if we say 'if len(values)<5'
    total_hand = hand + board
    values = [*set(card.value for card in total_hand)]
    slices = len(values) - reqd_hand_size
    if slices < 0:
        return straight
    else:
        straight, straight_hand_values = evaluate_straight(values)
        if straight:
            hand_type = 'straight'
            if 14 in straight_hand_values:  # all([5,14]) does not work here so using nested ifs.
                if 5 in straight_hand_values:
                    high_value = 5
            else:
                high_value = max(straight_hand_values)
            straight_hand = Hand(hand_type, high_value)
            return straight_hand
        else:
            return straight


@register
def find_trips(hand, board):
    """
    Calls find_multiple() to find three of a kind.

    Parameters
    -----------
    hand : list
    board : list

    Returns
    -------
    bool | Hand

    """
    trips = find_multiple(hand, board, n=3)
    return trips


@register
def find_two_pair(hand, board):
    """
    Is there two-pair?

    Hand and board are evaluated to determine whether there is a pair present.  If so, the remaining cards are
    evaluated to determine if there is another pair.  If so, a '2pair' Hand is returned.  If not, False is returned.

    Parameters
    -----------
    hand : list
    board : list

    Returns
    -------
    bool | Hand
    """
    hand = make_card(hand)
    board = make_card(board)
    two_pair = False
    # two_pair_hand = None
    total_hand = hand + board
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in values:
        if c[value] > 1:
            pair1 = Hand('pair', value)
            c.pop(value)
            for value in values:
                if c[value] > 1:
                    pair2 = Hand('pair', value)
                    kicker = max([value for value in values if value != pair1.high_value and value != pair2.high_value])
                    two_pair_hand = Hand('2pair', max(pair1.high_value, pair2.high_value), low_value=min(pair1.high_value, pair2.high_value), kicker=kicker)
                    two_pair = True
                    return two_pair_hand
    return two_pair


@register
def find_pair(hand, board):
    """
    Calls find_multiple() to find a pair.

    Parameters
    -----------
    hand : list
    board : list

    Returns
    -------
    bool | Hand

    """
    pair = find_multiple(hand, board, n=2)
    return pair


@register
def find_high_card(hand, board):
    """
    Create a 'high card' hand.

    Passed hand and board evaluated and a high card hand is returned with the highest value card as high_value,
    second as low, third as kicker.

    Parameters
    -----------
    hand : list
    board : list

    Returns
    -------
    high_card_hand : Hand
    """
    hand = make_card(hand)
    board = make_card(board)
    total_hand = hand + board
    total_hand_values = [card.value for card in total_hand]
    total_hand_values.sort()
    high_value = total_hand_values[-1]
    low_value = total_hand_values[-2]
    kicker = total_hand_values[-3]
    high_card_hand = Hand('hc', high_value,low_value=low_value, kicker=kicker)
    return high_card_hand
