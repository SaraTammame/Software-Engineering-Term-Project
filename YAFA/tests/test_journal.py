from datetime import datetime
import pytest
from app.model.journal import Journal
from app.model.user import insert_user_data
from sqlalchemy.exc import IntegrityError

def test_max_word_count(client):
    # Generate a log with 250 words (should succeed)
    log_250 = 'word ' * 250
    response = client.post('/journal', data={
        'user_id': 1,
        'entry_title': 'Max Word Test',
        'entry_content': log_250,
        'entry_date': '2025-07-15'
    })
    assert response.status_code == 200 or response.status_code == 302

    # Generate a log with 251 words (should fail)
    log_251 = 'word ' * 251
    response = client.post('/journal', data={
        'user_id': 1,
        'entry_title': 'Over Max Word Test',
        'entry_content': log_251,
        'entry_date': '2025-07-15'
    })
    assert b'word limit' in response.data or response.status_code == 400

def test_journal_empty_content(client):
    response = client.post('/journal', data={
        'user_id': 1,
        'entry_title': 'Empty Content Test',
        'entry_content': '',
        'entry_date': '2025-07-15'
    })
    # Expect a 400 Bad Request or an error message in the response
    assert b'Content is required.' in response.data or response.status_code == 400