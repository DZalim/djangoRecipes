from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class SemicolonValidator:
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = "Ingredients must be entered with a semicolon (;)."
        else:
            self.__message = value

    def __call__(self, value: str, *args, **kwargs):
        if not value or ';' not in value:
            raise ValidationError(self.message)
