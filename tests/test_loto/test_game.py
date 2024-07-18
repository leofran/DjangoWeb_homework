import pytest
import loto.game as game
from loto.game import Game
from tests.test_loto.conftest import flat


class TestGame:
    @pytest.mark.parametrize(
        "kind_of_players,players_num,with_names,players_names",
        [
            ("computer", "2", "yes", ["Comp_1", "Comp_2"]),
            # ("person", "1", "", ""),
            # ("person", "", "", ""),
        ]
    )
    def test_call_players(self, kind_of_players, players_num, with_names, players_names, capsys):
        inputs = [
            players_num,
            with_names,
            players_names
        ]
        inputs = flat(inputs)

        outputs = [
            f"How many {kind_of_players}s are playing the game: ",
           ]
        if inputs[0]: outputs.extend(f"It is {inputs[0]} {kind_of_players}(s) in game. You can give them names (Y - I will, empty - default names): ")
        if inputs[1]: outputs.extend([f"Write name for playing {kind_of_players} number_{e + 1} (empty - default name): " for e, v in enumerate(players_names)])

        players_names_to_be = []
        if players_names:
            for name in players_names:
                players_names_to_be.append(f"{name} ({kind_of_players})")
        else:
            for i in range(int(0 if not players_num else players_num)):
                players_names_to_be.append(f"Player_{kind_of_players}_{i + 1}")

        def mock_input(s):
            print(s, end='')
            return inputs.pop(0)

        game.input = mock_input

        game_test = Game()
        players = game_test.call_players(kind_of_players)

        out, err = capsys.readouterr()

        assert out == "".join(outputs)
        assert err == ''
        assert game_test.players == players
        assert [str(player) for player in players] == players_names_to_be


