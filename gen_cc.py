import random
import time


# Algoritmo Luhn para verificar la validez del número de tarjeta de crédito
def luhn_check(card_number):
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n = n * 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


# Generar número de tarjeta de crédito basado en un BIN
def generar_tarjeta(bin_number, mes=None, ano=None, cvc=None):
    # Generar los dígitos aleatorios para completar el número de la tarjeta
    cc_number = ""

    # Recorrer el BIN y reemplazar las 'x' con dígitos aleatorios
    for c in bin_number:
        if c == 'x':
            cc_number += random.choice('0123456789')
        else:
            cc_number += c

    # Asegurarnos de que el número es válido con el algoritmo Luhn
    if not luhn_check(cc_number):
        # Si no es válido, seguimos generando hasta que sea válido
        while not luhn_check(cc_number):
            cc_number = ""
            for c in bin_number:
                if c == 'x':
                    cc_number += random.choice('0123456789')
                else:
                    cc_number += c

    # Generar mes de expiración (si no se pasa)
    if not mes:
        month = random.randint(1, 12)
        mm = f"{month:02d}"
    else:
        mm = mes

    # Generar año de expiración (si no se pasa)
    if not ano:
        current_year = time.localtime().tm_year
        year = random.randint(current_year + 1, current_year + 5)  # Añadido el rango entre 1-5 años de futuro
        yyyy = str(year)
    else:
        yyyy = ano

    # Generar código de seguridad (CVC) si no se pasa
    if not cvc:
        cvc = ''.join(random.choices('0123456789', k=3))
    else:
        cvc = cvc

    return f"{cc_number}|{mm}|{yyyy}|{cvc}"

def gen():
    bin_number = '401795412607xxxx'
    mes = '11'
    ano = '2025'
    if len(bin_number) < 16:
        print("El bin debe de ser de 16 digitos entre x y numeros")
        return
    # Generar la tarjeta
    tarjeta = generar_tarjeta(bin_number, mes=mes, ano=ano)
    return tarjeta
