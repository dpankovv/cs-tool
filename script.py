import json

MAPS = ["de_dust2", "de_mirage", "de_inferno", "de_nuke", "de_anubis", "de_ancient", "de_vertigo"]

def load_stats(data):
    try:
        with open("stats.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_stats(data):

    with open("stats.json", "a", encoding="utf-8") as file:
            # Превращаем словарь в строку (S - string)
        json_line = json.dumps(data, ensure_ascii=False)
            # Записываем эту строку в файл и переходим на новую
        file.write(json_line + "\n")
    print("saved!")

def calculate_avg_damage(matches):
    if not matches:
        return 0

    total_dmg = 0
    for match in matches:
        # Важно: ключ в кавычках должен быть таким же, как в твоем JSON
        total_dmg += match.get("damage", 0)

        # Делим сумму на количество элементов в списке
    avg = total_dmg / len(matches)
    return round(avg)


def calculate_kd(kills, death):
    if death <= 0:
        return float(kills)
    return round(kills / death, 2) #2 это кол. знаков после точки


def user_inp():
    while True:
        wdl = input("Match result (W, L, =): ").upper().strip()
        if wdl in ["W", "L", "="]: break
        else:
            print("Ошибка! Можно ввести только W, L или =.")

    while True:
        try:
            while True:
                try:
                    print("\nMap:")
                    # цикл пронумировывает карты
                    for i, name in enumerate(MAPS, 1):
                        print(f"{i}. {name}")

                    # Просим нажать цифру
                    choice_idx = int(input("Введите номер карты: "))

                    # превращает цифру в название (минус 1, так как в коде счет с нуля)
                    map_name = MAPS[choice_idx - 1]
                    print(f"Выбрана карта: {map_name}")
                    break
                except ValueError:
                    print("Error")

            while True:
                try:
                    kills = int(input("Kills: "))
                    if kills >= 20:
                        print("он в прайме")
                    elif kills <= 10:
                        print("Пу пу пу....")
                    break
                except ValueError:
                    print("Error")

            while True:
                try:
                    death = int(input("Death: "))
                    break
                except ValueError:
                    print("скико?")
            while True:
                try:
                    assist = int(input("Help (Assists): "))
                    if assist >= 10:
                        print("помогатор")
                        break
                except ValueError:
                    print("Error")

            while True:
                try:
                    hs_percent = int(input("Head shot %: "))
                    break
                except ValueError:
                    print("Error")

            while True:
                try:
                    damage = int(input("Damage: "))
                    break
                except ValueError:
                        print("Error")
        except ValueError:
            print("Error")

        wins = 0
        losses = 0
        draws = 0

        if wdl == "W":
            wins = 1
        elif wdl == "L":
            losses = 1
        elif wdl == "=":
            draws = 1

        kd = calculate_kd(kills, death) # вызов функции кд

        print("\n--- Итоги матча ---")
        print(f"Result: {wdl}")
        print(f"K/D: {kd:.2f}")
        print(f"K/A/D: {kills}/{assist}/{death}")
        print(f"Headshots: {hs_percent}%")
        print(f"Урон: {damage}")

        match_result = {
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "map": map_name,
            "kills": kills,
            "deaths": death,
            "assists": assist,
            "kd": round(kd, 2),
            "hs": hs_percent,
            "damage": damage
        }

        save_stats(match_result)

        return


def show_stats(filter_map=None):
    print("\n--- Твоя общая статистика ---")



    total_kills = 0
    total_deaths = 0
    total_damage = 0
    total_wins = 0
    total_draws = 0
    total_losses = 0
    games_count = 0

    try:
        with open("stats.json", "r") as file:
            for line in file:
                if line.strip():
                    data = json.loads(line)

                    if filter_map and data.get("map") != filter_map:
                        continue

                    total_kills += data["kills"]
                    total_deaths += data["deaths"]
                    total_damage += data.get("damage", 0)
###################################################################
                    total_wins += data["wins"]
                    total_draws += data["draws"]
                    total_losses += data["losses"]
                    games_count += 1

        if games_count > 0:
            final_kd = calculate_kd(total_kills, total_deaths)
            avg_damage = total_damage / games_count

            print(f"Результат: W-{total_wins}, L-{total_losses}, D-{total_draws}")
            print(f"Всего игр: {games_count}")
            print(f"Общий K/D: {final_kd}")
            print(f"Всего убийств: {total_kills}")
            print(f"Средний урон за матч: {round(avg_damage)}")

        else:
            print("Матчей пока нет.")

    except FileNotFoundError:
        print("База данных пуста.")



while True:
    print("\n--- CS2 Tracker ---")
    print("1. Добавить матч")
    print("2. Посмотреть статистику")
    print("3. Выйти")

    choice = input("Выбери действие: ")

    if choice == "1":
        user_inp()
    elif choice == "2":
        print("\n1. Общая статистика\n2. По картам")
        sub_choice = input("Твой выбор: ")

        if sub_choice == "1":
            show_stats()  # Фильтр не передаем
        elif sub_choice == "2":
            print("\nКакую карту смотрим?")
            for i, m in enumerate(MAPS, 1): #enumerate берет список и делает из него пары: (номер, значение).
                print(f"{i}. {m}")

            m_idx = int(input("Номер карты: ")) - 1
            show_stats(MAPS[m_idx])

    elif choice == "3":
        print("Пока!")
        break
    else:
        print("Нажми 1, 2 или 3!")

