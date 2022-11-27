# If we try 4,3,7,8 positions ...the cods shows it as draw. But actually the bot wins there. SECOND VID

PLAYER_VALUE = 'x'
BOT_VALUE = 'o'

field = {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' ',
}


def print_field():
    print(f"{field[1]} {field[2]} {field[3]}")
    print(f"{field[4]} {field[5]} {field[6]}")
    print(f"{field[7]} {field[8]} {field[9]}")
    print('-------')


def is_free(pos):
    return True if field[pos] == ' ' else False


def check_draw():
    for key in field.keys():
        if field[key] == ' ':  # Если есть еще свободные клетки
            return False

    return True


def check_win():
    # Перечисляются все возжные комбинации для выигрыша
    if field[1] == field[2] == field[3] and not is_free(1):
        return True
    elif field[4] == field[5] == field[6] and not is_free(4):
        return True
    elif field[7] == field[8] == field[9] and not is_free(7):
        return True
    elif field[1] == field[4] == field[7] and not is_free(1):
        return True
    elif field[2] == field[5] == field[8] and not is_free(2):
        return True
    elif field[3] == field[6] == field[9] and not is_free(3):
        return True
    elif field[1] == field[5] == field[9] and not is_free(1):
        return True
    elif field[7] == field[5] == field[3] and not is_free(7):
        return True
    else:
        return False


def check_which_value_won(value):
    if field[1] == field[2] == field[3] and field[1] == value:
        return True
    elif field[4] == field[5] == field[6] and field[4] == value:
        return True
    elif field[7] == field[8] == field[9] and field[7] == value:
        return True
    elif field[1] == field[4] == field[7] and field[1] == value:
        return True
    elif field[2] == field[5] == field[8] and field[2] == value:
        return True
    elif field[3] == field[6] == field[9] and field[3] == value:
        return True
    elif field[1] == field[5] == field[9] and field[1] == value:
        return True
    elif field[7] == field[5] == field[3] and not field[7] == value:
        return True
    else:
        return False


def insert_value(pos, value):
    if is_free(pos):
        field[pos] = value
        print_field()

        if check_win():
            if value == 'o':
                print('Bot win!')
                exit()
            else:
                print('Player win!')
                exit()

        if check_draw():
            print('Draw!')
            exit()
    else:
        print('Enter another position')
        insert_value(int(input('New position: ')), value)


def minimax(field, depth, is_maximizing):
    if check_which_value_won(BOT_VALUE):
        return 1
    elif check_which_value_won(PLAYER_VALUE):
        return -1
    elif check_draw():
        return 0

    # Для бота
    if is_maximizing:
        best_score = -100

        for key in field.keys():
            if field[key] == ' ':
                field[key] = BOT_VALUE
                score = minimax(field, 0, False)  # TODO delete second and last parameters
                field[key] = ' '
                if score > best_score:
                    best_score = score

        return best_score
    # Для игрока
    else:
        best_score = 100

        for key in field.keys():
            if field[key] == ' ':
                field[key] = PLAYER_VALUE
                score = minimax(field, depth + 1, True)  # TODO delete second and last parameters
                field[key] = ' '
                if score < best_score:
                    best_score = score

        return best_score


def bot_turn():
    best_score = -100
    best_move = 0

    for key in field.keys():
        if field[key] == ' ':
            field[key] = BOT_VALUE
            score = minimax(field, 0, False)  # TODO delete second and last parameters
            field[key] = ' '
            if score > best_score:
                best_score = score
                best_move = key

    insert_value(best_move, BOT_VALUE)


def player_turn():
    insert_value(int(input(f'Enter the position for \'{PLAYER_VALUE}\': ')), PLAYER_VALUE)


# Основная функция для запуска игры
print("Player turns first!")
while not check_win():
    player_turn()
    bot_turn()
