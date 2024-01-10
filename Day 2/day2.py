def make_game_dict(filename):
    """
    Dictionary of Games:
        List of Rounds:
            Dictionary of colors shown
    """
    game_data = []
    with open(filename, 'r') as f:
        game_data = f.read().splitlines()
    game_dict = {}
    # Each game (dict):
    for line in game_data:
        game_id = line.split(':')
        game_dict[game_id[0]] = []
        # Each Round (list):
        for round in game_id[1].split(";"):
            total_colors = {
                "red": 0, 
                "green": 0, 
                "blue": 0
            }
            # Each color (dict):
            for color in round.split(","):
                if "red" in color:
                    total_colors["red"] = int(color[1:].split(" ")[0])
                elif "green" in color:
                    total_colors["green"] = int(color[1:].split(" ")[0])
                elif "blue" in color:
                    total_colors["blue"] = int(color[1:].split(" ")[0])

            game_dict[game_id[0]].append(total_colors)


    return game_dict

def check_for_valid_games(games_dict: dict[list[dict]], rgb: dict):
    all_valid_games = []

    for game in games_dict:
        check = check_game(games_dict[game], rgb)
        if check:
            number = int(game.split(" ")[1])
            all_valid_games.append(number)
    
    return all_valid_games

def check_game(game, rgb):
    for round in game:
        for color in round:
            if round[color] > rgb[color]:
                return False
    return True

def games_dict_to_powerset(games_dict):
    """Structure of lists:
        Game (list):
            MinColors (dict): 
            * {red, green, blue}
    """
    # Games:
    colors = []
    for game in games_dict:
        min_colors = {
            "red": 0,
            "green": 0, 
            "blue": 0
        }
        # Rounds:
        for round in games_dict[game]:
            # Colors:
            for color in round:
                if round[color] > min_colors[color]: # Find largest value for each color
                    min_colors[color] = round[color]
        colors.append(min_colors)
    
    # Make a list of games, where the value at each index is red*green*blue
    games_list = []
    for game in colors:
        games_list.append(game['red']*game['green']*game['blue'])
    
    return sum(games_list)


if __name__ == "__main__":
    game_dict = make_game_dict("input.txt")
    rgb = {
        "red": 12,
        "green": 13, 
        "blue": 14}
    valid_games = check_for_valid_games(game_dict, rgb)
    print(sum(valid_games))

    print(games_dict_to_powerset(game_dict))