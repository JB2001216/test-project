from app_messages.models import Message


def test_create_message(authenticated_client, user2):
    message = authenticated_client.post(
        "/messages/", {"to_user": user2.id, "title": "test title", "text": "test_text"}
    )
    assert message.status_code == 201
    assert message.json()["title"] == "test title"
    assert message.json()["text"] == "test_text"


def test_create_message_error(authenticated_client, client):
    message = authenticated_client.post(
        "/messages/", {"to_user": 5, "title": "test title", "text": "test_text"}
    )
    assert message.status_code == 400
    assert "to_user" in message.json()

    error_message = client.get("/messages_errors/")
    assert error_message.status_code == 200


def test_delete_message(authenticated_client, user2, authenticated_client2):
    message = authenticated_client.post(
        "/messages/", {"to_user": user2.id, "title": "test title", "text": "test_text"}
    )
    assert message.status_code == 201
    message = Message.objects.last()

    # test delete permissions

    delete_message_with_not_permissions = authenticated_client2.delete(
        f"/messages/{message.id}/"
    )

    assert (
        delete_message_with_not_permissions.json()["detail"]
        == "You do not have permission to perform this action."
    )
    assert delete_message_with_not_permissions.status_code == 403

    delete_message = authenticated_client.delete(f"/messages/{message.id}/")

    assert delete_message.status_code == 204
    assert Message.objects.count() == 0


def test_inbox(authenticated_client, user2):
    message = authenticated_client.post(
        "/messages/", {"to_user": user2.id, "title": "test title", "text": "test_text"}
    )
    assert message.status_code == 201