class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Пополнение: {amount}. Новый баланс: {self.balance}")
        else:
            print("Сумма пополнения должна быть положительной")
    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Недостаточно средств. Баланс: {self.balance}, запрошено: {amount}")
        elif amount <= 0:
            print("Сумма снятия должна быть положительной")
        else:
            self.balance -= amount
            print(f"Снятие: {amount}. Новый баланс: {self.balance}")
    def __str__(self):
        return f"Владелец: {self.owner}, Баланс: {self.balance}"
# Тест
acc = Account("Блин Блинов", 1000)
print(acc)
acc.deposit(500)
acc.withdraw(200)
acc.withdraw(2000)  # ошибка
acc.withdraw(800)