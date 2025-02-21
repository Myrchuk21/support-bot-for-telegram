import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = "bot token"
ADMIN_ID = user id  # Замените на ID администратора

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Храним соответствие сообщений пользователей
user_messages = {}

# Обработка сообщений от пользователей
async def handle_user_message(message: Message):
    user_id = message.from_user.id

    # Отправляем админу уведомление + текст сообщения
    forwarded_msg = await bot.send_message(
        ADMIN_ID,
        f"📩 Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}"
    )
    
    # Сохраняем связь сообщения с пользователем
    user_messages[forwarded_msg.message_id] = user_id

# Обработка ответов от администратора
async def handle_admin_reply(message: Message):
    if message.chat.id != ADMIN_ID:
        return  # Если сообщение не от админа, игнорируем

    if not message.reply_to_message:
        await message.reply("❌ Ответьте на сообщение с уведомлением, чтобы отправить ответ пользователю.")
        return

    # Проверяем, есть ли связь с пользователем
    original_message_id = message.reply_to_message.message_id
    user_id = user_messages.get(original_message_id)

    if not user_id:
        await message.reply("⚠ Не удалось определить, кому отправить сообщение.")
        return

    # Отправляем ответ пользователю
    await bot.send_message(user_id, f"📢 <b>Ответ от администратора:</b>\n{message.text}")

# Регистрируем обработчики
dp.message.register(handle_user_message, lambda msg: msg.chat.id != ADMIN_ID)  # Для пользователей
dp.message.register(handle_admin_reply, lambda msg: msg.chat.id == ADMIN_ID)  # Для админа

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
