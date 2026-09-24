"""Suite de pruebas para el módulo calculator."""
import math

import pytest

from calculator import evaluate, process, solve


# ---------------------------- Escalares binarios ----------------------------

@pytest.mark.parametrize("expr,expected", [
    ("(1,1,+)", 2),
    ("(7,5,-)", 2),
    ("(6,3,*)", 18),
    ("(4,2,/)", 2),
    ("(3,2,^)", 9),
    ("(9,2,R)", 3),
    ("(100,10,L)", 2),
    ("(10,E,L)", math.log(10)),
])
def test_binary_ops(expr, expected):
    assert evaluate(expr) == pytest.approx(expected)


def test_constants():
    assert evaluate("(2,E,*)") == pytest.approx(2 * math.e)
    assert evaluate("(PI,3,*)") == pytest.approx(3 * math.pi)


# ---------------------------- Errores ----------------------------

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("(1,0,/)")


def test_root_index_zero():
    with pytest.raises(ArithmeticError):
        evaluate("(9,0,R)")


def test_even_root_of_negative():
    with pytest.raises(ArithmeticError):
        evaluate("(-9,2,R)")


def test_odd_root_of_negative():
    assert evaluate("(-8,3,R)") == pytest.approx(-2)


def test_log_invalid():
    with pytest.raises(ArithmeticError):
        evaluate("(0,10,L)")


# ---------------------------- Unarios ----------------------------

@pytest.mark.parametrize("expr,expected", [
    ("(0,!)", 1),
    ("(5,!)", 120),
    ("(10,!)", 3628800),
    ("(0,F)", 0),
    ("(1,F)", 1),
    ("(5,F)", 5),
    ("(10,F)", 55),
])
def test_unary_ops(expr, expected):
    assert evaluate(expr) == pytest.approx(expected)


def test_factorial_negative():
    with pytest.raises(ArithmeticError):
        evaluate("(-1,!)")


# ---------------------------- Primos ----------------------------

def test_primes_up_to():
    assert process("(10,P)") == "2,3,5,7"
    assert process("(30,P)") == "2,3,5,7,11,13,17,19,23,29"


def test_primes_range():
    assert process("(50,70,P)") == "53,59,61,67"


def test_primes_limit():
    with pytest.raises(ArithmeticError):
        process("(1,2000000000,P)")


# ---------------------------- Ecuaciones polinómicas ----------------------------

def test_quadratic_real():
    roots = solve("(1,-3,2,X)")
    values = sorted(r.real for r in roots)
    assert values == pytest.approx([1, 2])


def test_quadratic_complex():
    roots = solve("(2,2,2,X)")
    for r in roots:
        assert r.real == pytest.approx(-0.5)
        assert abs(r.imag) == pytest.approx(math.sqrt(3) / 2)


def test_cubic_real():
    roots = solve("(1,-6,11,-6,X)")
    values = sorted(round(r.real) for r in roots)
    assert values == [1, 2, 3]
    for r in roots:
        assert abs(r.imag) < 1e-9


# ---------------------------- Polinomios ----------------------------

def test_poly_mul():
    assert process("[(1,1),(1,-1),*]") == "(1,0,-1)"
    assert process("[(1,1),(1,1),*]") == "(1,2,1)"


def test_poly_add_sub():
    assert process("[(1,2,3),(4,5,6),+]") == "(5,7,9)"
    assert process("[(1,2,3),(1,1),-]") == "(1,1,2)"


# ---------------------------- Matrices ----------------------------

def test_matrix_add():
    assert process("[[(1,1),(1,1)],[(1,1),(1,1)],+]") == "[(2,2),(2,2)]"


def test_matrix_mul():
    assert process("[[(1,2),(3,4)],[(5,6),(7,8)],*]") == "[(19,22),(43,50)]"


def test_matrix_incompatible():
    with pytest.raises(ValueError):
        process("[[(1,2)],[(3,4),(5,6)],+]")


def test_scalar_times_matrix():
    assert process("[3,[(1,2),(3,4)],*]") == "[(3,6),(9,12)]"
    assert process("[[(1,2),(3,4)],2,*]") == "[(2,4),(6,8)]"


def test_transpose():
    assert process("[[(1,2,3),(4,5,6)],T]") == "[(1,4),(2,5),(3,6)]"


def test_determinant():
    assert process("[[(1,2),(3,4)],D]") == "-2"
    assert process("[[(6,1,1),(4,-2,5),(2,8,7)],D]") == "-306"


def test_determinant_non_square():
    with pytest.raises(ValueError):
        process("[[(1,2,3),(4,5,6)],D]")


# ---------------------------- Malformados ----------------------------

@pytest.mark.parametrize("expr", ["()", "(1,)", "(,+)", "[T]", "[]"])
def test_malformed(expr):
    with pytest.raises(ValueError):
        process(expr)


# ---------------------------- Suma de array ----------------------------

def test_array_sum():
    assert evaluate("{1,2,3,4,5}") == pytest.approx(15)
    assert process("{1,2,3,4,5}") == "15"
    assert evaluate("{PI,E}") == pytest.approx(math.pi + math.e)
    assert evaluate("{}") == 0


def test_array_sum_malformed():
    with pytest.raises(ValueError):
        evaluate("{1,2,3")
