import os
from scripting_langs_lab2.lib import lowChar, uppChar, spcChar, single_process_crack, multiprocess_crack

def main():
    target_hash = "f6cdd18a322df702c076e508a62e9973a70da5363b438e0cf2b7a2d333ec3817"
    password_len = 5
    charset = lowChar + uppChar + spcChar  # Варіант 19

    cores = os.cpu_count() or 4
    print(f"Кількість ядер процесора у вашому ПК: {cores}")
    print("-" * 50)

    print("1. Запуск підбору пароля в однопроцесорному режимі...")
    passwd_single, time_single = single_process_crack(charset, password_len, target_hash)
    print(f"Результат (Single-process): {passwd_single}")
    print(f"Час виконання (Single-process): {time_single:.2f} сек.")
    print("-" * 50)

    print(f"2. Запуск підбору пароля в мультипроцесорному режимі ({cores} процесів)...")
    passwd_multi, time_multi = multiprocess_crack(charset, password_len, target_hash, cores)
    print(f"Знайдений пароль: {passwd_multi}")
    print(f"Час виконання (Multi-process): {time_multi:.2f} сек.")
    print("-" * 50)

    if time_multi > 0:
        speedup = time_single / time_multi
        print(f"Прискорення за рахунок мультипроцесорності: у {speedup:.2f} разів")

if __name__ == "__main__":
    main()
    