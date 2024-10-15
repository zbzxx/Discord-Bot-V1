from random import choice, randint
from password_gen import generate_password
import os

# Store game state and points for each user
user_games = {}
user_points = {}

TEXT_FILES_DIR = '../text_files'
if not os.path.exists(TEXT_FILES_DIR):
    os.makedirs(TEXT_FILES_DIR)

def start_number_game(user_id: str) -> str:
    number_to_guess = randint(1, 100)
    print(f'User {user_id} has to guess {number_to_guess}')
    user_games[user_id] = {'number': number_to_guess, 'tries': 0}
    return 'I have picked a number between 1 and 100. Try to guess it!'

# Update the get_user_points function to read points from a file
def get_user_points(user_id: str) -> str:
    file_path = os.path.join(TEXT_FILES_DIR, f'{user_id}_points.txt')
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('Points:'):
                    points = int(line.split(':')[1].strip())
                    print(f'User {user_id} has {points} points')
                    break
    except FileNotFoundError:
        points = 0

    user_points[user_id] = points
    save_points_to_file(user_id)
    return f'You have {points} points.'

# Update the save_points_to_file function to save points to a file
def save_points_to_file(user_id: str) -> None:
    points = user_points.get(user_id, 0)
    file_path = os.path.join(TEXT_FILES_DIR, f'{user_id}_points.txt')
    with open(file_path, 'w') as file:
        file.write(f'User ID: {user_id}\nPoints: {points}\n')

def get_response(user_input: str, user_id: str) -> str:
    lowered = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully quiet today.'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'info' in lowered:
        return (
            "This bot was created by zbzx as a project for a Python learning course. "
            "\nIt offers a multitude of functions, including a password generator, a dice roller, a Genshin Impact character build recommender, and more! "
            "\nYou can find the source code at https://github.com/zbzxx/Discord-Bot-V1"
            "\nIf you have any questions or suggestions, feel free to ask. Additionally, if you want to learn more about the bot, you can read the documentation in the README.md file and the GitBook documentation."
        )
    elif 'help' in lowered:
        return '''
        # I can help you with the following commands:
o Hello
o How are you
o Bye
o Roll dice
o Password
o Start game
o Points
o To ask me a question in private messages, you can use the '?' prefix.
o To get a Genshin Impact character build, use the '-gc' command followed by the character name.
        '''
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    elif 'password' in lowered:
        return f'Your new password is: {generate_password(randint(8, 26))}'
    elif 'start game' in lowered:
        return start_number_game(user_id)
    elif 'points' in lowered:
        return get_user_points(user_id)
    else:
        return choice(['I do not understand...', 'What are you talking about?', 'Do you mind rephrasing that?'])
