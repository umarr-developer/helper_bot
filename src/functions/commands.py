from aiogram import Bot, types


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command='start', description='Запустить бота'),
        types.BotCommand(command='menu', description='Перейти в меню'),
        types.BotCommand(command='about', description='Показать информацию о боте'),
        types.BotCommand(command='faq', description='Ответы на часто задаваемые вопросы')
    ],
        scope=types.BotCommandScopeAllPrivateChats()
    )
