import enum

from utils.misc_functions import get_random_item


class BaseEnum(enum.Enum):

    @classmethod
    def name_in_enum(cls, name):
        return name.upper() in cls.get_names()

    @classmethod
    def get_name_by_value(cls, value):
        return cls(value).name

    @classmethod
    def value_in_enum(cls, value):
        return value in cls.get_values()

    @classmethod
    def get_names(cls):
        return [x.name for x in cls if x.name.isupper()]

    @classmethod
    def get_values(cls):
        return [x.value for x in cls]

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_random(cls):
        return get_random_item(cls.get_names())
