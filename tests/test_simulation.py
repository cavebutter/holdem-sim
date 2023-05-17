import pytest
import poker_functions
import simulation as s

@pytest.fixture
def six_card_straight_board():
    # Straight, 6 card
    flop9 = ['Jh', '3c', '6d']
    turn9 = ['4h']
    river9 = ['5s']
    board = flop9 + turn9 + river9
    return board


@pytest.fixture
def six_card_straight_hand():
    hand9 = ['2c', '7s']
    return hand9

#  Duplicated Card
@pytest.fixture
def duplicate_hand():
    hand10 = ['3c', 'As']
    flop10 = ['3c', 'Jd', '9h']
    turn10 = ['4s']
    river10 = ['8s']
    check = hand10 + flop10 + turn10 + river10
    return check


@pytest.fixture
def impossible_straight():
    hand = ['As', 'Kd']
    flop = ['Kh', '6c', '4s']
    return hand, flop


#  Invalid Card
@pytest.fixture
def invalid_card():
    hand11 = ['3c', 'As']
    flop11 = ['9c', 'Jd', '9h']
    turn11 = ['4s']
    river11 = ['Ss']
    check = hand11 + flop11 + turn11 + river11
    return check

def test_simulation_incomplete_board():
    """Will the sim run without errors with an incomplete board? Minimum result is 1 pair"""
    hand = ['Ac', '3d']
    flop = ['As', '5c', '4d']
    sims = 5
    sim = s.simulation_one_player(hand, flop, sims=sims)
    assert sim[0] == 5


def test_no_impossible_straight(impossible_straight):
    """Prior to refactor, this hand and others similar would yield a small % of straights"""
    hand = impossible_straight[0]
    flop = impossible_straight[1]
    sim = s.simulation_one_player(hand, flop)
    assert sim[5] == 0


def test_duplicate_card(duplicate_hand):
    check = duplicate_hand
    duplicate = s.dedupe(check)
    assert duplicate


def test_not_duplicate(six_card_straight_hand, six_card_straight_board):
    check = six_card_straight_hand + six_card_straight_board
    duplicate = s.dedupe(check)
    assert not duplicate


def test_valid_card(six_card_straight_hand, six_card_straight_board):
    check = six_card_straight_hand + six_card_straight_board
    valid = s.validate_card(check)
    assert valid


def test_invalid_card(invalid_card):
    check = invalid_card
    valid = s.validate_card(check)
    assert not valid


def test_player_create():
    player = s.Player(1, ['Ac', 'Ad'])
    assert type(player) == s.Player


def test_player_cards():
    player = s.Player(1, ['Ac', 'Ad'])
    assert type(player.cards[0]) == poker_functions.Card


def test_player_no_cards():
    player = s.Player(2)
    assert player

def test_multiplayer_create_players_no_hole_cards():
    foo = s.simulation_multiplayer(['As', '9d'], opponents=3)
    assert len(foo) == 3


def test_multiplayer_create_players_with_hole_cards():
    foo = s.simulation_multiplayer(['As', '9d'], ['Jd', '8c'], ['6h', 'Kh'], opponents=3)
    assert len(foo) == 3


def test_multiplayer_with_hole_cards():
    foo = s.simulation_multiplayer(['As', '9d'], ['Kd', 'Th'], opponents=2)
    assert len(foo[1].cards) == 2


def test_score_game_single_winner():
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('3ok', 8, kicker=10)
    player1.hand = poker_functions.Hand('hc', 13, 10, 9)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[0].wins == 1


def test_score_game_high_winner():
    """More than 1 hand has a straight, flush or straight flush.  High card wins"""
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('flush', 13)
    player1.hand = poker_functions.Hand('flush', 9)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[0].wins == 1


def test_score_game_high_chop():
    """More than 1 hand has a straight, flush or straight flush.  Draw."""
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('flush', 13)
    player1.hand = poker_functions.Hand('flush', 13)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[0].wins == 0 and foo[1].wins == 0


def test_score_game_boat_high_plays():
    """More than 1 hand has a straight, flush or straight flush.  High card wins"""
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('boat', 13, 5)
    player1.hand = poker_functions.Hand('boat', 9, 6)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[0].wins == 1


def test_score_game_boat_low_plays():
    """More than 1 hand has a straight, flush or straight flush.  High card wins"""
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('boat', 13, 5)
    player1.hand = poker_functions.Hand('boat', 13, 6)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[1].wins == 1



def test_score_game_hi_lo_kick_clear_hi_winner():
    """More than 1 hand has a straight, flush or straight flush.  High card wins"""
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('boat', 13, 5)
    player1.hand = poker_functions.Hand('boat', 10, 6)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[0].wins == 1


def test_score_game_hi_lo_kick_lo_winner():
    """More than 1 hand has trips.  Fourth card plays"""
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('3ok', 13, 5, 3)
    player1.hand = poker_functions.Hand('3ok', 10, 6, 5)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[0].wins == 1


def test_score_game_hi_lo_kick_kicker_winner():
    """More than 1 hand has trips.  Fifth card plays """
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('3ok', 13, 5, 3)
    player1.hand = poker_functions.Hand('3ok', 13, 5, 4)
    player2.hand = poker_functions.Hand('pair', 8, kicker=12)

    contestants = [player0, player1, player2]

    foo = s.score_game(contestants)

    assert foo[1].wins == 1


@pytest.fixture
def quad_showdown():
    """More than 1 hand has quads.  Fifth card plays """
    player0 = s.Player(0)
    player1 = s.Player(1)
    player2 = s.Player(2)

    player0.hand = poker_functions.Hand('4ok', 5, low_value=3)
    player1.hand = poker_functions.Hand('4ok', 5, low_value=4)
    player2.hand = poker_functions.Hand('pair', 8, low_value=12, kicker=9)

    contestants = [player0, player1, player2]
    return contestants


def test_score_game_kicker_winner(quad_showdown):

    contestants = quad_showdown

    foo = s.score_game(contestants)

    assert foo[1].wins == 1