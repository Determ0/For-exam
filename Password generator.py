import secrets
import hashlib
import sqlite3

def generate_password(length=12):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def create_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS passwords ( id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, hashed_password TEXT ) ''')
    conn.commit()
    conn.close()


def add_user(username, password):
    hashed_pass = hash_password(password)
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passwords (username, hashed_password) VALUES (?, ?)', (username, hashed_pass))
        conn.commit()
        print(f'Пользователь {username} успешно зарегистрирован.')
    except sqlite3.IntegrityError as e:
        print(f'Ошибка регистрации: {e}')
    finally:
        conn.close()


def check_password(username, input_password):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hashed_password FROM passwords WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        print('Пользователь не найден!')
        return False

    stored_hash = result[0]
    entered_hash = hash_password(input_password)

    if stored_hash == entered_hash:
        print('Пароль верный!')
        return True
    else:
        print('Неверный пароль!')
        return False


if __name__ == '__main__':
    create_db()

    new_password = generate_password()
    print(f"Сгенерированный пароль: {new_password}")

    add_user('test_user', new_password)

    input_pwd = input("Введите пароль для проверки: ")
    check_password('test_user', input_pwd)