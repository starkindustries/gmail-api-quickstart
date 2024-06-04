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

def hello_world():
    return "Hello, World!"

def test_hello_world():
    assert hello_world() == "Hello, World!"

def test_get_all_labels():
    service = quickstart.get_api_service_obj()
    labels = quickstart.get_all_labels(service)    
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
    
    