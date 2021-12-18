from itertools import count

def find_highest_y(min_x, max_x, min_y, max_y):

    # maximize the number of steps until we reach the x area
    for start_vel_x in count(1):

        x_vel = start_vel_x
        has_hit_target = False
        x_pos = 0

        for step in count():
            if x_pos >= min_x and x_pos <= max_x:
                has_hit_target = True

            if x_vel == 0:
                break

            x_pos += x_vel
            x_vel -= 1

        if has_hit_target:
            break

    best_y_vel = -min_y - 1

    highest_y = (best_y_vel * (best_y_vel + 1)) // 2 
    
    return highest_y


def count_total_num(min_x, max_x, min_y, max_y):

    count = 0

    for start_x_vel in range(max_x + 1):
        for start_y_vel in range(min_y, -min_y):
            has_hit_target = False
            x_pos = y_pos = 0
            x_vel = start_x_vel
            y_vel = start_y_vel
            while True:
                if x_pos >= min_x and x_pos <= max_x and y_pos >= min_y and y_pos <= max_y:
                    has_hit_target = True
                    break

                if x_vel == 0 and y_pos < min_y:
                    break

                x_pos += x_vel
                y_pos += y_vel

                if x_vel > 0:
                    x_vel -= 1

                y_vel -= 1

            count += has_hit_target

    return count


if __name__ == "__main__":
    assert find_highest_y(20, 30, -10, -5) == 45
    assert find_highest_y(96, 125, -144, -98) == 10296
    # print(find_highest_y(96, 125, -144, -98))

    assert count_total_num(20, 30, -10, -5) == 112
    assert count_total_num(96, 125, -144, -98) == 2371