import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runuser_actions", action="store_true", default=False, help="run tests with UI interactions"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "user_action: mark test as requiring a user action to complete")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runuser_actions"):
        # --runuser_actions given in cli: do not skip UI tests
        return
    skip_ui = pytest.mark.skip(reason="need --runuser_actions option to run")
    for item in items:
        if "user_action" in item.keywords:
            item.add_marker(skip_ui)