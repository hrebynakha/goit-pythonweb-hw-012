from unittest.mock import patch

from tests.conftest import test_user, test_admin_user


def test_get_me(client, get_token):
    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("api/users/me", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "avatar" in data


@patch("src.services.fs.UploadFileService.upload_file")
def test_update_avatar_user_role_user(mock_upload_file, client, get_token):

    fake_url = "<http://example.com/avatar.jpg>"
    mock_upload_file.return_value = fake_url

    headers = {"Authorization": f"Bearer {get_token}"}

    file_data = {"file": ("avatar.jpg", b"fake image content", "image/jpeg")}

    response = client.patch("/api/users/avatar", headers=headers, files=file_data)

    assert response.status_code == 403, response.text

    data = response.json()
    assert data["detail"] == "Access denied"


@patch("src.services.fs.UploadFileService.upload_file")
def test_update_avatar_user_role_admin(mock_upload_file, client, get_admin_token):

    fake_url = "<http://example.com/avatar.jpg>"
    mock_upload_file.return_value = fake_url

    headers = {"Authorization": f"Bearer {get_admin_token}"}

    file_data = {"file": ("avatar.jpg", b"fake image content", "image/jpeg")}

    response = client.patch("/api/users/avatar", headers=headers, files=file_data)

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["username"] == test_admin_user["username"]
    assert data["email"] == test_admin_user["email"]
    assert data["avatar"] == fake_url

    mock_upload_file.assert_called_once()


@patch("src.services.fs.UploadFileService.upload_file")
def test_update_avatar_fail_user_role_admin(mock_upload_file, client, get_admin_token):
    mock_upload_file.return_value = None

    headers = {"Authorization": f"Bearer {get_admin_token}"}

    file_data = {"file": ("avatar.jpg", b"fake image content", "image/jpeg")}

    response = client.patch("/api/users/avatar", headers=headers, files=file_data)

    assert response.status_code == 400, response.text

    data = response.json()
    assert data["detail"] == "File not uploaded successfully"

    mock_upload_file.assert_called_once()
