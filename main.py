# If we try 4,3,7,8 positions ...the cods shows it as draw. But actually the bot wins there. SECOND VID

field = {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' ',
}


def print_field():
    print(f"{field[1]} {field[2]} {field[3]}")
    print(f"{field[4]} {field[5]} {field[6]}")
    print(f"{field[7]} {field[8]} {field[9]}")


def is_free(pos):
    return True if field[pos] == ' ' else False


def check_draw():
    for key in field.keys():
        if key == ' ':  # Если есть еще свободные клетки
            return False

    return True


def check_win():
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


def insertValue(pos, value):
    if is_free(pos):
        field[pos] = value
        print_field()

        if check_draw():
            print('Draw!')
            exit()

        if check_win():
            if value == 'x':
                print('Bot win!')
                exit()
            else:
                print('Player win!')
                exit()
    else:
        print('Enter another position')
        insertValue(int(input('New position: ')))
        return

