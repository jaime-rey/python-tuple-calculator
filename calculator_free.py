"""Versión reducida: solo +, -, *, / con constantes E y PI."""
from __future__ import annotations

import math
import sys


def evaluate(expr: str) -> float:
    if expr is None:
        raise ValueError("La entrada no puede ser nula")
    cleaned = expr.strip()
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = cleaned[1:-1]
    parts = cleaned.split(",")
    if len(parts) != 3:
        raise ValueError(f"Formato inválido. Se esperaba (n1,n2,op) — recibido: {expr}")
    a = _parse_number(parts[0].strip())
    b = _parse_number(parts[1].strip())
    op = parts[2].strip()
    if len(op) != 1:
        raise ValueError(f"Operador inválido: {op}")
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("División por cero")
        return a / b
    raise ValueError(
        f"Operador no soportado en versión Free: {op} (solo +, -, *, /). "
        "Actualiza a la versión completa."
    )


def _parse_number(token: str) -> float:
    if token.upper() == "E":
        return math.e
    if token.upper() == "PI":
        return math.pi
    try:
        return float(token)
    except ValueError:
        raise ValueError(f"Número inválido: {token}") from None


def _format(v: float) -> str:
    if v == math.floor(v) and not math.isinf(v):
        return str(int(v))
    return str(v)


def _run(expr: str) -> None:
    try:
        print(f"{expr} -> {_format(evaluate(expr))}")
    except (ValueError, ArithmeticError, ZeroDivisionError) as ex:
        print(f"{expr} -> ERROR: {ex}")


if __name__ == "__main__":
    ejemplos = ["(1,1,+)", "(7,5,-)", "(6,3,*)", "(4,2,/)", "(1,0,/)",
                "(2,E,*)", "(PI,2,/)", "(E,PI,+)"]
    for e in ejemplos:
        _run(e)
    if sys.argv[1:]:
        print("---")
        for a in sys.argv[1:]:
            _run(a)
