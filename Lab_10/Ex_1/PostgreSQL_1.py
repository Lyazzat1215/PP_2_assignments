import psycopg2
import csv
import sys
# извиняюс можно матерится?
class PhoneBook:
    def __init__(self):
        self.conn=psycopg2.connect(
            host="localhost",
            database="firstDB",
            user="postgres",
            password="1215" 
        )
        self.create_table()
    
    def create_table(self):
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
            self.conn.commit()
        print(" Таблица 'phonebook' создана бл")
    
    def insert_csv(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader=csv.reader(file)
                next(reader) 
                
                with self.conn.cursor() as cur:
                    for row in reader:
                        if len(row)>=3:
                            cur.execute("""
                                INSERT INTO phonebook (first_name, last_name, phone, email)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (phone) DO NOTHING
                            """, (row[0], row[1], row[2], row[3] if len(row) > 3 else None))
                    self.conn.commit()
            print(f" Данные из {filename} загружены")
        except FileNotFoundError:
            print(f" Файл {filename} не найден")
        except Exception as e:
            print(f" Ошибка: {e}")
    
    def insert_from_console(self):
        print("\n=== Ввод нового контакта ===")
        first_name=input("Имя: ").strip()
        last_name=input("Фамилия: ").strip() or None # не обяз
        phone=input("Телефон: ").strip()
        email=input("Email: ").strip() or None  # не обяз
        
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO phonebook (first_name, last_name, phone, email)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, phone, email))
                self.conn.commit()
            print(" Контакт добавлен!")
        except psycopg2.IntegrityError:
            print(" Телефон уже существует в базе")
    
    
    def update_contact(self):
        print("\n=== Обновление контакта ===")
        phone=input("Введите телефон контакта для изменения: ").strip()
        
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, first_name FROM phonebook WHERE phone = %s", (phone,))
            contact=cur.fetchone()
            
            if not contact:
                print(" Контакт не найден")
                return
            
            print(f"Найден контакт: {contact[1]}")
            new_first_name=input(f"Новое имя [{contact[1]}]: ").strip() or contact[1]
            new_phone=input(f"Новый телефон [{phone}]: ").strip() or phone
            
            cur.execute("""
                UPDATE phonebook 
                SET first_name=%s, phone=%s 
                WHERE id=%s
            """, (new_first_name, new_phone, contact[0]))
            self.conn.commit()
        
        print(" Контакт обновлен!")
    
    def search_contacts(self):
        print("\n=== Поиск контактов ===")

        print("1. По имени")
        print("2. По фамилии")
        print("3. По телефону")
        print("4. По email")
        print("5. Показать все контакты")
        
        choice=input("Выберите вариант поиска: ").strip()
        
        with self.conn.cursor() as cur:
            if choice=='1':
                name=input("Введите имя: ").strip()
                cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f'%{name}%',))
            elif choice=='2':
                last_name=input("Введите фамилию: ").strip()
                cur.execute("SELECT * FROM phonebook WHERE last_name ILIKE %s", (f'%{last_name}%',))
            elif choice=='3':
                phone = input("Введите телефон: ").strip()
                cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f'%{phone}%',))
            elif choice=='4':
                email=input("Введите email: ").strip()
                cur.execute("SELECT * FROM phonebook WHERE email ILIKE %s", (f'%{email}%',))
            elif choice=='5':
                cur.execute("SELECT * FROM phonebook ORDER BY first_name")
            else:
                print(" Неверный выбор")
                return
            
            contacts=cur.fetchall()
            if not contacts:
                print(" Контакты не найдены")
                return
            
            print(f"\nНайдено контактов: {len(contacts)}")
            for contact in contacts:
                print(f"{contact[0]}. {contact[1]} {contact[2] or ''} | {contact[3]} | {contact[4] or 'нет'}")
    
    
    def delete_contact(self):
        print("\n=== Удаление контакта ===")
        print("Удалить по:")
        print("1. Имени")
        print("2. Телефону")
        
        choice=input("Выберите: ").strip()
        
        with self.conn.cursor() as cur:
            if choice =='1':
                name=input("Введите имя для удаления: ").strip()
                cur.execute("DELETE FROM phonebook WHERE first_name ILIKE %s RETURNING phone", (f'%{name}%',))
            elif choice=='2':
                phone=input("Введите телефон для удаления: ").strip()
                cur.execute("DELETE FROM phonebook WHERE phone=%s RETURNING first_name", (phone,))
            else:
                print("неверный выбор")
                return
            
            deleted=cur.fetchall()
            self.conn.commit()
            
            if deleted:
                print(f" Удалены контакты {len(deleted)}")
            else:
                print("не найдены")
    
    def menu(self):
        while True:
            print("\n" + "="*40)
            print(" Телефонная книга")
            print("="*40)
            print("1. Создать таблицу")
            print("2. Загрузить из CSV")
            print("3. Обновить контакт")
            print("4. Поиск контактов")
            print("5. Удалить контакт")
            print("6. Показать все контакты")
            print("7. Выход")
            
            choice=input("\nВыберите действие: ").strip()
            
            if choice=='1':
                self.create_table()
            elif choice=='2':
                filename=input("Имя файл: ").strip()
                self.insert_from_csv(filename)
            elif choice=='3':
                self.insert_from_console()
            elif choice=='4':
                self.update_contact()
            elif choice=='5':
                self.search_contacts()
            elif choice=='6':
                self.delete_contact()
            elif choice=='7':
                self.search_contacts()  
            elif choice=='8':
                print("Выход...")
                self.conn.close()
                break
            else:
              print("неправильный выбор")


if __name__ == "__main__":
    pb = PhoneBook()
    pb.menu()
