import json

import pytest

from app import DiceExpressionError, app, parse_expression, roll_dice


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_parse_expression_valid_keep_high():
    count, sides, keep_type, keep_count, modifier = parse_expression("4d6kh3")

    assert (count, sides) == (4, 6)
    assert keep_type == "kh"
    assert keep_count == 3
    assert modifier == 0


def test_parse_expression_rejects_invalid_keep_count():
    with pytest.raises(DiceExpressionError):
        parse_expression("3d6kh0")


def test_parse_expression_rejects_keep_count_over_dice():
    with pytest.raises(DiceExpressionError):
        parse_expression("2d6kh3")


def test_roll_dice_returns_expected_structure():
    result = roll_dice("2d4+1")

    assert result.expression == "2d4+1"
    assert len(result.rolls) == 2
    assert result.kept and len(result.kept) <= 2
    assert isinstance(result.total, int)


def test_api_roll_success(client):
    response = client.post(
        "/api/roll", data=json.dumps({"expression": "1d6"}), content_type="application/json"
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["expression"] == "1d6"
    assert payload["total"] >= 1


def test_api_roll_invalid_expression_returns_error(client):
    response = client.post(
        "/api/roll", data=json.dumps({"expression": "bad"}), content_type="application/json"
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert "Invalid dice expression" in payload["error"]
