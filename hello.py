import flet as ft # Для создания графического интерфейса пользователя
from datetime import datetime # Чтобы работать с датой и временем при сохранении отчёта

# Базовая сущность для всех классов приложения
class Entity:
    def __init__(self):
        self._id = None  # Приватное поле идентификатора сущности

    @property # Геттер (чтение)
    def id(self): return self._id  

    @id.setter # Сеттер (запись), относится к свойству выше
    def id(self, value: int):
        """Сеттер проверяет тип данных."""
        if isinstance(value, int) and value > 0:
            self._id = value

    # Требование задания: переопределить спецметоды
    def __eq__(self, other):
        """
        Два объекта равны, если они одного типа и имеют одинаковые ID.
        Это нужно, чтобы пользователь не мог быть равен сессии или другому классу.
        """
        if type(self) is type(other):
            return self.id == other.id 
        return False

    def __repr__(self):
        return f"Entity(id={self.id})"

    def __str__(self):
        return str(self.id)
    
    # Требование задания: статические методы
    _next_id = 1  # Приватный статический атрибут - начальное значение

    @staticmethod
    def generate_id():
        """
        Генерирует уникальный идентификатор.
        """
        result = Entity._next_id  # Берём текущее значение
        Entity._next_id += 1     # Увеличиваем его для следующего объекта
        return result


# Реализация реального класса из задания
class User(Entity):
    """Пользователь системы."""
    
    def __init__(self, name: str):
        super().__init__()                     # Вызываем конструктор родителя
        self._id = User.generate_id()         # Генерируем уникальный ID через наш статик-метод
        self.name = name                      # Публичное поле имени
        
    @property
    def full_info(self) -> dict:
        """
        Требование задания: публичные методы,
        возвращающие словарь со всей информацией об объекте.
        """
        return {"id": self.id, "name": self.name}


# Второй обязательный класс по заданию
class Session(Entity):
    """Сессия работы пользователя."""

    def __init__(self, user: User, start_time: datetime):
        super().__init__()
        self._id = Session.generate_id()

        # Публичные поля
        self.user = user          # Пользователь, который открыл сессию
        self.start_time = start_time   # Время начала (datetime)
        self.end_time: datetime | None = None  # Время окончания может быть пустым

    @property
    def duration(self) -> float | None:
        """
        Продолжительность сессии в секундах.
        Если сессия ещё не завершена — возвращает None.
        """
        end = self.end_time or datetime.now()
        delta = end - self.start_time
        return delta.total_seconds()

    @property
    def full_info(self) -> dict:
        """
        Требование задания: публичные методы,
        возвращающие словарь со всей информацией об объекте.
        """
        return {
            "id": self.id,
            "user_name": self.user.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_sec": self.duration
        }


def main():
    """Простая проверка работы программы."""
    # Создадим двух пользователей
    alex = User("Alex")
    john = User("John")

    print(alex.full_info)      # {'id': 1, 'name': 'Alex'}
    print(john.full_info)      # {'id': 2, 'name': 'John'}

    # Проверим сравнение объектов
    print(f"{alex} == {john}:", alex == john)       # Должно быть False
    print(f"{alex} == {alex}:", alex == alex)        # Должно быть True

    # Создадим сессии
    session_1 = Session(user=alex, start_time=datetime(2026, 10, 13, 9, 0))
    session_2 = Session(user=john, start_time=datetime(2026, 10, 13, 14, 0))

    # Закроем первую сессию
    session_1.end_time = datetime(2026, 10, 13, 9, 5)

    # Выведем полную информацию
    for s in [session_1, session_2]:
        print(s.full_info)

if __name__ == "__main__":
    main()