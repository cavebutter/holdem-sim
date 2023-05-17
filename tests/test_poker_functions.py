import pytest
import poker_functions


# valid card string
card_str1 = 'As'

# invalid card string
card_string2 = 'Of'

#  hand with kicker
new_hand = p.Hand('pair', 12, 11)

@pytest.fixture
def two_pair():
    # 2 Pair
    hand1 = ['As', '4c']
    flop1 = ['4d', 'Qh', 'Ts']
    turn1 = ['7h']
    river1 = ['Ad']
    board = flop1 + turn1 + river1
    return hand1, board


@pytest.fixture
def flush_one_pair():
    # Flush, 1 Pair
    hand2 = ['As', 'Ks']
    flop2 = ['4d', 'Kh', 'Ts']
    turn2 = ['7s']
    river2 = ['3s']
    board = flop2 + turn2 + river2
    return hand2, board


@pytest.fixture
def straight_no_pair_no_flush():
    # Straight, no pair, no flush
    hand3 = ['4s', '5d']
    flop3 = ['6c', '7s', '8h']
    turn3 = ['Jc']
    river3 = ['As']
    board = flop3 + turn3 + river3
    return hand3, board


@pytest.fixture
def three_of_a_kind():
    # 3 of a kind
    hand4 = ['As', 'Ac']
    flop4 = ['4d', 'Qh', 'Ts']
    turn4 = ['7h']
    river4 = ['Ad']
    board = flop4  + turn4 + river4
    return hand4, board


@pytest.fixture
def boat():
    # Full House
    hand5 = ['As', 'Ac']
    flop5 = ['4d', 'Qh', 'Ts']
    turn5 = ['4c']
    river5 = ['Ad']
    board = flop5 + turn5 + river5
    return hand5, board



@pytest.fixture
def straight_flush():
    # Straight flush
    hand6 = ['4s', '5s']
    flop6 = ['6s', '7s', '8s']
    turn6 = ['Jc']
    river6 = ['Ac']
    board = flop6 + turn6 + river6
    return hand6, board

@pytest.fixture
def non_seq_straight():
    # Straight, non-sequential
    hand7 = ['2c', '9s']
    flop7 = ['Jh', '6c', '3d']
    turn7 = ['4h']
    river7 = ['5s']
    board = flop7 + turn7 + river7
    return hand7, board


@pytest.fixture
def straight_five_card():
    # Straight, 5 card
    hand8 = ['2c', '2s']
    flop8 = ['6h', '3c', '3d']
    turn8 = ['4h']
    river8 = ['5s']
    board = flop8 + turn8 + river8
    return hand8, board

@pytest.fixture
def straight_six_card():
# Straight, 6 card
    hand = ['2c', '7s']
    flop9 = ['Jh', '3c', '6d']
    turn9 = ['4h']
    river9 = ['5s']
    board = flop9 + turn9 + river9
    return hand, board

#  Duplicated Card
hand10 = ['3c', 'As']
flop10 = ['3c', 'Jd', '9h']
turn10 = ['4s']
river10 = ['8s']


#  Invalid Card
hand11 = ['3c', 'As']
flop11 = ['9c', 'Jd', '9h']
turn11 = ['4s']
river11 = ['Ss']


@pytest.fixture
def wheel():
    #  Wheel
    hand12 = ['Ac', 'Td']
    flop12 = ['2c', '3h', 'Qs']
    turn12 = ['4s']
    river12 = ['5d']
    board = flop12 + turn12 + river12
    return  hand12, board


@pytest.fixture
def high_card():
    #  High Card
    hand13 = ['Td', '4c']
    flop13 = ['2c', '3h', 'Qs']
    turn13 = ['5d']
    river13 = ['9c']
    board = flop13 + turn13 + river13
    return hand13, board


@pytest.fixture
def quads():
    hand14 = ['4c', '4h']
    flop14 = ['4s', 'Ac', '9h']
    turn14 = ['8d']
    river14 = ['4d']
    board = flop14 + turn14 + river14
    return hand14, board

def test_card_init():
    card = p.Card(card_str1)
    assert type(card) == p.Card


def test_card_rank():
    card = p.Card(card_str1)
    assert card.rank == 'A'


def test_card_suit():
    card = p.Card(card_str1)
    assert card.suit == 's'


def test_card_value():
    card = p.Card(card_str1)
    assert card.value == 14


def test_card_name():
    card = p.Card(card_str1)
    assert card.name == 'As'


def test_deck_init():
    deck = p.generate_deck()
    assert type(deck) == p.Deck


def test_deck_contents():
    deck = p.generate_deck()
    assert type(deck[5]) == p.Card


def test_deck_size():
    deck = p.generate_deck()
    assert len(deck) == 52


def test_deal_card_1():
    """Ensures that the deal_card generates a Card object"""
    deck = p.generate_deck()
    card, deck = deck.deal_card()
    assert type(card) == p.Card


def test_deal_card_2():
    """Ensures that deal_card removes Card from deck"""
    deck = p.generate_deck()
    card, deck = deck.deal_card()
    assert len(deck) == 51


def test_update_deck_1():
    """Remove a passed card from Deck passed as string"""
    deck = p.generate_deck()
    deck.update_deck('Ks')
    cards = [card.name for card in deck]
    assert len(deck) == 51


def test_update_deck_2():
    """Remove a passed card from Deck passed as Card"""
    card = p.Card('Ks')
    deck = p.generate_deck()
    deck.update_deck(card)
    cards = [card.name for card in deck]
    assert len(deck) == 51


def test_update_deck_3():
    """Ensure specific passed card is removed from deck"""
    passed_card = p.Card('2c')
    deck = p.generate_deck()
    deck.update_deck(passed_card)
    cards = [card.name for card in deck]
    assert passed_card.name not in cards


def test_update_deck_4():
    """Ensure specific passed card string is removed from deck"""
    passed_card = '2c'
    deck = p.generate_deck()
    deck.update_deck(passed_card)
    cards = [card.name for card in deck]
    assert passed_card not in cards


def test_no_flush(two_pair):
    board = two_pair[1]
    hand = two_pair[0]
    flush = p.find_flush(hand, board)
    assert not flush


def test_flush_hand_value(flush_one_pair):
    board2 = flush_one_pair[1]
    hand = flush_one_pair[0]
    flush_hand = p.find_flush(hand, board2)
    assert flush_hand.high_value == 14


def test_flush_hand_type(flush_one_pair):
    board2 = flush_one_pair[1]
    hand = flush_one_pair[0]
    flush_hand = p.find_flush(hand, board2)
    assert flush_hand.type == 'flush'

def test_one_pair_type(flush_one_pair):
    board2 = flush_one_pair[1]
    hand = flush_one_pair[0]
    multiple_hand = p.find_multiple(hand, board2)
    assert multiple_hand.type == 'pair'


def test_one_pair_high_value(flush_one_pair):
    board2 = flush_one_pair[1]
    hand = flush_one_pair[0]
    multiple_hand = p.find_multiple(hand, board2)
    assert multiple_hand.high_value == 13


def test_one_pair_low_value(flush_one_pair):
    board2 = flush_one_pair[1]
    hand = flush_one_pair[0]
    multiple_hand = p.find_multiple(hand, board2)
    assert multiple_hand.low_value == 14


def test_one_pair_kicker_value(flush_one_pair):
    board2 = flush_one_pair[1]
    hand = flush_one_pair[0]
    multiple_hand = p.find_multiple(hand, board2)
    assert multiple_hand.kicker == 10

def test_not_one_pair(straight_no_pair_no_flush):
    board = straight_no_pair_no_flush[1]
    hand = straight_no_pair_no_flush[0]
    pair = p.find_pair(hand, board)
    assert not pair

def test_not_two_pair(straight_no_pair_no_flush):
    board3 = straight_no_pair_no_flush[1]
    hand3 = straight_no_pair_no_flush[0]
    two_pair = p.find_two_pair(hand3, board3)
    assert not two_pair

def test_two_pair_type(two_pair):
    board1 = two_pair[1]
    hand1 = two_pair[0]
    two_pair_hand = p.find_two_pair(hand1, board1)
    assert two_pair_hand.type == '2pair' and two_pair_hand.kicker_rank == 'Q'



def test_two_pair_high(two_pair):
    board1 = two_pair[1]
    hand1 = two_pair[0]
    two_pair_hand = p.find_two_pair(hand1, board1)
    assert two_pair_hand.high_value == 14


def test_two_pair_low(two_pair):
    board1 = two_pair[1]
    hand1 = two_pair[0]
    two_pair_hand = p.find_two_pair(hand1, board1)
    assert two_pair_hand.low_value == 4

def test_not_3ok(two_pair):
    board1 = two_pair[1]
    hand1 = two_pair[0]
    three_o_kind = p.find_trips(hand1, board1)
    assert not three_o_kind


def test_3ok_type(three_of_a_kind):
    board = three_of_a_kind[1]
    hand = three_of_a_kind[0]
    three_o_kind_hand = p.find_trips(hand, board)
    assert three_o_kind_hand.type == '3ok'


def test_3ok_high_value(three_of_a_kind):
    board = three_of_a_kind[1]
    hand = three_of_a_kind[0]
    three_o_kind_hand = p.find_trips(hand, board)
    assert three_o_kind_hand.high_value == 14


def test_3ok_low_value(three_of_a_kind):
    board = three_of_a_kind[1]
    hand = three_of_a_kind[0]
    three_o_kind_hand = p.find_trips(hand, board)
    assert three_o_kind_hand.low_value == 12


def test_3ok_kicker(three_of_a_kind):
    board = three_of_a_kind[1]
    hand = three_of_a_kind[0]
    three_o_kind_hand = p.find_trips(hand, board)
    assert three_o_kind_hand.kicker == 10


def test_straight_sequential(straight_no_pair_no_flush):
    board3 = straight_no_pair_no_flush[1]
    hand3 = straight_no_pair_no_flush[0]
    straight_hand = p.find_straight(hand3, board3)
    assert straight_hand.type == 'straight'

def test_straight_non_sequential(non_seq_straight):
    board7 = non_seq_straight[1]
    hand7 = non_seq_straight[0]
    straight_hand = p.find_straight(hand7, board7)
    assert straight_hand.high_rank == '6'


def test_straight_5_card_type(straight_five_card):
    board8 = straight_five_card[1]
    hand8 = straight_five_card[0]
    straight_hand = p.find_straight(hand8, board8)
    assert straight_hand.type == 'straight'


def test_straight_5_card_high(straight_five_card):
    board8 = straight_five_card[1]
    hand8 = straight_five_card[0]
    straight_hand = p.find_straight(hand8, board8)
    assert straight_hand.high_value == 6


def test_straight_5_card_low(straight_five_card):
    board8 = straight_five_card[1]
    hand8 = straight_five_card[0]
    straight_hand = p.find_straight(hand8, board8)
    assert straight_hand.low_value == 0


def test_straight_5_card_kicker(straight_five_card):
    board8 = straight_five_card[1]
    hand8 = straight_five_card[0]
    straight_hand = p.find_straight(hand8, board8)
    assert straight_hand.kicker == 0


def test_straight_6_card(straight_six_card):
    board9 = straight_six_card[1]
    hand9 = straight_six_card[0]
    straight_hand = p.find_straight(hand9, board9)
    assert straight_hand.high_value == 7


def test_not_straight(two_pair):
    board4 = two_pair[1]
    hand4 = two_pair[0]
    straight = p.find_straight(hand4, board4)
    assert not straight


def test_straight_wheel(wheel):
    board12 = wheel[1]
    hand12 = wheel[0]
    straight_hand = p.find_straight(hand12, board12)
    assert straight_hand.high_rank == '5'


def test_not_straight_flush(boat):
    board = boat[1]
    hand = boat[0]
    straight_flush = p.find_straight_flush(hand, board)
    assert not straight_flush

def test_not_straight_flush_flush(flush_one_pair):
    board = flush_one_pair[1]
    hand = flush_one_pair[0]
    straight_flush = p.find_straight_flush(hand, board)
    assert not straight_flush


def test_straight_flush(straight_flush):
    board = straight_flush[1]
    hand = straight_flush[0]
    straight_flush_hand = p.find_straight_flush(hand, board)
    assert straight_flush_hand.high_value == 8

def test_hand_init():
    my_hand = new_hand
    assert type(my_hand) == poker_functions.Hand

def test_hand_value():
    my_hand = new_hand
    assert new_hand.hand_value == 2


def test_high_card_type(high_card):
    board = high_card[1]
    hand = high_card[0]
    high_card_hand = p.find_high_card(hand, board)
    assert high_card_hand.type == 'hc'


def test_high_card_high(high_card):
    board = high_card[1]
    hand = high_card[0]
    high_card_hand = p.find_high_card(hand, board)
    assert high_card_hand.high_value == 12


def test_high_card_low(high_card):
    board = high_card[1]
    hand = high_card[0]
    high_card_hand = p.find_high_card(hand, board)
    assert high_card_hand.low_value == 10


def test_high_card_kicker(high_card):
    board = high_card[1]
    hand = high_card[0]
    high_card_hand = p.find_high_card(hand, board)
    assert high_card_hand.kicker == 9


def test_quads_type(quads):
    board = quads[1]
    hand = quads[0]
    quads = p.find_quads(hand, board)
    assert quads.type == '4ok'


def test_quads_high(quads):
    board = quads[1]
    hand = quads[0]
    quads = p.find_quads(hand, board)
    assert quads.high_value == 4


def test_quads_low(quads):
    board = quads[1]
    hand = quads[0]
    quads = p.find_quads(hand, board)
    assert quads.low_value == 14


def test_not_quads(flush_one_pair):
    board = flush_one_pair[1]
    hand = flush_one_pair[0]
    quads = p.find_quads(hand, board)
    assert not quads


def test_not_boat(flush_one_pair):
    hand = flush_one_pair[0]
    board = flush_one_pair[1]
    boat = p.find_full_house(hand, board)
    assert not boat


def test_boat_high(boat):
    hand = boat[0]
    board = boat[1]
    boat = p.find_full_house(hand, board)
    assert boat.high_value == 14


def test_boat_low(boat):
    hand = boat[0]
    board = boat[1]
    boat = p.find_full_house(hand, board)
    assert boat.low_value == 4


def test_boat_type(boat):
    hand = boat[0]
    board = boat[1]
    boat = p.find_full_house(hand, board)
    assert boat.type == 'boat'

