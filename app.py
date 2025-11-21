import random
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")


dice_pattern = re.compile(
    r"^\s*(?P<count>\d+)d(?P<sides>\d+)(?:(?P<keep_type>kh|kl)(?P<keep_count>\d+))?(?P<modifier>[+-]\d+)?\s*$",
    re.IGNORECASE,
)


@dataclass
class DiceRollResult:
    expression: str
    rolls: List[int]
    kept: List[int]
    modifier: int
    total: int


class DiceExpressionError(ValueError):
    """Raised when a dice expression cannot be parsed."""


def parse_expression(expression: str) -> Tuple[int, int, Optional[str], Optional[int], int]:
    match = dice_pattern.match(expression)
    if not match:
        raise DiceExpressionError("Invalid dice expression. Use patterns like 2d20, 4d6kh3, or 9d4-4.")

    count = int(match.group("count"))
    sides = int(match.group("sides"))
    keep_type = match.group("keep_type")
    keep_count = match.group("keep_count")
    modifier = int(match.group("modifier") or 0)

    if count <= 0 or sides <= 1:
        raise DiceExpressionError("Dice count must be positive and sides must be at least 2.")

    keep_count_int = int(keep_count) if keep_count else None
    if keep_count_int is not None and keep_count_int <= 0:
        raise DiceExpressionError("Keep count must be positive when specified.")
    if keep_count_int is not None and keep_count_int > count:
        raise DiceExpressionError("Keep count cannot exceed the number of dice rolled.")

    return count, sides, keep_type.lower() if keep_type else None, keep_count_int, modifier


def roll_dice(expression: str) -> DiceRollResult:
    count, sides, keep_type, keep_count, modifier = parse_expression(expression)

    rolls = [random.randint(1, sides) for _ in range(count)]

    if keep_type == "kh":
        kept_sorted = sorted(rolls, reverse=True)
    elif keep_type == "kl":
        kept_sorted = sorted(rolls)
    else:
        kept_sorted = list(rolls)

    keep_limit = min(keep_count if keep_count is not None else len(kept_sorted), len(kept_sorted))
    kept = kept_sorted[:keep_limit]

    total = sum(kept) + modifier

    return DiceRollResult(
        expression=expression.strip(),
        rolls=rolls,
        kept=kept,
        modifier=modifier,
        total=total,
    )


@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/roll", methods=["POST"])
def api_roll():
    data = request.get_json(silent=True) or {}
    expression = data.get("expression", "")

    try:
        result = roll_dice(expression)
    except DiceExpressionError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({
        "expression": result.expression,
        "rolls": result.rolls,
        "kept": result.kept,
        "modifier": result.modifier,
        "total": result.total,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
