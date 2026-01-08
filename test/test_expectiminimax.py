import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import math
import pytest

from algorithms.expectiminimax import ExpectiMinimaxPleyer
from game_engine import GameEngine
from game_state import State, PlayerColor


# --------------------------------------------------
# FIXTURES (إعداد مشترك)
# --------------------------------------------------

@pytest.fixture
def ai_black():
    return ExpectiMinimaxPleyer(PlayerColor.BLACK, max_depth=2)


@pytest.fixture
def engine():
    return GameEngine()


# --------------------------------------------------
# 1) SANITY TESTS
# --------------------------------------------------

def test_ai_does_not_crash(ai_black):
    state = State({1}, {10}, PlayerColor.BLACK, 2)
    ai_black.find_best_move(state)


# --------------------------------------------------
# 2) EVALUATION TESTS
# --------------------------------------------------

def test_black_win_evaluation(ai_black):
    state = State({1, 2}, set(), PlayerColor.WHITE, 3)
    assert ai_black.evaluate(state) == math.inf


def test_white_win_evaluation(ai_black):
    state = State(set(), {5}, PlayerColor.BLACK, 3)
    assert ai_black.evaluate(state) == -math.inf


def test_house_of_water_penalty(ai_black):
    state = State({5}, {27}, PlayerColor.BLACK, 1)
    assert ai_black.evaluate(state) < -30


def test_house_of_happiness_bonus(ai_black):
    state = State({5}, {26}, PlayerColor.BLACK, 1)
    assert ai_black.evaluate(state) > 20


def test_pawn_off_board_bonus(ai_black):
    state1 = State({1}, {29}, PlayerColor.BLACK, 2)
    state2 = State({1}, {29, 30}, PlayerColor.BLACK, 2)
    assert ai_black.evaluate(state1) > ai_black.evaluate(state2)


# --------------------------------------------------
# 3) CHANCE NODE TESTS
# --------------------------------------------------

def test_probabilities_sum_to_one(ai_black):
    assert abs(sum(ai_black.probabilities.values()) - 1.0) < 1e-6


def test_expected_value_differs_from_value(ai_black):
    state = State({1}, {10}, PlayerColor.BLACK, 2)
    v1 = ai_black.get_value(state, 1)
    v2 = ai_black.expected_value(state, 1)
    assert v1 != v2


# --------------------------------------------------
# 4) DECISION MAKING TESTS
# --------------------------------------------------

def test_avoid_house_of_water(ai_black):
    state = State({1}, {24, 10}, PlayerColor.BLACK, 3)
    assert ai_black.find_best_move(state) == 10


def test_prefer_house_of_happiness(ai_black):
    state = State({1}, {23, 12}, PlayerColor.BLACK, 3)
    assert ai_black.find_best_move(state) == 23


def test_choose_winning_move(ai_black):
    state = State({1}, {29, 25}, PlayerColor.BLACK, 2)
    assert ai_black.find_best_move(state) == 29


# --------------------------------------------------
# 5) DEPTH BEHAVIOR (NOT FORCING CHANGE)
# --------------------------------------------------

def test_deeper_search_runs_correctly():
    ai_shallow = ExpectiMinimaxPleyer(PlayerColor.BLACK, 1)
    ai_deep = ExpectiMinimaxPleyer(PlayerColor.BLACK, 3)

    state = State({14}, {22}, PlayerColor.BLACK, 3)

    move1 = ai_shallow.find_best_move(state)
    move2 = ai_deep.find_best_move(state)

    assert move1 is not None
    assert move2 is not None


# --------------------------------------------------
# 6) EDGE CASES
# --------------------------------------------------

def test_sticks_zero(ai_black):
    state = State({5}, {10}, PlayerColor.BLACK, 0)
    ai_black.find_best_move(state)


def test_single_pawn_safe(ai_black):
    state = State(set(), {1}, PlayerColor.BLACK, 5)
    ai_black.find_best_move(state)


def test_no_legal_moves(engine, ai_black):
    state = State({15}, {28}, PlayerColor.BLACK, 1)
    ai_black.get_value(state, 2)
