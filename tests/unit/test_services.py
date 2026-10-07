from app.services import toggle_state, validate_title


def test_title_is_trimmed():
    assert validate_title('  Repasar Git  ') == 'Repasar Git'


def test_pending_can_be_completed():
    assert toggle_state(False) is True
