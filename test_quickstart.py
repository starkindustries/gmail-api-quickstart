import os

def test_github_secrets():
    # Note: reminder to add this env variable locally for this test to pass on local machine
    my_secret = os.getenv('MY_TEST_SECRET')
    assert my_secret == "this_is_some_super_secret_info"

def hello_world():
    return "Hello, World!"

def test_hello_world():
    assert hello_world() == "Hello, World!"
