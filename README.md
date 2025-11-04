# Proyecto Integrador: Validador de ISBN

## Descripción del Módulo

El módulo `isbn.py` provee 4 funciones públicas:
* `normalize_isbn(s)`: Limpia la cadena de entrada.
* `is_valid_isbn10(s)`: Valida según la regla de checksum módulo 11.
* `is_valid_isbn13(s)`: Valida según la regla de checksum módulo 10.
* `detect_isbn(s)`: Devuelve "ISBN-10", "ISBN-13" o "INVALID".

## Decisiones y Supuestos

**Caracteres:** Solo se aceptan dígitos, espacios, guiones y la 'X' (mayúscula) al final de un ISBN-10[cite: 47]. [cite_start]Cualquier otro caracter (incluyendo 'x' minúscula o prefijos como "ISBN:") causará un `ValueError` durante la normalización[cite: 46].
* **Logger:** El módulo es puramente funcional. [cite_start]Se añadió un `logger` opcional a `detect_isbn` únicamente para cumplir con el requisito académico de demostrar el uso de *mocks*[cite: 108].

## Cómo Ejecutar Pruebas y Cobertura

1.  Asegúrate de tener `pytest` y `pytest-cov` instalados:
    ```bash
    pip install pytest pytest-cov
    ```

2.  Ejecuta la suite de pruebas:
    ```bash
    pytest
    ```

3.  [cite_start]Ejecuta las pruebas y genera el reporte de cobertura en la terminal:
    ```bash
    pytest --cov=isbn --cov-report term-missing
    ```

4.  (Opcional) Genera un reporte de cobertura en HTML:
    ```bash
    pytest --cov=isbn --cov-report=html
    ```
    Luego, abre `htmlcov/index.html` en tu navegador.
