from aiogram.filters.callback_data import CallbackData


class RegionsCallbackFactory(CallbackData, prefix='regions'):
    id: int
    item: str


class CountryCallbackFactory(CallbackData, prefix='country'):
    id: int
    item: str


class CityCallbackFactory(CallbackData, prefix='city'):
    id: int
    item: str


class CityCallbackFactoryV2(CallbackData, prefix='city_v2'):
    id: int
    item: str


class CharCallbackFactory(CallbackData, prefix='char'):
    char: str
