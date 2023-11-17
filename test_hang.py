import pytest
from hang import Game
from hang import History

@pytest.fixture
def game_instance():
    game = Game()
    game._answer = "testinggame"
    game._status = "_es_______e"
    game._remainingGuesses = 6
    game._guessed = set()
    return game

@pytest.fixture
def hist_instance():
    hist = History()
    hist._scores = []
    hist.readTable()
    return hist

#Test Functions
def test_validLetter(game_instance):
    game = game_instance
    assert game.validLetter('b') == True
    assert game.validLetter('g') == True
    assert game.validLetter('a') == True
    game._guessed = "abcxyz2"
    assert game.validLetter('d') == True
    assert game.validLetter('1') == False
    assert game.validLetter('a') == False
    assert game.validLetter('2') == False
    game._guessed = set()

# Hist Functions
def test_updateCsvAtEnd(hist_instance):
    hist_instance.updateCsvAtEnd("test_player", 10)
    assert len(hist_instance.getScores()) > 0
    assert any(player["name"] == "test_player" and player["high_score"] == 10 for player in hist_instance.getScores())
