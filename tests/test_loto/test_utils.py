import pytest
from loto.utils import NumCard
from functools import reduce


class TestUtils:
    @pytest.mark.parametrize(
        "rows_number,cells_in_row,cells_filled_in_row",
        [
            (2, 15, 10),
            (1, 2, 1),
        ]
    )
    def test_new_card(self, rows_number, cells_in_row, cells_filled_in_row):
        NumCard.rows_number = rows_number
        NumCard.cells_in_row = cells_in_row
        NumCard.cells_filled_in_row = cells_filled_in_row

        card = NumCard()
        new_card = card.new_card()

        assert len(new_card) == rows_number
        assert all(filter(lambda _: len(_) == cells_in_row, new_card))
        assert all(filter(lambda _: reduce(lambda x, y: int(x) + (0 if x == "" else 1), _) == cells_filled_in_row, new_card))
