import psycopg2
import csv
import sys

class PhoneBookWithProcedures:
    def __init__(self):
        self.conn=psycopg2.connect(
            host="localhost",
            database="firstDB",
            user="postgres",
            password="1215" 
        )
        self.create_table_and_procedures()
    
    def create_table_and_procedures(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50),
                    phone VARCHAR(20) UNIQUE NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            procedures_sql="""
CREATE OR REPLACE FUNCTION search_by_pattern(search_pattern TEXT)
RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone, p.email
    FROM phonebook p
    WHERE p.first_name ILIKE '%'  search_pattern  '%'
       OR p.last_name ILIKE '%'  search_pattern  '%'
       OR p.phone ILIKE '%'  search_pattern  '%'
       OR p.email ILIKE '%'  search_pattern  '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_or_update_user(
    IN user_first_name VARCHAR,
    IN user_phone VARCHAR,
    IN user_last_name VARCHAR DEFAULT NULL,
    IN user_email VARCHAR DEFAULT NULL
)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phone = user_phone) THEN
        UPDATE phonebook 
        SET first_name = user_first_name,
            last_name = COALESCE(user_last_name, last_name),
            email = COALESCE(user_email, email)
        WHERE phone = user_phone;
        RAISE NOTICE 'Пользователь с телефоном % обновлен', user_phone;
    ELSE
        INSERT INTO phonebook (first_name, last_name, phone, email)
        VALUES (user_first_name, user_last_name, user_phone, user_email);
        RAISE NOTICE 'Новый пользователь % добавлен', user_first_name;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_many_users(
    IN users_data TEXT,  
    OUT incorrect_data TEXT[]
)
AS $$
DECLARE
    user_record TEXT;
    user_name VARCHAR;
    user_phone VARCHAR;
    phone_valid BOOLEAN;
    incorrect_items TEXT[];
BEGIN
    incorrect_items := ARRAY[]::TEXT[];
    
    FOREACH user_record IN ARRAY string_to_array(users_data, ',')
    LOOP
        user_name := split_part(user_record, ':', 1);
        user_phone := split_part(user_record, ':', 2);
        
        phone_valid := user_phone ~ '^[0-9+]{10,15}$';
        
        IF phone_valid AND user_name != '' AND user_phone != '' THEN
            CALL insert_or_update_user(user_name, user_phone);
        ELSE
            incorrect_items := array_append(incorrect_items, user_record);
        END IF;
    END LOOP;
    
    incorrect_data := incorrect_items;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(
    page_limit INTEGER DEFAULT 10,
    page_offset INTEGER DEFAULT 0
)
RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    total_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone, p.email,
           COUNT(*) OVER() AS total_count
    FROM phonebook p
    ORDER BY p.first_name, p.last_name
    LIMIT page_limit
    OFFSET page_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(
    IN search_value VARCHAR
)
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM phonebook WHERE phone = search_value;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    IF deleted_count = 0 THEN
        DELETE FROM phonebook WHERE first_name ILIKE search_value;
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
    END IF;
    
    IF deleted_count > 0 THEN
        RAISE NOTICE 'Удалено % записей(и)', deleted_count;
    ELSE

RAISE NOTICE 'Записи не найдены';
    END IF;
END;
$$ LANGUAGE plpgsql;
            """
            cur.execute(procedures_sql)
            
            self.conn.commit()
        print("Таблица и процедуры созданы")
    
    def search_by_pattern(self):
        print("\nПоиск по шаблону")
        pattern = input("Введите часть имени, фамилии или телефона: ").strip()
        
        with self.conn.cursor() as cur:
            cur.callproc('search_by_pattern', [pattern])
            results=cur.fetchall()
            
            if not results:
                print(" Ничего не найдено")
                return
            
            print(f"\n Найдено {len(results)} записей:")
            for row in results:
                print(f"  {row[1]} {row[2] or ''} | {row[3]} | {row[4] or 'нет'}")
    
    def insert_or_update(self):
        print("\nДобавить/Обновить пользователя")
        first_name=input("Имя: ").strip()
        phone=input("Телефон: ").strip()
        last_name=input("Фамилия (опционально): ").strip() or None
        email= input("Email (опционально): ").strip() or None
        
        with self.conn.cursor() as cur:
            cur.execute("CALL insert_or_update_user(%s, %s, %s, %s)",
                       (first_name, phone, last_name, email))
            self.conn.commit()
        
        print(" Готово")
    
    def insert_many_users(self):
        print("\nМассовая вставка пользователей")
        print("Формат: Имя:Телефон,Имя:Телефон,...")
        print("Пример: Иван:87011234567,Анна:87029876543")
        
        users_input=input("Введите данные: ").strip()
        
        with self.conn.cursor() as cur:
            cur.callproc('insert_many_users', [users_input])
            cur.execute("SELECT incorrect_data")
            incorrect=cur.fetchone()[0]
            
            self.conn.commit()
            
            if incorrect:
                print(f"\nНекорректные данные ({len(incorrect)}):")
                for item in incorrect:
                    print(f" -{item}")
            else:
                print("Все данные корректны и добавлены!")
    
    def show_paginated(self):
        print("\nПросмотр с пагинацией ")
        try:
            limit=int(input("Сколько записей на странице (по умолчанию 5): ") or 5)
            page=int(input("Номер страницы (начиная с 0): ") or 0)
            offset=page*limit
        except ValueError:
            print("Некорректный ввод")
            return
        
        with self.conn.cursor() as cur:
            cur.callproc('get_contacts_paginated', [limit, offset])
            results=cur.fetchall()
            
            if not results:
                print(" Нет записей")
                return
            
            total_count=results[0][5] if results else 0
            total_pages=(total_count+limit-1)//limit
            
            print(f"\n Страница {page + 1} из {total_pages} (всего {total_count} записей):")
            for row in results:
                print(f"  {row[1]} {row[2] or ''} |  {row[3]}")
            
            print(f"\nКоманды: N-следующая, P-предыдущая, Q-выход")
            
            while True:
                cmd=input("> ").lower()
                if cmd=='n' and page<total_pages-1:
                    page+=1
                    offset=page*limit
                    cur.callproc('get_contacts_paginated', [limit, offset])
                    results=cur.fetchall()
                    
                    print(f"\nСтраница {page + 1}:")
                    for row in results:
                        print(f"  {row[1]} {row[2] or ''} | {row[3]}")
                
                elif cmd=='p' and page>0:
                    page-=1
                    offset=page*limit
                    cur.callproc('get_contacts_paginated', [limit, offset])
                    results=cur.fetchall()
                    
                    print(f"\n Страница {page + 1}:")
                    for row in results:
                        print(f"  {row[1]} {row[2] or ''} | {row[3]}")
                elif cmd=='q':
                    break
                
    def delete_by_name_or_phone(self):
        print("\nУдаление записи")
        value = input("Введите имя или телефон для удаления: ").strip()
        
        confirmation = input(f"Удалить '{value}'? (y/n): ").lower()
        if confirmation != 'y':
            print("Отменено")
            return
        
        with self.conn.cursor() as cur:
            cur.execute("CALL delete_by_name_or_phone(%s)", (value,))
            self.conn.commit()
        
        print("процедура удаления выполнена")
    
    def insert_from_csv(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader=csv.reader(file)
                next(reader)
                
                for row in reader:
                    if len(row)>=3:
                        with self.conn.cursor() as cur:
                            cur.execute("CALL insert_or_update_user(%s, %s, %s, %s)",
                                       (row[0], row[2], row[1], row[3] if len(row) > 3 else None))
                self.conn.commit()
            print(f"данные из {filename} загружены")
        except Exception as e:
            print(f"oшибка: {e}")
    
    def insert_from_console(self):
        print("\nВвод нового контакта ")
        first_name=input("Имя: ").strip()
        phone=input("Телефон: ").strip()
        last_name=input("Фамилия: ").strip() or None
        email=input("Email: ").strip() or None
        
        with self.conn.cursor() as cur:
            cur.execute("CALL insert_or_update_user(%s, %s, %s, %s)",
                       (first_name, phone, last_name, email))
            self.conn.commit()
        print("Готово")
    
    def menu(self):
        while True:
            print("\n" + "="*50)
            print("Телефонная кига")
            print("="*50)
            print("=== Основные функции ===")
            print("1. Поиск по шаблону")
            print("2. Добавить/обновить пользователя")
            print("3. Массовая вставка с проверкой")
            print("4. Просмотр с пагинацией")
            print("5. Удаление по имени/телефону")
            print("\n=== Вспомогательные ===")
            print("6. Создать таблицу и процедуры")
            print("7. Загрузить из CSV")
            print("8. Добавить с консоли (простой)")
            print("9. Выход")
            
            choice=input("\nВыберите действие (1-9): ").strip()
            
            actions={
                '1': self.search_by_pattern,
                '2': self.insert_or_update,
                '3': self.insert_many_users,
                '4': self.show_paginated,
                '5': self.delete_by_name_or_phone,
                '6': self.create_table_and_procedures,
                '7': lambda: self.insert_from_csv(input("Имя CSV файла: ")),
                '8': self.insert_from_console,
                '9': lambda: (print("Выход..."), self.conn.close(), sys.exit())
            }
            
            if choice in actions:
                actions[choice]()
            else:
                print("Неверный выбор")

if __name__ == "__main__":
    sample_csv="""first_name,last_name,phone,email
Иван,Петров,87011234567,ivan@mail.kz
Анна,Сидорова,87029876543,anna@mail.kz
Мария,Иванова,87035556677,maria@mail.kz
"""
    
    with open('contacts.csv', 'w', encoding='utf-8') as f:
        f.write(sample_csv)
    
    print("cоздан тестовый файл contacts.csv")
    
    pb=PhoneBookWithProcedures()
    pb.menu()
