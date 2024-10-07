import json
import os
from telethon import TelegramClient

# Введите свои API ID и Hash
api_id = '23620385'
api_hash = '6e10be3dbfc16f1740b63fb2fa517e62'
# Телефонный номер, связанный с вашим Telegram аккаунтом
phone = '+6281265395536'

# Инициализация клиента
client = TelegramClient('new_session_name', api_id, api_hash)

# Указываем полный путь к файлу для сохранения
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parsed_messages.json')

async def main():
    # Подключаемся к клиенту
    await client.start(phone)
    
    # Выберите чат или канал для парсинга
    chat = 'https://t.me/argentina_chat_kg'

    message_count = 0  # Счётчик сообщений
    messages_data = []  # Список для сохранения всех сообщений
    unique_users = set()  # Множество для хранения уникальных пользователей

    # Получаем историю сообщений
    async for message in client.iter_messages(chat):
        sender = await message.get_sender()
        
        # Проверяем, отправитель это пользователь или канал
        if sender:  # Проверка, что sender не None
            # Проверяем уникальность пользователя
            if sender.id not in unique_users:
                unique_users.add(sender.id)  # Добавляем ID пользователя в множество
                message_info = {
                    'user_id': sender.id,
                    'message': message.text
                }
                if hasattr(sender, 'first_name'):
                    message_info['first_name'] = sender.first_name
                    message_info['username'] = sender.username or 'Unknown'
                elif hasattr(sender, 'title'):
                    message_info['first_name'] = 'Channel/Group'
                    message_info['username'] = sender.title
                
                messages_data.append(message_info)
                message_count += 1  # Увеличиваем счётчик для каждого уникального сообщения

                # Выводим информацию в консоль
                print(f"Сообщение #{message_count}")
                if hasattr(sender, 'first_name'):
                    print(f"Пользователь: {sender.username or sender.first_name}, ID: {sender.id}")
                else:
                    print(f"Сообщение от канала или группы: {sender.title}")
                print(f"Сообщение: {message.text}\n")

                # Проверяем, собрали ли 100 уникальных пользователей
                if len(unique_users) >= 100:
                    break  # Прерываем цикл, если достигли 100 уникальных пользователей
        else:
            print(f"Сообщение не имеет отправителя.")

    # Если сообщения были собраны, сохраняем их в JSON
    if messages_data:
        try:
            print(f"Попытка сохранить данные в: {save_path}")
            with open(save_path, 'w', encoding='utf-8') as file:
                json.dump(messages_data, file, ensure_ascii=False, indent=4)
            print(f"Данные успешно сохранены в: {save_path}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    else:
        print("Не было собрано ни одного сообщения.")

    await client.disconnect()

# Запуск скрипта
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
