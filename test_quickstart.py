import os
import random
import quickstart


def test_github_secret():
    """
    Test github secret 'MY_TEST_SECRET' to verify that secrets are stored in env vars
    https://github.com/starkindustries/gmail-api-quickstart/settings/secrets/actions
    """
    # Note: reminder to add this env variable locally for this test to pass on local machine
    # export MY_TEST_SECRET=this_is_some_super_secret_info
    my_secret = os.getenv('MY_TEST_SECRET')
    assert my_secret == "this_is_some_super_secret_info"


def test_list_labels():
    service = quickstart.get_api_service_obj()
    labels = quickstart.list_labels(service)    
    label_names = [label["name"] for label in labels]
    expected_labels = ["CHAT", "SENT", "INBOX", "IMPORTANT", "TRASH", "DRAFT", "SPAM", 
            "CATEGORY_FORUMS", "CATEGORY_UPDATES", "CATEGORY_PERSONAL", 
            "CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "STARRED", "UNREAD"]
    for expected_label in expected_labels:
        assert expected_label in label_names


def test_create_and_delete_label():
    service = quickstart.get_api_service_obj()
    randnum = random.randint(1000, 9999)
    label_name = "foo" + str(randnum)
    new_label = quickstart.create_label(service, label_name)
    print(f"{new_label=}")
    assert new_label["name"] == label_name
    assert quickstart.delete_label(service, new_label["id"])


def test_list_messages():
    service = quickstart.get_api_service_obj()
    messages = quickstart.list_messages(service)
    assert messages

    test_message = {
        "Subject": "test email 001",
        "From": "testuser9448@gmail.com",
        "To": "testuser9448@gmail.com",
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    }
    
    for message in messages:
        message_data = quickstart.get_full_message(service, message['id'])

        if message_data["headers"]["Subject"] == test_message["Subject"]:
            assert test_message["From"] in message_data["headers"]["From"]
            assert test_message["To"] in message_data["headers"]["To"]
            
            # Remove the line breaks from the message
            message_body = message_data["body"].replace('\r\n', ' ').replace('\n', ' ').strip()
            assert test_message["body"] == message_body


def test_apply_label_to_message():
    service = quickstart.get_api_service_obj()
    messages = quickstart.list_messages(service)
    assert messages

    # Create new random label
    randnum = random.randint(1000, 9999)
    label_name = "foo" + str(randnum)
    new_label = quickstart.create_label(service, label_name)

    # Find test email 002
    for message in messages:
        message_data = quickstart.get_full_message(service, message['id'])
        if message_data["headers"]["Subject"] == "test email 002":
            result_message = quickstart.apply_label(service, 'me', message['id'], new_label['id'])
            assert new_label["id"] in result_message["labelIds"]
    
    # Clean-up: delete random label
    assert quickstart.delete_label(service, new_label["id"])
