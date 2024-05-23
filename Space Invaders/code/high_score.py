def read_high_score(file_path):
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def write_high_score(file_path, score):
    with open(file_path, 'w') as file:
        file.write(str(score))
