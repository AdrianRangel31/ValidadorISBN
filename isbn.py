VALID_ISBN10 = "ISBN-10"
VALID_ISBN13 = "ISBN-13"
INVALID = "INVALID"

def normalize_isbn(s):
    if s is None:
        return ""
    cleaned_chars = []
    for ch in s:
        if ch.isspace() or ch == "-":
            continue
        cleaned_chars.append(ch)
    cleaned = "".join(cleaned_chars).upper()

    if cleaned == "":
        return ""

    for i, ch in enumerate(cleaned):
        if ch.isdigit():
            continue
        if ch == "X":
            if i != len(cleaned) - 1:
                raise ValueError("Caracter 'X' solo permitido como último carácter.")
            continue
        raise ValueError("Caracter ilegal en ISBN: '{}'".format(ch))
    return cleaned

def is_valid_isbn10(s):
    try:
        cleaned = normalize_isbn(s)
    except ValueError:
        return False

    if len(cleaned) != 10:
        return False


    for ch in cleaned[:9]:
        if not ch.isdigit():
            return False

    last = cleaned[9]
    if not (last.isdigit() or last == "X"):
        return False

    total = 0
    for i in range(10):
        ch = cleaned[i]
        if ch == "X":
            value = 10
        else:
            value = ord(ch) - ord("0")
        weight = 10 - i
        total += weight * value

    return total % 11 == 0

def is_valid_isbn13(s):

    try:
        cleaned = normalize_isbn(s)
    except ValueError:
        return False

    if len(cleaned) != 13:
        return False

    for ch in cleaned:
        if not ch.isdigit():
            return False

    total = 0
    for i, ch in enumerate(cleaned):
        value = ord(ch) - ord("0")
        weight = 1 if (i % 2 == 0) else 3
        total += weight * value

    return total % 10 == 0

def detect_isbn(s, logger=None):
    """
    Detecta si una cadena es un ISBN-10, ISBN-13 o Inválido.
    
    Args:
        s (str): La cadena a validar.
        logger (object, optional): Un objeto logger que tenga un método .warn().
                                   Se usa para loggear entradas inválidas.
    
    Returns:
        str: "ISBN-10", "ISBN-13", o "INVALID".
    """
    try:
        cleaned = normalize_isbn(s)
    except ValueError:
        if logger:
            logger.warn(f"ISBN Inválido detectado (caracter ilegal): {s}")
        return INVALID

    if cleaned == "":
        if logger:
            logger.warn(f"ISBN Inválido detectado (vacío): {s}")
        return INVALID

    if len(cleaned) == 10:
        if is_valid_isbn10(cleaned):
            return VALID_ISBN10
        else:
            if logger:
                logger.warn(f"ISBN Inválido detectado (checksum/formato 10): {s}")
            return INVALID
            
    if len(cleaned) == 13:
        if is_valid_isbn13(cleaned):
            return VALID_ISBN13
        else:
            if logger:
                logger.warn(f"ISBN Inválido detectado (checksum/formato 13): {s}")
            return INVALID

    if logger:
        logger.warn(f"ISBN Inválido detectado (longitud): {s}")
    return INVALID

__all__ = ["normalize_isbn", "is_valid_isbn10", "is_valid_isbn13", "detect_isbn"]

# Este bloque solo se ejecuta si corres "python isbn.py"
# No será cubierto por las pruebas (lo cual es correcto)
if __name__ == "__main__":
    isbn = "0-879-30566-8"
    print(f"Normalizado: {normalize_isbn(isbn)}")
    print(f"Es ISBN-10: {is_valid_isbn10(isbn)}")
    print(f"Es ISBN-13: {is_valid_isbn13(isbn)}")
    print(f"Detectado: {detect_isbn(isbn)}")
