import random
from itertools import product
from tqdm import tqdm

# Коэффицент, влияющий на скорость обучения
LEARNING_RATE = 0.05
EMPTY_SYMBOL = '0'


# Заменена символа в строке по заданному индексу
def replace_char_at_index(str, index, new_char):
    new_str = list(str)
    if index < len(str):
        new_str[index] = new_char
        str = ''.join(new_str)
    return str


class Field:
    # Возвращает список индексов пустых клеток
    @staticmethod
    def get_empty_cells(field):
        empty_cells = []
        field_list = list(field)

        for i in range(len(field_list)):
            if field_list[i] == EMPTY_SYMBOL:
                empty_cells.append(i)

        return empty_cells

    # Проверка поля на наличие победителя
    # (-1 - ничья, 0 - есть свободные клетки, 1 - победил игрок №1, 2 - победил игрок №2)
    @staticmethod
    def check_winner(field):
        # Перечисление всех выигрышных комбинаций
        if field[0] == field[1] == field[2] == '1' or field[3] == field[4] == field[5] == '1' or field[
            6] == field[7] == field[8] == '1' or field[0] == field[3] == field[6] == '1' or field[1] == \
                field[4] == field[7] == '1' or field[2] == field[5] == field[8] == '1' or field[0] == \
                field[4] == field[8] == '1' or field[2] == field[4] == field[6] == '1':
            return 1
        elif field[0] == field[1] == field[2] == '2' or field[3] == field[4] == field[5] == '2' or field[
            6] == field[7] == field[8] == '2' or field[0] == field[3] == field[6] == '2' or field[1] == \
                field[4] == field[7] == '2' or field[2] == field[5] == field[8] == '2' or field[0] == \
                field[4] == field[8] == '2' or field[2] == field[4] == field[6] == '2':
            return 2
        elif len(Field.get_empty_cells(field)) == 0:
            return -1
        else:
            return 0

    # Создание поля
    @staticmethod
    def generate_field():
        field = []
        for i in range(9):
            field.append(EMPTY_SYMBOL)

        return ''.join(field)

    # Обучение агента (игра с другим агентом)
    def learning_agent(self, player1, player2, steps):
        for i in tqdm((range(steps))):
            field = self.generate_field()

            # Пока есть свободные клетки
            while Field.check_winner(field) == 0:
                old_field = field
                field = player1.turn(field)

                # Перерасчет ценностей
                player2.recalculation(old_field, field)

                # Проверка, что прошлый игрок не победил на последнем шаге
                if Field.check_winner(field) == 0:
                    old_field = field
                    field = player2.turn(field)
                    player1.recalculation(old_field, field)

    def user_decision(self, field, user_number):
        print('Текущее поле:')
        self.user_print(field)
        user_step = int(input("Введите позицию для хода: "))
        return replace_char_at_index(field, user_step, str(user_number))

    # Удобный вывод для пользователя
    def user_print(self, field):
        field_for_human = field.replace('1', 'X').replace('2', 'O')
        for char_num in range(9):
            if field_for_human[char_num] == EMPTY_SYMBOL:
                field_for_human = replace_char_at_index(field_for_human, char_num, str(char_num))
        self.print_field(field_for_human)

    # Вывод поля в консоль
    @staticmethod
    def print_field(field):
        print(f"|{field[0]}|{field[1]}|{field[2]}|")
        print(f"|{field[3]}|{field[4]}|{field[5]}|")
        print(f"|{field[6]}|{field[7]}|{field[8]}|")

    # Начало игры
    def start_game(self, agent, user):
        field = self.generate_field()

        # Пока есть свободные клетки
        while Field.check_winner(field) == 0:
            if user == 'X':
                user_num = 1
                field = self.user_decision(field, user_num)
                # Проверка, что прошлый игрок не победил на последнем шаге
                if Field.check_winner(field) == 0:
                    field = agent.turn(field)
            elif user == 'O':
                user_num = 2
                field = agent.turn(field)
                # Проверка, что прошлый игрок не победил на последнем шаге
                if Field.check_winner(field) == 0:
                    field = self.user_decision(field, user_num)

        print('Конец игры: ')

        if self.check_winner(field) == -1:
            print('Ничья')
        elif self.check_winner(field) == 1:
            print('Победил игрок №1')
        elif self.check_winner(field) == 2:
            print('Победил игрок №2')

        self.user_print(field)


class Player:
    def __init__(self, player_number):
        # Номер игрока
        self.player_number = player_number
        # Таблица ценностей (состояний)
        self.prices = {}
        # Шаги во время игры
        self.steps = []
        # Заполнить стартовую таблицу ценностей
        self.fill_prices_matrix()

    # Заполнение таблицы ценностей начальными значениями
    def fill_prices_matrix(self):
        for roll in product([0, 1, 2], repeat=9):
            key = ''.join(str(x) for x in roll)
            winner = Field.check_winner(key)
            # Состояния выигрыша
            if winner == self.player_number:
                self.prices[key] = 1
            # Стандартное состояние
            elif winner == 0:
                self.prices[key] = 0.5
            # Состояние проигрыша
            else:
                self.prices[key] = 0

    # Возвращает доступные шаги для игрока в текущем состоянии и их ценности
    def get_available_states(self, current_field):
        available_states = {}
        # Получение списка пустые клеток
        empty_cells = Field.get_empty_cells(current_field)
        # Получение списка возможных следующих состояний
        for cell in empty_cells:
            avail_state = replace_char_at_index(current_field, cell, str(self.player_number))
            available_states[avail_state] = self.prices[avail_state]
        return available_states

    # Принятие решения о следующем шаге
    def turn(self, current_state):
        available_states = self.get_available_states(current_state)
        # Делать ли разведочный шаг True, False
        exploration_move = random.random() <= 0.05
        # Если шаг не разведочный выбираем состояние с наибольшей ценностью
        if not exploration_move:
            # Поиск наивысшей ценности среди возможных шагов
            max_value = max(available_states.values())
            # Поиск всех ходов с наивысшей ценой
            max_value_states = {}  # Словарь ходов с наивысшей ценой
            # Заполнить словарь ходов с наивысшей ценой
            for state in available_states.keys():
                if available_states[state] == max_value:
                    max_value_states[state] = available_states[state]
            # Вернуть следующее состояние с максимальной ценой (если несколько - выбрать рандомно)
            new_state, max_value = random.choice(list(max_value_states.items()))
            return new_state
        # Если шаг разведочный то выбираем случайно
        else:
            new_state, random_value = random.choice(list(available_states.items()))
            self.steps.append(new_state)
            return new_state

    # Перерасчет ценностей состояний
    def recalculation(self, n_state, n1_state):
        # Для каждого шага в прошедшей игре перерасчитать ценность по формуле:
        # Новое_значение_ценности = Старое_значение_ценности + Размер_шага * (Ценность_последнего_шага - Старое_значение_ценности)
        # Ценность_последнего_шага равна 1 (если игрок выиграл) 0,5 (если ничья) 0 (если проиграл)
        self.prices[n_state] = self.prices[n_state] + LEARNING_RATE * (self.prices[n1_state] - self.prices[n_state])


# Создание игроков
player1 = Player(1)  # Обученный играть за X
player2 = Player(2)  # Обученный играть за O
# Создание игрового поля
field = Field()
print('Загрузка противника')
field.learning_agent(player1, player2, 200000)

# Игра
while True:
    user_choice = input("За кого будете играть? Введите X или O (английские буквы): ")
    if user_choice == 'X':
        field.start_game(player2, user_choice)
    elif user_choice == 'O':
        field.start_game(player1, user_choice)
    else:
        new_game = input("Некорректный ввод! Для выхода введите 0. Для продолжения - любой символ: ")
        if new_game == '0':
            break
