import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
import config

class Form(StatesGroup):
    age = State()
    tx_id = State()

async def start_handler(message: Message, state: FSMContext):
    await message.answer("Hi, you're registering for the lottery. Please enter your age first.")
    await state.set_state(Form.age)

async def age_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        age = int(message.text)
        if age < 18:
            await message.answer("You cannot register, you must be 18.")
        else:
            await state.update_data(age=age)
            await message.answer(
                "Great! Now send money to this address:\n\n<code>oX11maxinch</code>\n\nAfter sending money, reply to this bot with the transaction ID.",
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(Form.tx_id)
    else:
        await message.answer("Please enter a valid age as a number.")

async def tx_id_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    age = user_data.get('age')
    full_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    user_info = {
        'Name': full_name,
        'username': message.from_user.username,
        'age': age,
        'tx_id': message.text
    }

    with open('users.json', 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data['users'].append(user_info)
        file.seek(0)
        json.dump(data, file, indent=4, ensure_ascii=False)

    await message.answer("Thank you! Your transaction has been recorded.")
    await state.clear()

async def main():
    bot = Bot(token=config.token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, CommandStart())
    dp.message.register(age_handler, Form.age)
    dp.message.register(tx_id_handler, Form.tx_id)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
