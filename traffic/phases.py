<<<<<<< HEAD
# traffic/phases.py

# Просто переменные-константы, чтобы не писать везде строки руками
NS_GREEN = "NS_GREEN"   # Зеленый для Севера и Юга
NS_YELLOW = "NS_YELLOW" # Желтый (пока не используем, но пусть будет)
EW_GREEN = "EW_GREEN"   # Зеленый для Востока и Запада
EW_YELLOW = "EW_YELLOW"
ALL_RED = "ALL_RED"     # Всем красный (безопасная пауза)
=======
# These names are easier to read than raw strings all over the code.
# NS means north-south. EW means east-west.
# These are just shared phase labels used all over the project.
NS_GREEN = "NS_GREEN"   # North and south can move.
NS_YELLOW = "NS_YELLOW" # Short warning before red.
EW_GREEN = "EW_GREEN"   # East and west can move.
EW_YELLOW = "EW_YELLOW"
ALL_RED = "ALL_RED"     # Small safety pause. Nobody moves.
>>>>>>> master
