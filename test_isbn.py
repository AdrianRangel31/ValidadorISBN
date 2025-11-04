import pytest
from unittest.mock import Mock
from isbn import (
    normalize_isbn, 
    is_valid_isbn10, 
    is_valid_isbn13, 
    detect_isbn, 
    INVALID, 
    VALID_ISBN10, 
    VALID_ISBN13
)

# ----------------------------
# PRUEBAS DE normalize_isbn
# ----------------------------

@pytest.mark.parametrize("entrada, esperado", [
    ("0-321-14653-0", "0321146530"),
    (" 0 3 2 1 1 4 6 5 3 0 ", "0321146530"),
    ("0-8044-2957-X", "080442957X"),
    ("", ""),
    (None, ""),
])
def test_normalize_isbn_valid(entrada, esperado):
    """Prueba la normalización de cadenas válidas, vacías y None."""
    assert normalize_isbn(entrada) == esperado

@pytest.mark.parametrize("entrada_invalida", [
    ("0X80442957"), # X no al final
    ("0-321-14653-A"), # Caracter ilegal
])
def test_normalize_isbn_invalid_char(entrada_invalida):
    """Prueba que la normalización lanza ValueError con caracteres ilegales."""
    with pytest.raises(ValueError):
        normalize_isbn(entrada_invalida)

# ----------------------------
# PRUEBAS DE is_valid_isbn10
# ----------------------------

@pytest.mark.parametrize("entrada, esperado", [
    ("0306406152", True),        # Válido digito
    ("0-8044-2957-X", True),     # Válido X con guiones
    ("0306406153", False),       # Inválido checksum
    ("030640615", False),        # Inválido longitud corta
    ("0-321-14653-A", False),    # Inválido caracter (falla normalización)
])
def test_is_valid_isbn10(entrada, esperado):
    assert is_valid_isbn10(entrada) == esperado

# ----------------------------
# PRUEBAS DE is_valid_isbn13
# ----------------------------

@pytest.mark.parametrize("entrada, esperado", [
    ("9780306406157", True),     # Válido
    ("978-3-16-148410-0", True), # Válido con guiones
    ("9780306406158", False),    # Inválido checksum
    ("978030640615", False),     # Inválido longitud corta
    ("97803A6406157", False),    # Inválido caracter (falla normalización)
])
def test_is_valid_isbn13(entrada, esperado):
    assert is_valid_isbn13(entrada) == esperado

# ----------------------------
# PRUEBAS DE detect_isbn
# ----------------------------

@pytest.mark.parametrize("entrada, esperado", [
    ("0306406152", VALID_ISBN10),
    ("9780306406157", VALID_ISBN13),
    ("0306406153", INVALID),       # Checksum 10 fallido
    ("9780306406158", INVALID),    # Checksum 13 fallido
    ("", INVALID),                 # Vacío
    ("123456789", INVALID),        # Longitud inválida
])
def test_detect_isbn(entrada, esperado):
    assert detect_isbn(entrada) == esperado

# ----------------------------
# PRUEBA DE DOBLE (MOCK)
# ----------------------------

def test_detect_isbn_logs_warning_on_invalid():
    """Prueba que detect_isbn llama a logger.warn() en una entrada inválida."""
    # Arrange
    mock_logger = Mock()
    invalid_input = "123"
    
    # Act
    detect_isbn(invalid_input, logger=mock_logger)
    
    # Assert
    # Verifica que el método .warn() fue llamado exactamente una vez
    mock_logger.warn.assert_called_once()
    # Verifica que fue llamado con el mensaje específico
    mock_logger.warn.assert_called_once_with(f"ISBN Inválido detectado (longitud): {invalid_input}")

# ----------------------------
# PRUEBAS DE PROPIEDADES
# ----------------------------

def test_normalization_idempotent():
    """La normalización aplicada dos veces es igual que aplicada una vez."""
    s = " 0-8044-2957-X "
    assert normalize_isbn(normalize_isbn(s)) == normalize_isbn(s)

def test_equivalent_formats_same_result():
    """ISBNs equivalentes (con/sin guiones) deben producir el mismo resultado."""
    raw = "978-0-306-40615-7"
    clean = "9780306406157"
    assert detect_isbn(raw) == detect_isbn(clean)
    assert detect_isbn(raw) == VALID_ISBN13


