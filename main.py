def division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Le diviseur ne peut pas être zéro.")
    return a / b


if __name__ == "__main__":
    nombre1 = 10
    nombre2 = 2
    resultat = division(nombre1, nombre2)
    print(f"{nombre1} / {nombre2} = {resultat}")
