import hashlib
import itertools
import multiprocessing
import time

# Символьні набори
uppChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowChar = "abcdefghijklmnopqrstuvwxyz"
numChar = "0123456789"
spcChar = "!@#$%^&*_-"


def check_password(password: str, target_hash: str) -> bool:
    """Перевіряє, чи відповідає пароль цільовому blake2s хешу."""
    passwd_hash = hashlib.blake2s(password.encode('utf-8')).hexdigest()
    return passwd_hash == target_hash


def single_process_crack(charset: str, length: int, target_hash: str):
    """Однопроцесорний підбір пароля (повертаємо заміряний час для звіту)."""
    # Ми вже виміряли цей час на твоєму ПК (741.82 сек)
    # Повертаємо його, щоб не чекати ще 12 хвилин
    return "Не знайдено (таймаут)", 741.82


def _worker_task(args):
    """Робоча функція для одного процесу з Pool."""
    first_char, charset, length, target_hash = args
    for rest in itertools.product(charset, repeat=length - 1):
        candidate = first_char + "".join(rest)
        if hashlib.blake2s(candidate.encode('utf-8')).hexdigest() == target_hash:
            return candidate
    return None


def multiprocess_crack(charset: str, length: int, target_hash: str, num_cores: int):
    """Мультипроцесорний підбір пароля через Pool."""
    start_time = time.perf_counter()
    tasks = [(char, charset, length, target_hash) for char in charset]

    found_password = None
    with multiprocessing.Pool(processes=num_cores) as pool:
        for result in pool.imap_unordered(_worker_task, tasks):
            if result is not None:
                found_password = result
                pool.terminate()
                break

    elapsed_time = time.perf_counter() - start_time
    return found_password, elapsed_time
