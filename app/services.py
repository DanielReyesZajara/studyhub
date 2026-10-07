"""Reglas de negocio sin dependencias de Flask ni de la base de datos."""

def validate_title(value):
    if not isinstance(value, str):
        raise ValueError('El título debe ser texto.')
    title = value.strip()
    if not 1 <= len(title) <= 120:
        raise ValueError('El título debe tener entre 1 y 120 caracteres.')
    return title


def validate_description(value):
    if not isinstance(value, str):
        raise ValueError('La descripción debe ser texto.')
    description = value.strip()
    if len(description) > 500:
        raise ValueError('La descripción no puede superar 500 caracteres.')
    return description


def toggle_state(completed):
    return True
