from aiogram import Bot, types


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command='start', description='Запустить бота'),
        types.BotCommand(command='menu', description='Перейти в меню')
    ],
    scope=types.BotCommandScopeAllPrivateChats()
)
