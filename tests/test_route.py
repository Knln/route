import pytest


def test_root_page(app):

    client = app.test_client()
    response = client.get("/")
    assert b"Welcome to the home page" in response.data


def test_json_data_path(app):
    client = app.test_client()
    response = client.post("/path", json={
        "path": "hello515",
        "res": "hefewf8o28orllo5"
    })

    print(response.data)

    assert response.status_code == 200
    assert response.get_data() == b'{"status":"ok"}\n'


if __name__ == '__main__':
    pytest.main()
