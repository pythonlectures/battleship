import pytest
import battleship_oo2 as btl


@pytest.fixture
def a_cell_hit():
    return btl.Cell(btl.Coordinates(2, 1), btl.CellStatus.HIT)


class TestCell:

    def test_set_correct_status(self):
        cell = a_cell_hit()
        new_status = btl.CellStatus.UNDISCOVERED
        cell.set_status(new_status)
        assert cell.get_status() is new_status

    def test_set_wrong_status(self):
        cell = a_cell_hit()
        new_status = "wrong_status"
        with pytest.raises(ValueError):
            cell.set_status(new_status)


@pytest.fixture
def a_ship_half_hit():
    ship = btl.Ship((btl.Coordinates(2, 2), btl.Coordinates(2, 3)))
    ship._cells[0].set_status(btl.CellStatus.HIT)
    return ship


@pytest.fixture
def a_hitting_shot():
    return btl.Shot(btl.Coordinates(2, 3))


@pytest.fixture
def a_missing_shot():
    return btl.Shot(btl.Coordinates(4, 4))


@pytest.fixture
def ship_is_hit():
    ship = a_ship_half_hit()
    ship.is_hit(shot=a_hitting_shot())
    return ship


@pytest.fixture
def ship_is_not_hit():
    ship = a_ship_half_hit()
    ship.is_hit(shot=a_missing_shot())
    return ship


class TestShip(object):

    def test_is_cell_set_to_hit_when_shot_is_a_hit(self):
        ship = ship_is_hit()
        assert ship._cells[1].get_status() is btl.CellStatus.HIT

    def test_is_cell_still_undiscovered_when_shot_is_a_miss(self):
        ship = ship_is_not_hit()
        assert ship._cells[1].get_status() is btl.CellStatus.UNDISCOVERED

    def test_is_sunk_when_shot_is_a_hit(self):
        ship = ship_is_hit()
        assert ship._is_sunk is True

    def test_is_sunk_when_shot_is_a_miss(self):
        ship = ship_is_not_hit()
        assert ship._is_sunk is False
