import os
import sys
import time

screen_width = 100


#########
# Игрок #
#########
class player:
    def __init__(self):
        self.name = ''
        self.feeling = ''
        self.astrological = ''
        self.position = 'ground'
        self.won = False
        self.solves = 0


player1 = player()

#########
# Карта	#
#########

DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = False
SIDE_UP = 'up', 'forward'
SIDE_DOWN = 'down', 'back'
SIDE_LEFT = 'left',
SIDE_RIGHT = 'right',

room_solved = {'top': False, 'north': False, 'ground': False, 'east': False, 'west': False, 'south': False, }

cube = {
    'top': {
        DESCRIPTION: "Как ни странно, вы обнаруживаете, что нормально стоите на облаках.",
        INFO: "Еще более странным, чем стоять на облаках, является\nптица, которая начинает с вами разговаривать.\n",
        PUZZLE: "Птица устрашающе спрашивает:\nБез крыльев я летаю. Без глаз я вижу. Без рук я поднимаюсь.\n Пугливее, чем любой зверь, сильнее чем любой враг.\nМне свойственны хитрость, безжалостность, я могу прихвастнуть.\nВ конце концов я всегда беру верх.'\n'Кто я?'",
        SOLVED: "воображение",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'east',
        SIDE_RIGHT: 'west',
    },
    'north': {
        DESCRIPTION: "Вы попадаете в холодную арктическую долину.\nВ соседней пещере ярко пылает костер.",
        INFO: "Теперь вы стоите лицом к лицу с гигантским йети.",
        PUZZLE: "Йети спрашивает вас: «Что кусается без зубов?»",
        SOLVED: "мороз",
        SIDE_UP: 'top',
        SIDE_DOWN: 'ground',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    },
    'ground': {
        DESCRIPTION: "Вы попадаете в довольно красивое, обычное травянистое поле.\nЧто-то не так, как будто это ядро мира.",
        INFO: "Довольно большой, хотя и легко незаметный золотой ключ\nстоит вертикально в поле.\nКак странно.",
        PUZZLE: "Ключ находится в замочной скважине соответствующего размера,\nскрытой грязью и травой. Кажется, он не поворачивается.",
        SOLVED: False,
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    },
    'east': {
        DESCRIPTION: "Вы попадаете в пышный лес, полный дикой природы\n и какафонического щебетания.",
        INFO: "Рядом с маленькой хижиной сидит мужчина грубого вида.\nЕго глаза прикованы к биноклю для наблюдения за птицами.",
        PUZZLE: "Мужчина грубого вида спрашивает: «Какова скорость полета порожней европейской ласточки?» (мили в час)",
        SOLVED: "24",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'ground',
        SIDE_RIGHT: 'top',
    },
    'west': {
        DESCRIPTION: 'Вы окажетесь окруженным сильным ветром и песчаными дюнами.',
        INFO: 'Среди кактусов прячется испуганный мужчина.',
        PUZZLE: "Напуганный человек спрашивает: «Что может измерять время, когда в конце концов все рушится?»",
        SOLVED: "песок",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'top',
        SIDE_RIGHT: 'ground',
    },
    'south': {
        DESCRIPTION: "Вы оказываетесь рядом с успокаивающим прудом.\nСтарик пристально смотрит на столик неподалеку.",
        INFO: "Вы приветствуете старика.\nОн манит вас посмотреть на замысловатый двенадцатигранный стол.",
        PUZZLE: "На каждой стороне стола есть уникальный символ, хотя все они вам знакомы.\Рядом с каким символом вы сидите?",
        SOLVED: "",  # Ваш знак зодиака.
        SIDE_UP: 'ground',
        SIDE_DOWN: 'top',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    }
}


def clear_console():
    os.system('cls')


########
# Меню #
########
def title_screen_options():
    option = input("> ")
    if option.lower() == "играть":
        setup_game()
    elif option.lower() == "выход":
        sys.exit()
    elif option.lower() == "помощь":
        help_menu()
    while option.lower() not in ['играть', 'помощь', 'выход']:
        print("Неверная команда, попробуйте еще раз.")
        option = input("> ")
        if option.lower() == "играть":
            setup_game()
        elif option.lower() == "выход":
            sys.exit()
        elif option.lower() == "помощь":
            help_menu()


def title_screen():
    clear_console()
    print('#' * 45)
    print('# Добро пожаловать в текстовую RPG головоломку')
    print('#' * 45)
    print("                 .: Играть :.                  ")
    print("                 .: Помощь :.                  ")
    print("                 .: Выход :.                  ")
    title_screen_options()


##########
# Помощь #
##########
def help_menu():
    print("")
    print('#' * 45)
    print("~" * 45)
    print("Введите команду такую как 'двигаться' затем 'налево'")
    print("чтобы перемещаться по кубу-головоломке.\n")
    print("Введите 'посмотреть' или 'изучить' чтобы")
    print("взаимодействовать с головоломками в комнатах.\n")
    print("Головоломки потребуют различных входных данных и, ")
    print("возможно, ответов из внешних знаний.\n")
    print("Для удобства вводите строчными буквами.\n")
    print('#' * 45)
    print("\n")
    print('#' * 45)
    print("    Пожалуйста, выберите вариант, чтобы продолжить.     ")
    print('#' * 45)
    print("                 .: Играть :.                  ")
    print("                 .: Помощь :.                  ")
    print("                 .: Выход :.                  ")
    title_screen_options()


########
# Игра #
########
quitgame = 'выход'


def print_location():
    print('\n' + ('#' * (4 + len(player1.position))))
    print('# ' + player1.position.upper() + ' #')
    print('#' * (4 + len(player1.position)))
    print('\n' + (cube[player1.position][DESCRIPTION]))


def prompt():
    if player1.solves == 5:
        print("Кажется, что-то в мире изменилось. Хм...")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Что бы вы хотели сделать?")
    action = input("> ")
    acceptable_actions = ['двигаться', 'идти', 'путешествовать', 'выйти', 'осмотреть', 'изучить', 'посмотреть', 'искать']
    while action.lower() not in acceptable_actions:
        print("Неизвестная команда действия, попробуйте еще раз.\n")
        action = input("> ")
    if action.lower() == quitgame:
        sys.exit()
    elif action.lower() in ['двигаться', 'идти', 'путешествовать']:
        move(action.lower())
    elif action.lower() in ['осмотреть', 'изучить', 'посмотреть', 'искать']:
        examine()


def move(myAction):
    askString = "Куда бы вы хотели " + myAction + " ?\n> "
    destination = input(askString)
    if destination == 'вперед':
        move_dest = cube[player1.position][SIDE_UP]  # if you are on ground, should say north
        move_player(move_dest)
    elif destination == 'налево':
        move_dest = cube[player1.position][SIDE_LEFT]
        move_player(move_dest)
    elif destination == 'направо':
        move_dest = cube[player1.position][SIDE_RIGHT]
        move_player(move_dest)
    elif destination == 'назад':
        move_dest = cube[player1.position][SIDE_DOWN]
        move_player(move_dest)
    else:
        print("Неверная команда направления. Попробуйте использовать команду «Вперед», «Назад», «Влево» или «Вправо».\n")
        move(myAction)


def move_player(move_dest):
    print("\nВы отправились " + move_dest + ".")
    player1.position = move_dest
    print_location()


def examine():
    if room_solved[player1.position] == False:
        print('\n' + (cube[player1.position][INFO]))
        print((cube[player1.position][PUZZLE]))
        puzzle_answer = input("> ")
        checkpuzzle(puzzle_answer)
    else:
        print("Здесь вы не увидите ничего нового.")


def checkpuzzle(puzzle_answer):
    if player1.position == 'ground':
        if player1.solves >= 5:
            endspeech = (
                "Без вашего участия ключ начинает вращаться.\nНачинается дождь.\nВсе стороны коробки начинают рушиться внутрь.\nСвет начинает сиять сквозь трещины в стенах.\nУдаряет ослепляющая вспышка света.\nВы сбежали!")
            for character in endspeech:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(0.05)
            print("\nПОЗДРАВЛЯЕМ!")
            sys.exit()
        else:
            print("Кажется, по-прежнему ничего не происходит...")
    elif player1.position == 'south':
        if puzzle_answer == (player1.astrological):
            room_solved[player1.position] = True
            player1.solves += 1
            print("Вы решили головоломку. Вперед!")
            print("\nРешены головоломки: " + str(player1.solves))
        else:
            print("Неверный ответ! Попробуйте еще раз.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
            examine()
    else:
        if puzzle_answer == (cube[player1.position][SOLVED]):
            room_solved[player1.position] = True
            player1.solves += 1
            print("Вы решили головоломку. Вперед!")
            print("\nРешены головоломки: " + str(player1.solves))
        else:
            print("Неверный ответ! Попробуйте еще раз.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
            examine()


def main_game_loop():
    total_puzzles = 6
    while player1.won is False:
        prompt()


###############
# Запуск игры #
###############
def setup_game():
    clear_console()

    question1 = "Здравствуйте, как ваше имя?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    player1.name = player_name

    question2 = "Мой дорогой друг " + player1.name + ", как вы себя чувствуете?\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    feeling = input("> ")
    player1.feeling = feeling.lower()

    good_adj = ['хороший', 'отличный', 'рохит', 'счастливый', 'светлый', 'понимающий', 'отличный', 'в порядке', 'спокойный', 'уверенный',
                'неплохо', 'мужественный', 'спокойный', 'надежный', 'радостный', 'энергичный', 'на', 'легко', 'просто', 'удачливый',
                'к', 'комфортный', 'удивленный', 'удачливый', 'оптимистичный', 'довольный', 'свободный', 'восхищенный', 'шикарный',
                'воодушевленный', 'хорошо', 'обрадованный', 'импульсивный', 'умный', 'заинтересованный', 'ликующий', 'свободный', 'удивленный',
                'довольный', 'благодарный', 'резвый', 'довольный', 'восприимчивый', 'важный', 'оживленный', 'спокойный', 'хорошо',
                'праздничный', 'одухотворенный', 'определенный', 'добрый', 'экстатический', 'взволнованный', 'расслабленный', 'удовлетворенный', 'замечательный',
                'безмятежный', 'радостный', 'свободный', 'и', 'легкий', 'веселый', 'яркий', 'солнечный', 'благословенный', 'веселый', 'успокоенный',
                'восторженный', '1738', 'любовь', 'заинтересованный', 'позитивный', 'сильный', 'любящий']
    hmm_adj = ['idk', 'concerned', 'lakshya', 'eager', 'impulsive', 'considerate', 'affected', 'keen', 'free',
               'ласковый', 'очарованный', 'серьезный', 'уверенный', 'чувствительный', 'заинтригованный', 'намеренный', 'определенный', 'нежный',
               'поглощенный', 'тревожный', 'мятежный', 'преданный', 'любознательный', 'вдохновленный', 'уникальный', 'привлекательный', 'любопытный',
               'решительный', 'динамичный', 'страстный', 'любопытный', 'возбужденный', 'упорный', 'восхищение', 'увлеченный',
               'восторженный', 'выносливый', 'теплый', 'любопытный', 'смелый', 'надежный', 'тронутый', 'храбрый', 'сочувствие', 'смелый',
               'близкий', 'сложный', 'любимый', 'оптимистичный', 'утешенный', 'повторный', 'вынужденный', 'влекущий', 'к',
               'уверенность', 'надежда', 'трудный']
    bad_adj = ['плохо', 'плохо', 'грустно', 'голодно', 'неприятно', 'чувства', 'сердито', 'подавленно', 'растерянно', 'беспомощно',
               'раздраженный', 'паршивый', 'расстроенный', 'неспособный', 'разгневанный', 'разочарованный', 'сомневающийся', 'одинокий', 'враждебный',
               'обескураженный', 'неуверенный', 'парализованный', 'оскорбленный', 'стыд', 'нерешительный', 'усталый', 'болезненный',
               'бессильный', 'недоумевающий', 'бесполезный', 'раздраженный', 'уменьшенный', 'смущенный', 'неполноценный', 'расстроенный',
               'виноватый', 'нерешительный', 'уязвимый', 'ненавистный', 'недовольный', 'стеснительный', 'пустой', 'неприятный', 'несчастный',
               'одурманенный', 'вынужденный', 'обидный', 'отвратительный', 'разочарованный', 'нерешительный', 'горький', 'отвратительный',
               'неверующий', 'отчаяние', 'агрессивный', 'презрительный', 'скептический', 'разочарованный', 'обиженный',
               'отвращение', 'недоверие', 'огорчение', 'воспаление', 'мерзость', 'недовольство', 'горе', 'провокация',
               'ужасный', 'потерянный', 'жалкий', 'негодующий', 'в', 'отчаянии', 'неуверенный', 'трагический', 'разгневанный', 'сердитый',
               'беспокойный', 'крест', 'плохой', 'пессимистичный', 'доминирующий', 'работал', 'поднялся', 'а', 'чувство', 'о', 'потеря',
               'напряженный', 'кипящий', 'дымящийся', 'возмущенный', 'равнодушный', 'испуганный', 'обиженный', 'грустный', 'бесчувственный',
               'боязливый', 'раздавленный', 'плаксивый', 'унылый', 'испуганный', 'измученный', 'печальный', 'бесстрастный',
               'подозрительный', 'лишенный', 'болезненный', 'нейтральный', 'тревожный', 'болезненный', 'горе', 'сдержанный', 'встревоженный',
               'замученный', 'страдание', 'усталый', 'паника', 'удрученный', 'опустошенный', 'скучающий', 'нервный', 'отвергнутый',
               'отчаянный', 'озабоченный', 'испуганный', 'раненый', 'пессимистичный', 'холодный', 'обеспокоенный', 'обиженный', 'несчастный',
               'незаинтересованный', 'испуганный', 'страдающий', 'одинокий', 'безжизненный', 'робкий', 'болящий', 'огорченный', 'дрожащий',
               'пострадавший', 'скорбный', 'беспокойный', 'разбитое сердце', 'встревоженный', 'сомневающийся', 'мучимый', 'угрожаемый',
               'потрясенный', 'трусливый', 'униженный', 'дрожащий', 'обиженный', 'угрожающий', 'отчужденный', 'настороженный']

    if player1.feeling in good_adj:
        feeling_string = "Я рад, что вы чувствуете себя"
    elif player1.feeling in hmm_adj:
        feeling_string = "Это интересно, что вы чувствуете себя"
    elif player1.feeling in bad_adj:
        feeling_string = "Мне жаль слышать, что вы чувствуете себя"
    else:
        feeling_string = "Я не знаю, каково это - чувствовать себя"

    question3 = f"Что ж, тогда {player1.name}, {feeling_string} {player1.feeling}.\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    question4 = "Теперь скажите мне, какой у вас знак зодиака?\n"
    for character in question4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    print("#####################################################")
    print("# Пожалуйста, напечатайте название, чтобы указать свой знак.")
    print("# ♈ Aries (Овен)")
    print("# ♉ Taurus (Телец)")
    print("# ♊ Gemini (Близнецы)")
    print("# ♋ Cancer (Рак)")
    print("# ♌ Leo (Лев)")
    print("# ♍ Virgo (Дева)")
    print("# ♎ Libra (Весы)")
    print("# ♏ Scorpio (Скорпион)")
    print("# ♐ Sagittarius (Стрелец)")
    print("# ♑ Capricorn (Козерог)")
    print("# ♒ Aquarius (Водолей)")
    print("# ♓ Pisces (Рыбы)")
    print("#####################################################")
    astrological = input("> ")
    acceptable_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
                        'capricorn', 'aquarius', 'pisces']

    while astrological.lower() not in acceptable_signs:
        print("Это неприемлемый знак, попробуйте еще раз.")
        astrological = input("> ")
    player1.astrological = astrological.lower()

    speech1 = f"Ах, {player1.astrological}, как интересно. Ну что ж.\n"
    speech2 = f"Кажется, здесь нам придется расстаться, {player1.name}.\n"
    speech3 = "Как жаль.\n"
    speech4 = "О, вы не знаете, где вы? Хорошо...\n"
    speech5 = "К счастью, я оставил вас в небольшой головоломке. Надеюсь, вам удастся выбраться из этого ящика.\n"
    speech6 = "Хех. Хех.. Хех...\n"
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech5:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech6:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.2)
    time.sleep(1)

    clear_console()
    print("################################")
    print("# Здесь начинаются приключения... #")
    print("################################\n")
    print("Вы оказываетесь в центре странного места.\nКажется, вы заперты в маленькой коробочке.\n")
    print("Кажется, что каждая внутренняя поверхность коробки имеет свою тему.\nКак из этого выбраться...\n")
    print("Вы замечаете предметы, стоящие боком на стенах.\nНе действует ли гравитация? Хотя облака есть...")
    main_game_loop()


title_screen()
