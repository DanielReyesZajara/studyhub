from app.services import toggle_state

def test_completed_can_be_reopened():
    assert toggle_state(True) is False