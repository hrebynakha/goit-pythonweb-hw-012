# test_integration_contacts.py - Integration tests for contacts API endpoints

contact_data = {
    "first_name": "test_first_name",
    "last_name": "test_last_name",
    "email": "test_contact@email.com",
}


def test_create_contact(client, get_token):
    response = client.post(
        "/api/contacts",
        json=contact_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == "test_first_name"
    assert data["last_name"] == "test_last_name"
    assert data["email"] == "test_contact@email.com"
    assert "id" in data


def test_get_contact(client, get_token):
    response = client.get(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "test_first_name"
    assert data["last_name"] == "test_last_name"
    assert data["email"] == "test_contact@email.com"
    assert "id" in data


def test_get_contact_not_found(client, get_token):
    response = client.get(
        "/api/contacts/2", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"


def test_get_contacts(client, get_token):
    response = client.get(
        "/api/contacts", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["first_name"] == "test_first_name"
    assert data[0]["last_name"] == "test_last_name"
    assert data[0]["email"] == "test_contact@email.com"
    assert "id" in data[0]


def test_update_contact(client, get_token):
    response = client.put(
        "/api/contacts/1",
        json={
            "first_name": "new_test_first_name",
            "last_name": "new_test_last_name",
            "email": "new_test_contact@email.com",
        },
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "new_test_first_name"
    assert data["last_name"] == "new_test_last_name"
    assert data["email"] == "new_test_contact@email.com"
    assert "id" in data


def test_update_contact_not_found(client, get_token):
    response = client.put(
        "/api/contacts/2",
        json={
            "first_name": "new_test_first_name",
            "last_name": "new_test_last_name",
            "email": "new_test_contact@email.com",
        },
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"


def test_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "new_test_first_name"
    assert data["last_name"] == "new_test_last_name"
    assert data["email"] == "new_test_contact@email.com"
    assert "id" in data


def test_repeat_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"
