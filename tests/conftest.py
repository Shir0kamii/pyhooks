import pytest

import pyhooks


@pytest.fixture
def mother_class():
    class Mother:
        @pyhooks.Hook
        def method(self):
            self.method_run = True
    return Mother


@pytest.fixture
def child_class(mother_class):
    class Child(mother_class):
        @pyhooks.precall_register("method")
        def precall(self):
            self.precall_run = True

        @pyhooks.postcall_register("method")
        def postcall(self):
            self.postcall_run = True
    return Child


@pytest.fixture
def method(child_class):
    return child_class.precall
