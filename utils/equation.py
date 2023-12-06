def solve_equation_degree_2(a: float, b: float, c: float) -> tuple[float, float] | None:
    d = b * b - 4 * a * c
    if d < 0:
        return None
    if d == 0:
        return -b / (2 * a)
    d = d**0.5
    x1, x2 = (-b + d) / (2 * a), (-b - d) / (2 * a)
    return (x1, x2) if x1 < x2 else (x2, x1)
