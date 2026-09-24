"""Entry point: `python -m calculator [expr ...]`."""
import sys
from . import process

EJEMPLOS = [
    "(1,1,+)", "(4,2,/)", "(3,2,^)", "(100,10,L)",
    "(2,E,*)", "(PI,3,*)", "(10,E,L)", "(9,2,R)",
    "(1,-3,2,X)", "(2,2,2,X)", "(1,0,-1,Y)",
    "(1,0,0,-8,X)", "(1,-6,11,-6,X)",
    "(5,!)", "(0,!)", "(5,F)", "(10,F)",
    "(10,P)", "(30,P)", "(1,100,P)", "(50,70,P)",
    "[(1,1),(1,-1),*]",
    "[(1,1),(1,1),*]",
    "[(1,2,3),(4,5,6),+]",
    "[(1,2,3),(1,1),-]",
    "[(1,0,0,0),(1,0,0,0),*]",
    "[[(1,1),(1,1)],[(1,1),(1,1)],+]",
    "[[(1,2),(3,4)],[(5,6),(7,8)],-]",
    "[[(1,2),(3,4)],[(5,6),(7,8)],*]",
    "[[(1,2,3)],[(4),(5),(6)],*]",
    "[3,[(1,2),(3,4)],*]",
    "[[(1,2),(3,4)],2,*]",
    "[[(1,2,3),(4,5,6)],T]",
    "[[(1,2),(3,4)],D]",
    "[[(6,1,1),(4,-2,5),(2,8,7)],D]",
    "{1,2,3,4,5}",
    "{PI,E,10}",
]


def _run(expr: str) -> None:
    try:
        print(f"{expr} -> {process(expr)}")
    except (ValueError, ArithmeticError, ZeroDivisionError, RuntimeError) as ex:
        print(f"{expr} -> ERROR: {ex}")


def main(argv: list[str]) -> None:
    for e in EJEMPLOS:
        _run(e)
    if argv:
        print("---")
        for a in argv:
            _run(a)


if __name__ == "__main__":
    main(sys.argv[1:])
