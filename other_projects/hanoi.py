def move_tower(n, from_name, to_name, spare_name):
    if n > 0:
        move_tower(n-1, from_name, spare_name, to_name)
        print(f'Move disc {n} from {from_name} to {to_name}')
        move_tower(n-1, spare_name, to_name, from_name)

move_tower(3, 'A', 'B', 'C')
