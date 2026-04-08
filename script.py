import json


def main():
    while True:
        try:
            map_name = input("Map: ").lower().strip()
            kills = int(input("Kills: "))
            death = int(input("Death: "))
            assist = int(input("Help (Assists): "))
            hs_percent = int(input("Head shot %: "))
            damage = int(input("Damage: "))

            break
        except ValueError:
            print("Ошибка: пожалуйста, вводи только числа!\n")

    if death > 0:
        kd = kills / death
    else:
        kd = float(kills)  # Защита от деления на ноль

    print("\n--- Итоги матча ---")
    print()
    print(f"K/D: {kd:.2f}")
    print(f"K/A/D: {kills}/{assist}/{death}")
    print(f"Headshots: {hs_percent}%")
    print(f"Урон: {damage}")

    match_result = {
        "map": map_name,
        "kills": kills,
        "deaths": death,
        "assists": assist,
        "kd": round(kd, 2),
        "hs": hs_percent,
        "damage": damage
    }

    with open("stats.json", "a") as file:
        json.dump(match_result, file)
        file.write("\n")

    print("saved!")


def show_stats():
    print("\n--- Твоя общая статистика ---")

    total_kills = 0
    total_deaths = 0
    total_damage = 0
    total_wins = 0
    total_losses = 0
    games_count = 0

    try:
        with open("stats.json", "r") as file:
            for line in file:
                if line.strip():
                    data = json.loads(line)

                    # Прибавляем данные из текущего матча к общим
                    total_kills += data["kills"]
                    total_deaths += data["deaths"]
                    total_damage += data.get("damage", 0)  # .get на случай если в старых записях нет урона
                    total_wins += data["wins"]
                    total_losses += data["losses"]
                    games_count += 1

        # После того как цикл прошел по ВСЕМ строкам, считаем среднее
        if games_count > 0:
            overall_kd = total_kills / total_deaths if total_deaths > 0 else total_kills
            avg_damage = total_damage / games_count

            print(f"Всего игр: {games_count}")
            print(f"Общий K/D: {overall_kd:.2f}")
            print(f"Всего убийств: {total_kills}")
            print(f"Средний урон за матч: {avg_damage:.0f}")
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
        main()
    elif choice == "2":
        show_stats()
    elif choice == "3":
        print("Пока!")
        break
    else:
        print("Нажми 1, 2 или 3!")