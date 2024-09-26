import pytest
import requests

def test_homepage():
    header = {
        'Content-Type': 'application/json'
    }
    base_url = 'http://localhost:5000/'

    resp = requests.get(url = base_url)

    assert resp.status_code == 200