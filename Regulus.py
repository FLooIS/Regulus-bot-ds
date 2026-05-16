import discord
from discord import app_commands # Новый импорт для слэш-команд
from discord.ext import commands
# Импортируем данные необходимые для защиты токена
import os
from dotenv import load_dotenv

# Загружаем данные из файла .env
load_dotenv()

# Достаем токен
TOKEN = os.getenv('DISCORD_TOKEN')

# Настройка доступов
intents = discord.Intents.default()
intents.message_content = True 

# Создание экземпляра бота
bot = commands.Bot(command_prefix='!', intents=intents)



# Добавляем событие синхронизации
@bot.event
async def on_ready():
    try:
        # Синхронизируем команды с серверами Дискорда
        synced = await bot.tree.sync()
        print(f"✅ Синхронизировано {len(synced)} слэш-команд")
        print(f"✅ Бот {bot.user} запущен!")
    except Exception as e:
        print(f"❌ Ошибка синхронизации: {e}")

# 2. Создаем слэш-команду вместо обычной
@bot.tree.command(name="calc", description="Рассчитать суммарный урон яда с акселерантом")
@app_commands.describe(poison="Текущее количество яда", stacks="Стаки акселеранта")
async def calc(interaction: discord.Interaction, poison: int, stacks: int):
    # В слэш-командах вместо ctx используется interaction
    total_ticks = min(poison, 1 + stacks)
    last_poison = poison - total_ticks + 1
    final_damage = (poison + last_poison) * total_ticks // 2
    
    await interaction.response.send_message(
        f"🧪 **Яд:** {poison} | **Акселерант:** {stacks}\n"
        f"💥 Итоговый урон: **{final_damage}**"
    )

ELITES_DATA = {
    "Заросли": [
        "Никого не встречал", 
        "Античный истукан(Bygone Effigy)", 
        "Лягуш-паразит(Phrog Parasite)", 
        "Птахоклюй(Byrdonis)"
    ],
    "Пристань": [
        "Никого не встречал", 
        "Испугорь(Terror Eel)", 
        "Копотливая колония(Skulking Colony)", 
        "Фантомный альгочист(Phantasmal Gardener)"
    ],
    "Улей": [
        "Никого не встречал",
        "Зараженная призма(Infested Prism)",
        "Скольконожка(Decimillipede)",
        "Энтомант(Entomancer)"
    ],
    "Чертог": [
        "Никого не встречал",
        "Рыцари-гниды(Knight's)",
        "Меха-Рыцарь(Mecha Knight)",
        "Чистилище душ(Soul Nexus)"
    ]
}

# Сначала создаем список биомов для выбора
BIOMES = [app_commands.Choice[str](name=name, value=name) for name in ELITES_DATA.keys()]

@bot.tree.command(name="elite", description="Узнать, кто может встретиться следующим")
@app_commands.describe(biome="Выбери текущий биом", last_elite="Кого ты встретил последним?")
@app_commands.rename(biome="локация", last_elite="предыдущая_элита") # Меняем отображение
@app_commands.choices(biome=BIOMES)
async def elite(interaction: discord.Interaction, biome: str, last_elite: str):
    # Получаем полный список для выбранного биома
    all_elites = ELITES_DATA[biome]
    
    if last_elite == "Никого не встречал":
        # Если никого не видели, доступны все, кроме самого пункта "Никого..."
        possible_elites = [e for e in all_elites if e != "Никого не встречал"]
    else:
        # Если кто-то был, исключаем его И пункт "Никого..."
        possible_elites = [e for e in all_elites if e != last_elite and e != "Никого не встречал"]
    
    response_text = f"📍 Биом: **{biome}**\n"
    response_text += f"⏭ Следующая элита может быть c 50% шансом: **{', '.join(possible_elites)}**"
    
    await interaction.response.send_message(response_text)

# Автодополнения для второго поля
@elite.autocomplete('last_elite')
async def elite_autocomplete(interaction: discord.Interaction, current: str):
    # Достаем то, что юзер УЖЕ выбрал в поле 'biome'
    biome = getattr(interaction.namespace, "локация", None)
    
    if not biome:
        return [] # Если биом не выбран, ничего не предлагаем
        
    # Берем список элит для этого биома
    choices = ELITES_DATA.get(biome, [])
    
    # Возвращаем список вариантов, которые подходят под то, что юзер начал печатать
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in choices if current.lower() in choice.lower()
    ]

@bot.tree.command(name ="password", description="Я знаю пароль, я вижу ориентир")
async def password(interaction: discord.Interaction,):
    await interaction.response.send_message("Абибиботик: ||8841||")

if TOKEN is None:
    print("❌ DISCORD_TOKEN not found in environment variables. Please check your .env file.")
else:
    bot.run(TOKEN)