"""Практична робота: вбудовані колекції Python.

Запуск: python main.py
Зовнішні залежності не потрібні. Дані демонстрацій детерміновані;
вимірювання часу залежать від комп'ютера та фонових процесів.
"""

from __future__ import annotations

import csv
import platform
import re
import statistics
import sys
import timeit
from pathlib import Path
from typing import Callable, TypeVar


T = TypeVar("T")
OUTPUT_DIRECTORY = Path(__file__).resolve().parent
BENCHMARK_CSV = OUTPUT_DIRECTORY / "benchmark_results.csv"
SAMPLE_TEXT_PATH = OUTPUT_DIRECTORY / "sample_text.txt"


def print_section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def task_1_lists() -> None:
    print_section("ЗАВДАННЯ 1. СПИСКИ: ІНДЕКСАЦІЯ, ЗРІЗИ ТА МУТАЦІЇ")

    numbers = [12, 7, 25, 7, 31, 18, 42, 5]
    print(f"Початковий список: {numbers}")
    print(f"Додатний індекс [2]: {numbers[2]}")
    print(f"Від'ємний індекс [-1]: {numbers[-1]}")

    print(f"Зріз [1:6]: {numbers[1:6]}")
    print(f"Зріз [:8:2] (крок 2): {numbers[:8:2]}")
    print(f"Зріз [-6:-1:2]: {numbers[-6:-1:2]}")

    alias = numbers
    copied_slice = numbers[1:4]
    copied_concat = numbers + [50]
    print(f"alias is numbers: {alias is numbers} (нового списку немає)")
    print(f"Зріз створив окремий список: {copied_slice}; той самий об'єкт: {copied_slice is numbers}")
    print(f"Конкатенація створила окремий список: {copied_concat}; той самий об'єкт: {copied_concat is numbers}")

    numbers.append(99)
    print(f"Після append(99), мутація на місці: {numbers}")
    numbers.insert(2, 15)
    print(f"Після insert(2, 15), мутація на місці: {numbers}")
    numbers.remove(7)
    print(f"Після remove(7) (видалено перше входження), мутація на місці: {numbers}")
    print(f"Фінальний список через alias: {alias}")


def unpack_inventory_record(record: tuple[int, str, int, float]) -> tuple[int, str, int, float]:
    """Повертає окремі поля після явного розпакування кортежу."""
    item_id, name, quantity, unit_price = record
    return item_id, name, quantity, unit_price


def total_inventory_value(records: list[tuple[int, str, int, float]]) -> float:
    """Повертає загальну облікову вартість у гривнях."""
    return sum(quantity * unit_price for _, _, quantity, unit_price in records)


def task_2_tuples() -> None:
    print_section("ЗАВДАННЯ 2. КОРТЕЖІ ТА ВКЛАДЕНІ МУТАБЕЛЬНІ ОБ'ЄКТИ")

    # Порядок полів: (ідентифікатор, назва, кількість, ціна за одиницю у грн).
    inventory: list[tuple[int, str, int, float]] = [
        (101, "Папір А4", 12, 149.90),
        (102, "Ручка синя", 30, 18.50),
        (103, "Папка", 8, 42.00),
    ]
    print("Записи (поля виведені після розпакування кортежу):")
    print("ID    Назва              Поля")
    for record in inventory:
        item_id, name, quantity, unit_price = unpack_inventory_record(record)
        print(f"{item_id:<5} {name:<18} кількість={quantity:<3} ціна={unit_price:>7.2f} грн")
    print(f"Загальна вартість: {total_inventory_value(inventory):.2f} грн")

    student_record: tuple[int, str, list[int]] = (201, "Іваненко", [90, 85, 95])
    print(f"Кортеж із вкладеним списком до змін: {student_record}")
    try:
        student_record[0] = 202  # type: ignore[index]
    except TypeError as error:
        print(f"Присвоєння за індексом заборонено: {type(error).__name__}")
    student_record[2].append(100)
    print(f"Після зміни вкладеного списку: {student_record}")
    print("Незмінними лишилися елементи кортежу як посилання; сам вкладений список змінюється.")


WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", flags=re.UNICODE)


def tokenize_and_normalize(text: str) -> list[str]:
    """Слова — послідовності Unicode-літер; внутрішній апостроф зберігається.

    Регістр ігнорується через casefold; розділові знаки, цифри та підкреслення
    відкидаються. Дефіс розділяє сусідні слова.
    """
    return [match.casefold() for match in WORD_PATTERN.findall(text)]


def count_words(text: str) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for word in tokenize_and_normalize(text):
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def task_3_dictionaries() -> None:
    print_section("ЗАВДАННЯ 3. СЛОВНИК ЧАСТОТ")

    sample_text = SAMPLE_TEXT_PATH.read_text(encoding="utf-8")
    frequencies = count_words(sample_text)
    missing_word = "відсутнє"
    print("Текст для підрахунку:")
    print(sample_text)
    print("Правило: Unicode-слова, casefold(), розділові знаки вилучаються.")
    print(f"Безпечне отримання відсутнього ключа {missing_word!r}: {frequencies.get(missing_word, 0)}")

    frequent_words = {word: count for word, count in frequencies.items() if count >= 2}
    print("Частоти за абеткою:")
    for word, count in sorted(frequencies.items(), key=lambda pair: pair[0]):
        print(f"  {word}: {count}")
    print("Частоти за спаданням (при однаковій частоті — за абеткою):")
    for word, count in sorted(frequencies.items(), key=lambda pair: (-pair[1], pair[0])):
        print(f"  {word}: {count}")
    print(f"Похідний словник частот >= 2 (dict comprehension): {dict(sorted(frequent_words.items()))}")


def task_4_sets() -> None:
    print_section("ЗАВДАННЯ 4. МНОЖИНИ ТА УНІКАЛЬНІ ІДЕНТИФІКАТОРИ")

    identifiers_a = ["STU-001", "STU-002", "STU-003", "STU-003", "STU-005"]
    identifiers_b = ["STU-002", "STU-004", "STU-005", "STU-005", "STU-006"]
    identifiers_c = ["STU-001", "STU-002"]
    set_a, set_b, set_c = set(identifiers_a), set(identifiers_b), set(identifiers_c)

    print(f"Колекція A: {identifiers_a} -> унікальні: {sorted(set_a)}")
    print(f"Колекція B: {identifiers_b} -> унікальні: {sorted(set_b)}")
    print(f"Колекція C: {identifiers_c} -> унікальні: {sorted(set_c)}")
    print(f"Перетин A і B: {sorted(set_a & set_b)}")
    print(f"Об'єднання A і B: {sorted(set_a | set_b)}")
    print(f"Симетрична різниця A і B: {sorted(set_a ^ set_b)}")
    print(f"C <= A (істинне твердження): {set_c <= set_a}")
    print(f"B <= A (хибне твердження): {set_b <= set_a}")

    frozen_pair = frozenset({"STU-001", "STU-002"})
    groups_by_members = {frozen_pair: "навчальна пара 1"}
    print(f"frozenset як ключ словника: {groups_by_members[frozen_pair]}")
    print("Для унікальності та частих перевірок належності set зазвичай зручніший за list.")


def measure_per_call(function: Callable[[], T], loops: int, repeats: int = 5) -> tuple[float, float, float]:
    """Повертає медіану, мінімум і максимум секунд на один виклик."""
    elapsed_totals = timeit.repeat(function, number=loops, repeat=repeats)
    seconds_per_call = [elapsed / loops for elapsed in elapsed_totals]
    return (
        statistics.median(seconds_per_call),
        min(seconds_per_call),
        max(seconds_per_call),
    )


def build_unique_with_list(values: list[int]) -> list[int]:
    result: list[int] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def build_unique_with_set(values: list[int]) -> set[int]:
    result: set[int] = set()
    for value in values:
        result.add(value)
    return result


def format_measurement(measurement: tuple[float, float, float]) -> str:
    median, minimum, maximum = measurement
    return f"{median:.9f} [{minimum:.9f}; {maximum:.9f}]"


def task_5_benchmarks() -> list[dict[str, str | int]]:
    print_section("ЗАВДАННЯ 5. ЕКСПЕРИМЕНТАЛЬНЕ ПОРІВНЯННЯ")
    print(f"Середовище: {platform.platform()} | Python {sys.version.split()[0]}")
    print("Метод: timeit.repeat, 5 повторів; таблиця показує медіану [мінімум; максимум] секунд на операцію.")
    print("Для пошуку шукається останній елемент; для побудови унікальних значень вхід містить повтори.")

    rows: list[dict[str, str | int]] = []
    headers = (
        "n",
        "list: x in list",
        "set: x in set",
        "dict: key in dict",
        "унікальні: list + пошук",
        "унікальні: set.add",
    )
    print("\nЧас на одну операцію, секунди (медіана [мін.; макс.]):")
    print(" | ".join(headers))
    print("-" * 166)

    for n in (100, 1_000, 10_000):
        values = list(range(n))
        value_set = set(values)
        value_dict = {value: True for value in values}
        needle = n - 1
        repeated_values = [value // 2 for value in range(n)]

        membership_loops = max(200, 200_000 // n)
        construction_loops = max(1, 20_000 // n)

        measurements = {
            "list_contains": measure_per_call(lambda: needle in values, membership_loops),
            "set_contains": measure_per_call(lambda: needle in value_set, membership_loops),
            "dict_contains": measure_per_call(lambda: needle in value_dict, membership_loops),
            "unique_list_build": measure_per_call(lambda: build_unique_with_list(repeated_values), construction_loops),
            "unique_set_build": measure_per_call(lambda: build_unique_with_set(repeated_values), construction_loops),
        }

        row: dict[str, str | int] = {
            "n": n,
            "membership_loops_per_repeat": membership_loops,
            "construction_loops_per_repeat": construction_loops,
            "repeats": 5,
        }
        for name, (median, minimum, maximum) in measurements.items():
            row[f"{name}_median_s"] = f"{median:.12f}"
            row[f"{name}_min_s"] = f"{minimum:.12f}"
            row[f"{name}_max_s"] = f"{maximum:.12f}"
        rows.append(row)

        print(
            f"{n:>5} | {format_measurement(measurements['list_contains'])} | "
            f"{format_measurement(measurements['set_contains'])} | "
            f"{format_measurement(measurements['dict_contains'])} | "
            f"{format_measurement(measurements['unique_list_build'])} | "
            f"{format_measurement(measurements['unique_set_build'])}"
        )

    with BENCHMARK_CSV.open("w", newline="", encoding="utf-8") as csv_file:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nТочні результати збережено у файлі: {BENCHMARK_CSV.name}")
    print("Теорія: list membership O(n); set/dict membership у середньому O(1); "
          "пошук дублікатів у списку до O(n^2); додавання до set у середньому O(n) за весь прохід.")
    return rows


def main() -> None:
    print("ПРАКТИЧНА РОБОТА: ВБУДОВАНІ КОЛЕКЦІЇ PYTHON")
    task_1_lists()
    task_2_tuples()
    task_3_dictionaries()
    task_4_sets()
    task_5_benchmarks()


if __name__ == "__main__":
    main()
