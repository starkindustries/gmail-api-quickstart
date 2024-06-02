import os
from quickstart import *

def test_github_secrets():
    # Note: reminder to add this env variable locally for this test to pass on local machine
    # export MY_TEST_SECRET=this_is_some_super_secret_info
    my_secret = os.getenv('MY_TEST_SECRET')
    assert my_secret == "this_is_some_super_secret_info"

def hello_world():
    return "Hello, World!"

def test_hello_world():
    assert hello_world() == "Hello, World!"

def test_get_all_labels():
    service = get_api_service_obj()
    labels = get_all_labels(service)    
    label_names = [label["name"] for label in labels]
    expected_labels = ["CHAT", "SENT", "INBOX", "IMPORTANT", "TRASH", "DRAFT", "SPAM", 
            "CATEGORY_FORUMS", "CATEGORY_UPDATES", "CATEGORY_PERSONAL", 
            "CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "STARRED", "UNREAD"]
    for expected_label in expected_labels:
        assert expected_label in label_names