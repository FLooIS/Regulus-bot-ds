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

# 1. Сначала создаем список биомов для выбора
BIOMES = [app_commands.Choice(name=name, value=name) for name in ELITES_DATA.keys()]

@bot.tree.command(name="elite", description="Узнать, кто может встретиться следующим")
@app_commands.choices(biome=BIOMES) # Пользователь выбирает из ваших 4-х биомов
async def elite(interaction: discord.Interaction, biome: str, last_elite: str):
    # Здесь будет логика ответа
    # Нам нужно исключить ту элитку, которую ввел пользователь (last_elite)
    possible_elites = [e for e in ELITES_DATA[biome] if e != last_elite and e != "Никого не встречал"]
    
    await interaction.response.send_message(
        f"📍 Биом: **{biome}**\n"
        f"⏭ Следующая элита может быть: **{', '.join(possible_elites)}**"
    )

# 2. А теперь — магия автодополнения для второго поля
@elite.autocomplete('last_elite')
async def elite_autocomplete(interaction: discord.Interaction, current: str):
    # Достаем то, что юзер УЖЕ выбрал в поле 'biome'
    biome = interaction.namespace.biome
    
    if not biome:
        return [] # Если биом не выбран, ничего не предлагаем
        
    # Берем список элит для этого биома
    choices = ELITES_DATA.get(biome, [])
    
    # Возвращаем список вариантов, которые подходят под то, что юзер начал печатать
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in choices if current.lower() in choice.lower()
    ]