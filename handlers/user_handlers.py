from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup

from callback_factories.edit_items import RegionsCallbackFactory, CountryCallbackFactory, CityCallbackFactory, \
    CharCallbackFactory, CityCallbackFactoryV2
from database.database import bot_database as db, users_db, user_dict_template
from keyboards.keyboard import create_keyboard, create_char_keyboard
from lexicon.lexicon import LEXICON
from aiogram_calendar import DialogCalendar, DialogCalendarCallback, get_user_locale
from services.parsing_aviasales import parser

router: Router = Router()


@router.message(CommandStart())
@router.message(Command(commands='help'))
async def process_start_command(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='menu'))
async def process_menu_command(message: Message):
    regions = db.getRegions()
    if regions:
        await message.answer(
            text=LEXICON['select_from_list'],
            reply_markup=create_keyboard(*regions, callback_factory=RegionsCallbackFactory)
        )
    else:
        await message.answer(text=LEXICON['no'])


@router.callback_query(RegionsCallbackFactory.filter())
async def process_edit_books_press(callback: CallbackQuery, callback_data: RegionsCallbackFactory):
    countries = db.getCountries(callback_data.id)
    if countries:
        await callback.message.answer(
            text=LEXICON['select_from_list'],
            reply_markup=create_keyboard(*countries, callback_factory=CountryCallbackFactory)
        )
    else:
        await callback.message.answer(text=LEXICON['no'])


@router.callback_query(CountryCallbackFactory.filter())
async def process_edit_books_press(callback: CallbackQuery, callback_data: CountryCallbackFactory):
    cities = db.getCitites(callback_data.id)
    if cities:
        await callback.message.answer(
            text=LEXICON['select_from_list'],
            reply_markup=create_keyboard(*cities, callback_factory=CityCallbackFactory)
        )
    else:
        await callback.message.answer(text=LEXICON['no'])


@router.callback_query(CityCallbackFactory.filter())
async def get_departure_char_city(callback: CallbackQuery, callback_data: CityCallbackFactory):
    destination_city_abbr = db.getDesCity(callback_data.id)
    users_db[callback.from_user.id]['destination_city'] = destination_city_abbr[0] if destination_city_abbr else None
    rus_cities_chars = db.getRussianCitiesFirstChar()
    if rus_cities_chars:
        await callback.message.answer(
            text=LEXICON['select_from_list'] + 'первую букву города, откуда собираетесь улетать',
            reply_markup=create_char_keyboard(*map(lambda x: x[0], rus_cities_chars))
        )
    else:
        await callback.message.answer(text=LEXICON['no'])


@router.callback_query(CharCallbackFactory.filter())
async def get_departure_city(callback: CallbackQuery, callback_data: CharCallbackFactory):
    cities = db.getRussianCities(callback_data.char)
    if cities:
        await callback.message.answer(
            text=LEXICON['select_from_list'],
            reply_markup=create_keyboard(*cities, callback_factory=CityCallbackFactoryV2)
        )
    else:
        await callback.message.answer(text=LEXICON['no'])


@router.callback_query(CityCallbackFactoryV2.filter())
async def process_departure_city(callback: CallbackQuery, callback_data: CityCallbackFactoryV2):
    departure_city_abbr = db.getDesRusCity(callback_data.id)
    users_db[callback.from_user.id]['departure_city'] = departure_city_abbr[0] if departure_city_abbr else None
    kb = [[KeyboardButton(text='Календарь')]]
    start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await callback.message.reply(f"Выберите календарь", reply_markup=start_kb)


@router.message(F.text.lower() == 'календарь')
async def dialog_cal_handler(message: Message):
    await message.answer(
        "Please select a date: ",
        reply_markup=await DialogCalendar(
            locale=await get_user_locale(message.from_user)
        ).start_calendar()
    )


@router.callback_query(DialogCalendarCallback.filter())
async def process_dialog_calendar(callback: CallbackQuery, callback_data: DialogCalendarCallback):
    selected, date = await DialogCalendar(
        locale=await get_user_locale(callback.from_user)
    ).process_selection(callback, callback_data)
    if selected:
        users_db[callback.from_user.id]['date'] = date.strftime("%Y-%m-%d")
        user = users_db[callback.from_user.id]
        await callback.message.answer(
            '\n'.join(parser.display_tickets_info(user['departure_city'], user['destination_city'], user['date']))
        )

