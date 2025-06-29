import os
import matplotlib.pyplot as plt
import timeit
from tabulate import tabulate

def compute_lps(pattern: str) -> list:
    """Calculates the largest prefix and suffix (LPS) array for the KMP algorithm"""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string: str, pattern: str) -> int:
    """KMP (Knuth-Morris-Pratt) algorithm for searching for a substring in text"""
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1

def build_shift_table(pattern: str) -> dict:
    """Create a shift table for the Boyer-Moore algorithm"""
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text: str, pattern: str) -> int:
    shift_table = build_shift_table(pattern)
    i = 0 # Start index

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 # Start from the end of the substring

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 # Moving to the beginning of the substring

        # If the entire substring matches, return its position
        if j < 0:
            return i

        # Shift the index based on the shift table
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def polynomial_hash(s: str, base: int = 256, modulus: int = 101) -> int:
    """Returns the polynomial hash of the string s."""
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string: str, substring: str) -> int:
    # Lengths of the main string and substring of the search
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Previous value for hash recalculation
    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def run_tests(text: str, pattern_exist: str, pattern_fake: str) -> dict:
    """Runs tests for each substring search algorithm."""
    results = {}

    for name, func in {
        'KMP': kmp_search,
        'Boyer-Moore': boyer_moore_search,
        'Rabin-Karp': rabin_karp_search
    }.items():
        time_exist = timeit.timeit(lambda: func(text, pattern_exist), number=5)
        time_fake = timeit.timeit(lambda: func(text, pattern_fake), number=5)
        results[name] = {
            'existing_pattern': time_exist,
            'fake_pattern': time_fake
        }
    return results

def display_results(name, results):
    print(f"\nResults for {name}:")
    table = []
    for algo, data in results.items():
        table.append([algo, f"{data['existing_pattern']:.6f}", f"{data['fake_pattern']:.6f}"])
    print(tabulate(table, headers=["Алгоритм", "Час (існуючий)", "Час (вигаданий)"], tablefmt="grid"))

def load_text(filename: str) -> str:
    """Loads text from a file with error handling."""
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' was not found.")
        return ""

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"⚠️ Помилка при читанні файлу '{filename}': {e}")
        return ""

# Графік стовпчикової діаграми
def plot_bar_chart(results1: dict or None, results2: dict or None):
    """Build a bar chart to compare results."""
    bar_width = 0.2

    if results1:
        algorithms = list(results1.keys())
    elif results2:
        algorithms = list(results2.keys())
    else:
        print("No results for graphing.")
        return

    x = range(len(algorithms))
    plt.figure(figsize=(10, 6))

    if results1:
        existing1 = [results1[algo]['existing_pattern'] for algo in algorithms]
        fake1 = [results1[algo]['fake_pattern'] for algo in algorithms]

        plt.bar([i - 0.3 * bar_width for i in x], existing1, width=bar_width,
                label='Text1 - існуючий', color='#FFD700')
        plt.bar([i + 0.3 * bar_width for i in x], fake1, width=bar_width,
                label='Text1 - вигаданий', color='#1E90FF')

    if results2:
        existing2 = [results2[algo]['existing_pattern'] for algo in algorithms]
        fake2 = [results2[algo]['fake_pattern'] for algo in algorithms]

        offset = 1.2 if results1 else -0.3
        plt.bar([i + offset * bar_width for i in x], existing2, width=bar_width,
                label='Text2 - існуючий', color='#F4E04D')
        plt.bar([i + (offset + 0.6) * bar_width for i in x], fake2, width=bar_width,
                label='Text2 - вигаданий', color='#4682B4')

    plt.xticks(x, algorithms)
    plt.ylabel("Час виконання (секунди)")
    plt.title("Порівняння алгоритмів пошуку підрядка")
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

results1 = None
results2 = None

text1 = load_text('text1.txt')
text2 = load_text('text2.txt')

if not text1:
    print("Unable to run tests for text1: text is empty.")
else:
    results1 = run_tests(text1, "Жадібний", "вигаданий")
    display_results("Текст 1", results1)

if not text2:
    print("Unable to run tests for text2: text is empty.")
else:
    results2 = run_tests(text2, "Перевага", "вигаданий")
    display_results("Текст 2", results2)

plot_bar_chart(results1, results2)
