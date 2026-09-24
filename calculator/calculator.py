"""Calculadora que interpreta expresiones en forma de tupla.

Formatos:
    (a, b, op)           operaciones escalares (+, -, *, /, ^, R, L)
    (a, op)              operadores unarios (!, F)
    (n, P) / (a, b, P)   primos hasta n / en [a,b]
    (a_n,...,a_0, X)     ecuación polinómica (X o Y)
    [(p),(q), op]        aritmética de polinomios (+, -, *)
    [[m1],[m2], op]      aritmética de matrices (+, -, *)
    [k,[m], *]           escalar por matriz
    [[m], T]             traspuesta
    [[m], D]             determinante
"""
from __future__ import annotations

import math
from typing import Iterable

MAX_PRIME_LIMIT = 100_000_000


# ---------------------------- API pública ----------------------------

def evaluate(expr: str) -> float:
    nums, op = _parse(expr)
    if op in ("X", "Y"):
        raise RuntimeError("Usa solve() para ecuaciones polinómicas")
    if len(nums) == 1:
        return _unary_op(op, nums[0])
    if len(nums) == 2:
        return _binary_op(op, nums[0], nums[1])
    raise ValueError(f"Formato inválido para operador escalar: {expr}")


def solve(expr: str) -> list[complex]:
    nums, op = _parse(expr)
    if op not in ("X", "Y"):
        raise ValueError("Se esperaba operador 'X' o 'Y' para ecuación polinómica")
    if len(nums) < 2:
        raise ValueError("Se necesitan al menos 2 coeficientes (grado >= 1)")
    return _solve_polynomial(nums)


def process(expr: str) -> str:
    if expr is None:
        raise ValueError("La entrada no puede ser nula")
    s = expr.strip()
    if s.startswith("["):
        return _process_bracketed(s)
    nums, op = _parse(expr)
    if op == "P":
        return ",".join(str(p) for p in _primes_from_args(nums))
    if op in ("X", "Y"):
        return _format_roots(op, _solve_polynomial(nums))
    return _format_number(evaluate(expr))


# ---------------------------- Parseo ----------------------------

def _parse(expr: str) -> tuple[list[float], str]:
    if expr is None:
        raise ValueError("La entrada no puede ser nula")
    cleaned = _strip_parens(expr.strip())
    parts = cleaned.split(",")
    if len(parts) < 2:
        raise ValueError(f"Formato inválido. Mínimo (n,op) — recibido: {expr}")
    op = parts[-1].strip()
    if len(op) != 1:
        raise ValueError(f"Operador inválido: {op}")
    nums = [_parse_number(p.strip()) for p in parts[:-1]]
    return nums, op


def _strip_parens(s: str) -> str:
    if s.startswith("(") and s.endswith(")"):
        return s[1:-1]
    return s


def _parse_number(token: str) -> float:
    if token.upper() == "E":
        return math.e
    if token.upper() == "PI":
        return math.pi
    try:
        return float(token)
    except ValueError as _:
        raise ValueError(f"Número inválido: {token}") from None


def _split_top_level(s: str) -> list[str]:
    out = []
    depth = 0
    start = 0
    for i, c in enumerate(s):
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c == "," and depth == 0:
            out.append(s[start:i])
            start = i + 1
    out.append(s[start:])
    return out


# ---------------------------- Escalares ----------------------------

def _unary_op(op: str, a: float) -> float:
    if op == "!":
        return _factorial(a)
    if op == "F":
        return _fibonacci(a)
    raise ValueError(f"Operador unario no soportado: {op}")


def _binary_op(op: str, a: float, b: float) -> float:
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return _divide(a, b)
    if op == "^": return a ** b
    if op == "R": return _root(a, b)
    if op == "L": return _logarithm(a, b)
    raise ValueError(f"Operador no soportado: {op}")


def _divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("División por cero")
    return a / b


def _root(a: float, b: float) -> float:
    if b == 0:
        raise ArithmeticError("Índice de la raíz no puede ser 0")
    if a < 0 and b % 2 == 0:
        raise ArithmeticError("Raíz de índice par de un número negativo no es real")
    if a < 0:
        return -((-a) ** (1.0 / b))
    return a ** (1.0 / b)


def _logarithm(a: float, b: float) -> float:
    if a <= 0 or b <= 0 or b == 1:
        raise ArithmeticError("Logaritmo inválido: argumento > 0 y base > 0 y != 1")
    return math.log(a) / math.log(b)


def _factorial(a: float) -> float:
    if a < 0 or a != math.floor(a):
        raise ArithmeticError("Factorial requiere entero >= 0")
    n = int(a)
    r = 1
    for i in range(2, n + 1):
        r *= i
    return float(r)


def _fibonacci(a: float) -> float:
    if a < 0 or a != math.floor(a):
        raise ArithmeticError("Fibonacci requiere entero >= 0")
    n = int(a)
    if n == 0:
        return 0
    prev, curr = 0, 1
    for _ in range(1, n):
        prev, curr = curr, prev + curr
    return float(curr)


# ---------------------------- Primos ----------------------------

def _primes_from_args(nums: list[float]) -> list[int]:
    if len(nums) == 1:
        return _primes_in_range(0.0, nums[0])
    if len(nums) == 2:
        return _primes_in_range(nums[0], nums[1])
    raise ValueError("Formato inválido para P: (n,P) o (a,b,P)")


def _primes_in_range(lo: float, hi: float) -> list[int]:
    if lo != math.floor(lo) or hi != math.floor(hi):
        raise ArithmeticError("Primos requiere enteros")
    if hi < lo:
        raise ArithmeticError("Intervalo inválido: el límite superior debe ser >= al inferior")
    if hi > MAX_PRIME_LIMIT:
        raise ArithmeticError(f"Límite superior demasiado grande (máx {MAX_PRIME_LIMIT})")
    end = int(hi)
    if end < 2:
        return []
    start = max(2, int(lo))
    sieve = bytearray(b"\x01") * (end + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(end ** 0.5) + 1):
        if sieve[i]:
            step = i
            sieve[i * i:end + 1:step] = bytearray(len(sieve[i * i:end + 1:step]))
    return [i for i in range(start, end + 1) if sieve[i]]


# ---------------------------- Ecuaciones polinómicas ----------------------------

def _solve_polynomial(coeffs: list[float]) -> list[complex]:
    n = len(coeffs) - 1
    if n < 1:
        raise ValueError("Grado inválido")
    if coeffs[0] == 0:
        raise ValueError("El coeficiente principal no puede ser 0")
    if n == 1:
        return [complex(-coeffs[1] / coeffs[0], 0)]
    if n == 2:
        return _solve_quadratic(coeffs[0], coeffs[1], coeffs[2])
    return _durand_kerner(coeffs)


def _solve_quadratic(a: float, b: float, c: float) -> list[complex]:
    disc = b * b - 4 * a * c
    if disc >= 0:
        sq = math.sqrt(disc)
        return [complex((-b + sq) / (2 * a), 0), complex((-b - sq) / (2 * a), 0)]
    sq = math.sqrt(-disc)
    return [complex(-b / (2 * a), sq / (2 * a)),
            complex(-b / (2 * a), -sq / (2 * a))]


def _durand_kerner(coeffs: list[float]) -> list[complex]:
    n = len(coeffs) - 1
    monic = [c / coeffs[0] for c in coeffs]
    seed = complex(0.4, 0.9)
    z = [seed ** k for k in range(n)]
    for _ in range(2000):
        max_delta = 0.0
        for k in range(n):
            denom = complex(1, 0)
            for j in range(n):
                if j != k:
                    denom *= z[k] - z[j]
            delta = _poly_eval(monic, z[k]) / denom
            z[k] -= delta
            if abs(delta) > max_delta:
                max_delta = abs(delta)
        if max_delta < 1e-12:
            break
    return [_clean_complex(v) for v in z]


def _poly_eval(coeffs: list[complex] | list[float], x: complex) -> complex:
    r = complex(coeffs[0])
    for c in coeffs[1:]:
        r = r * x + c
    return r


def _clean_complex(z: complex) -> complex:
    re = 0.0 if abs(z.real) < 1e-9 else z.real
    im = 0.0 if abs(z.imag) < 1e-9 else z.imag
    return complex(re, im)


# ---------------------------- Aritmética estructurada ----------------------------

def _process_bracketed(expr: str) -> str:
    if not expr.endswith("]"):
        raise ValueError(f"Formato inválido: falta ']' en {expr}")
    inner = expr[1:-1]
    parts = _split_top_level(inner)
    op = parts[-1].strip()
    if len(op) != 1:
        raise ValueError(f"Operador inválido: {op}")

    if len(parts) == 2:
        m = _parse_matrix(parts[0].strip())
        if op == "T":
            return _format_matrix(_matrix_transpose(m))
        if op == "D":
            return _format_number(_determinant(m))
        raise ValueError(f"Operador unario no soportado en corchetes: {op} (usa T, D)")

    if len(parts) != 3:
        raise ValueError(f"Formato inválido — recibido: {expr}")

    first = parts[0].strip()
    second = parts[1].strip()
    first_is_matrix = first.startswith("[")
    second_is_matrix = second.startswith("[")

    if first_is_matrix and second_is_matrix:
        return _format_matrix(_matrix_op(op, _parse_matrix(first), _parse_matrix(second)))

    if first_is_matrix ^ second_is_matrix:
        if op != "*":
            raise ValueError("Escalar y matriz solo admiten '*'")
        matrix_str = first if first_is_matrix else second
        scalar_str = second if first_is_matrix else first
        return _format_matrix(_matrix_scale(_parse_matrix(matrix_str), _parse_number(scalar_str)))

    p = _parse_coeffs(first)
    q = _parse_coeffs(second)
    if op == "+": r = _poly_add(p, q)
    elif op == "-": r = _poly_sub(p, q)
    elif op == "*": r = _poly_mul(p, q)
    else: raise ValueError(f"Operador de polinomios no soportado: {op} (usa +, -, *)")
    return _format_coeffs(r)


# ---------------------------- Polinomios ----------------------------

def _parse_coeffs(token: str) -> list[float]:
    t = token.strip()
    if t.startswith("(") and t.endswith(")"):
        t = t[1:-1]
    return [_parse_number(x.strip()) for x in t.split(",")]


def _poly_add(p: list[float], q: list[float]) -> list[float]:
    n = max(len(p), len(q))
    r = [0.0] * n
    for i in range(n):
        a = p[-1 - i] if i < len(p) else 0
        b = q[-1 - i] if i < len(q) else 0
        r[-1 - i] = a + b
    return _trim_leading_zeros(r)


def _poly_sub(p: list[float], q: list[float]) -> list[float]:
    n = max(len(p), len(q))
    r = [0.0] * n
    for i in range(n):
        a = p[-1 - i] if i < len(p) else 0
        b = q[-1 - i] if i < len(q) else 0
        r[-1 - i] = a - b
    return _trim_leading_zeros(r)


def _poly_mul(p: list[float], q: list[float]) -> list[float]:
    r = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return _trim_leading_zeros(r)


def _trim_leading_zeros(r: list[float]) -> list[float]:
    i = 0
    while i < len(r) - 1 and r[i] == 0:
        i += 1
    return r[i:]


def _format_coeffs(r: list[float]) -> str:
    return "(" + ",".join(_format_number(v) for v in r) + ")"


# ---------------------------- Matrices ----------------------------

def _parse_matrix(token: str) -> list[list[float]]:
    t = token.strip()
    if not (t.startswith("[") and t.endswith("]")):
        raise ValueError(f"Matriz inválida: {token}")
    inner = t[1:-1]
    rows = _split_top_level(inner)
    m = [_parse_coeffs(r.strip()) for r in rows]
    if not all(len(row) == len(m[0]) for row in m):
        raise ValueError("Filas de longitud inconsistente en la matriz")
    return m


def _matrix_op(op: str, a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    if op == "+": return _matrix_add(a, b, 1)
    if op == "-": return _matrix_add(a, b, -1)
    if op == "*": return _matrix_mul(a, b)
    raise ValueError(f"Operador de matrices no soportado: {op} (usa +, -, *)")


def _matrix_add(a: list[list[float]], b: list[list[float]], sign: int) -> list[list[float]]:
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError(f"Dimensiones incompatibles: {len(a)}x{len(a[0])} vs {len(b)}x{len(b[0])}")
    return [[a[i][j] + sign * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _matrix_mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    if len(a[0]) != len(b):
        raise ValueError(
            f"Dimensiones incompatibles para producto: "
            f"{len(a)}x{len(a[0])} * {len(b)}x{len(b[0])}"
        )
    result = [[0.0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                result[i][j] += a[i][k] * b[k][j]
    return result


def _matrix_scale(m: list[list[float]], k: float) -> list[list[float]]:
    return [[k * v for v in row] for row in m]


def _matrix_transpose(m: list[list[float]]) -> list[list[float]]:
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def _determinant(m: list[list[float]]) -> float:
    if len(m) != len(m[0]):
        raise ValueError(f"El determinante requiere matriz cuadrada, recibida {len(m)}x{len(m[0])}")
    n = len(m)
    a = [row[:] for row in m]
    det = 1.0
    for col in range(n):
        pivot = col
        for row in range(col + 1, n):
            if abs(a[row][col]) > abs(a[pivot][col]):
                pivot = row
        if a[pivot][col] == 0:
            return 0.0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        det *= a[col][col]
        for row in range(col + 1, n):
            factor = a[row][col] / a[col][col]
            for k in range(col, n):
                a[row][k] -= factor * a[col][k]
    return det


def _format_matrix(m: list[list[float]]) -> str:
    return "[" + ",".join("(" + ",".join(_format_number(v) for v in row) + ")" for row in m) + "]"


# ---------------------------- Formato ----------------------------

def _format_number(v: float) -> str:
    if v == math.floor(v) and not math.isinf(v):
        return str(int(v))
    return str(v)


def _format_complex(z: complex) -> str:
    rs = _format_number(z.real)
    im_abs = _format_number(abs(z.imag))
    if z.imag == 0:
        return rs
    if z.real == 0:
        return ("-" if z.imag < 0 else "") + im_abs + "i"
    return rs + (" - " if z.imag < 0 else " + ") + im_abs + "i"


def _format_roots(label: str, roots: Iterable[complex]) -> str:
    return ", ".join(f"{label}{i+1} = {_format_complex(z)}" for i, z in enumerate(roots))
