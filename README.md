# python-tuple-calculator

Calculadora en Python que interpreta expresiones en forma de tupla y devuelve el resultado. Puerto del proyecto Java [`java-tuple-calculator`](https://github.com/jaime-rey/java-tuple-calculator).

Soporta:

- Operaciones escalares: `+`, `-`, `*`, `/`, `^`, raíz (`R`), logaritmo (`L`).
- Constantes: `E`, `PI`.
- Operadores unarios: factorial (`!`), Fibonacci (`F`).
- Ecuaciones polinómicas (`X` / `Y`) de cualquier grado, con raíces reales y complejas.
- Listas de números primos (`P`) hasta un valor o en un intervalo.
- Aritmética de polinomios (`+`, `-`, `*`).
- Aritmética de matrices (`+`, `-`, `*`), escalar × matriz, traspuesta (`T`), determinante (`D`).

Sin dependencias externas (solo `pytest` para los tests). Requiere Python ≥ 3.10.

## Ejecutar

```bash
cd C:\pythontest; python -m calculator "(4,2,/)" "[[(1,2),(3,4)],D]"
```

## Tests

```bash
cd C:\pythontest; python -m pytest tests/ -q
```

## Documentación

- [MANUAL.md](MANUAL.md) — referencia completa con ejemplos.
- [MANUAL.pdf](MANUAL.pdf) — misma referencia en PDF.

## Versión reducida

`calculator_free.py` es un script autónomo con solo `+`, `-`, `*`, `/` y las constantes `E`, `PI`.

```bash
cd C:\pythontest; python calculator_free.py "(2,E,*)"
```
