import os
import random
import math
from PIL import Image

# MAP_SIZE = 200
MAP_WIDTH = 60
MAP_HEIGHT = 33
WALL = "*"
OPEN = "."
MIN_WALL_PERCENT = 10
MAX_WALL_PERCENT = 60
MIN_OPEN_REGION_PERCENT = 30
TANK1 = 'T'
TANK2 = 'L'

def load_image_as_grayscale(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image not found: " + image_path)

    image = Image.open(image_path)
    grayscale_image = image.convert("L")
    return grayscale_image

def resize_image(grayscale_image, target_width=MAP_WIDTH, target_height=MAP_HEIGHT):
    original_width, original_height = grayscale_image.size

    width_scale = target_width / original_width
    height_scale = target_height / original_height
    scale = min(width_scale, height_scale)

    new_width = max(1, round(original_width * scale))
    new_height = max(1, round(original_height * scale))

    resized = grayscale_image.resize((new_width, new_height), resample=Image.BOX)

    canvas = Image.new("L", (target_width, target_height), color=0)
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    canvas.paste(resized, (x_offset, y_offset))

    return canvas

def get_pixels(grayscale_image):
    width, height = grayscale_image.size
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            value = grayscale_image.getpixel((x, y))
            row.append(value)
        pixels.append(row)
    return pixels

#Otsu method implementation
def find_threshold(pixels):

    counts = [0] * 256
    total_pixels = 0
    for row in pixels:
        for value in row:
            counts[value] += 1
            total_pixels += 1

    overall_brightness_sum = 0
    for brightness in range(256):
        overall_brightness_sum += brightness * counts[brightness]

    best_threshold = 0
    best_score = -1

    dark_count = 0
    dark_brightness_sum = 0

    for threshold in range(256):
        dark_count += counts[threshold]
        dark_brightness_sum += threshold * counts[threshold]
        light_count = total_pixels - dark_count

        if dark_count == 0 or light_count == 0:
            continue

        dark_average = dark_brightness_sum / dark_count
        light_brightness_sum = overall_brightness_sum - dark_brightness_sum
        light_average = light_brightness_sum / light_count

        dark_weight = dark_count / total_pixels
        light_weight = light_count / total_pixels
        difference = dark_average - light_average
        score = dark_weight * light_weight * difference * difference

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold

""" Simple implementation
    THRESHOLD = 128   # pixels 0-128 = wall, 129-255 = open """

def pixels_to_map(pixels, threshold):
    char_map = []
    for row in pixels:
        map_row = []
        for value in row:
            if value <= threshold:
                map_row.append(WALL)
            else:
                map_row.append(OPEN)
        char_map.append(map_row)
    return char_map

def count_walls(char_map):
    wall_count = 0
    for row in char_map:
        for cell in row:
            if cell == WALL:
                wall_count += 1
    return wall_count

def get_wall_percentage(char_map):
    total_cells = len(char_map) * len(char_map[0])
    walls = count_walls(char_map)
    return (walls / total_cells) * 100

def find_largest_open_region(char_map):
    rows = len(char_map)
    columns = len(char_map[0])

    visited = []
    for r in range(rows):
        visited.append([False] * columns)

    largest_size = 0

    for r in range(rows):
        for c in range(columns):
            if char_map[r][c] == WALL:
                continue
            if visited[r][c]:
                continue

            region_size = 0
            stack = [(r, c)]
            visited[r][c] = True

            while len(stack) > 0:
                current_row, current_column = stack.pop()
                region_size += 1

                neighbors = [
                    (current_row - 1, current_column),
                    (current_row + 1, current_column),
                    (current_row, current_column - 1),
                    (current_row, current_column + 1),
                ]

                for neighbor_row, nc in neighbors:
                    if neighbor_row < 0 or neighbor_row >= rows:
                        continue
                    if nc < 0 or nc >= columns:
                        continue
                    if char_map[neighbor_row][nc] == WALL:
                        continue
                    if visited[neighbor_row][nc]:
                        continue

                    visited[neighbor_row][nc] = True
                    stack.append((neighbor_row, nc))

            if region_size > largest_size:
                largest_size = region_size

    return largest_size

def check_map_is_valid(char_map):
    wall_percent = get_wall_percentage(char_map)
    total_cells = len(char_map) * len(char_map[0])

    if wall_percent >= 100:
        return False, "Image is entirely dark. map is 100% walls."

    if wall_percent <= 0:
        return False, "Image is entirely light. map has 0% walls."

    if wall_percent < MIN_WALL_PERCENT:
        return False, (
            "Wall percentage is " + str(round(wall_percent, 1)) + "%, "
            "below the minimum of " + str(MIN_WALL_PERCENT) + "%. "
            "The map would be too empty."
        )

    if wall_percent > MAX_WALL_PERCENT:
        return False, (
            "Wall percentage is " + str(round(wall_percent, 1)) + "%, "
            "above the maximum of " + str(MAX_WALL_PERCENT) + "%."
        )

    largest_region = find_largest_open_region(char_map)
    region_pct = (largest_region / total_cells) * 100

    if region_pct < MIN_OPEN_REGION_PERCENT:
        return False, (
            "Largest open region is only " + str(round(region_pct, 1)) + "% "
            "of the map (minimum required: " + str(MIN_OPEN_REGION_PERCENT) + "%)."
        )

    return True, "OK"

def remove_isolated_walls(char_map):
    rows = len(char_map)
    columns = len(char_map[0])

    new_map = []
    for row in char_map:
        new_map.append(row[:])

    for r in range(rows):
        for c in range(columns):
            if char_map[r][c] != WALL:
                continue

            has_wall_neighbor = False

            if r > 0 and char_map[r - 1][c] == WALL:
                has_wall_neighbor = True
            if r < rows - 1 and char_map[r + 1][c] == WALL:
                has_wall_neighbor = True
            if c > 0 and char_map[r][c - 1] == WALL:
                has_wall_neighbor = True
            if c < columns - 1 and char_map[r][c + 1] == WALL:
                has_wall_neighbor = True

            if not has_wall_neighbor:
                new_map[r][c] = OPEN

    return new_map

def add_tank_spawns(char_map):
    rows = len(char_map)
    columns = len(char_map[0])
    open_spots = []

    # Find all open floor coordinates
    for r in range(rows):
        for c in range(columns):
            if char_map[r][c] == OPEN:
                open_spots.append((r, c))

    # if map is too small
    if len(open_spots) < 2:
        return char_map

    # shuffle open spaces to pick on at random
    random.shuffle(open_spots)
    t_row, t_col = open_spots[0]
    char_map[t_row][t_col] = TANK1

    # find a space that is far enough away from the other tank
    min_distance = min(rows, columns) // 3
    l_row, l_col = open_spots[1]

    # calculate the straight line distance between 2 points
    for r, c in open_spots[1:]:
        distance = math.sqrt((r-t_row)**2 + (c - t_col)**2)
        if distance >= min_distance:
            l_row, l_col = r, c
            break

    char_map[l_row][l_col] = TANK2

    return char_map

def write_map_to_file(char_map, output_path):
    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for row in char_map:
            line = ""
            for cell in row:
                line += cell
            f.write(line + "\n")

def generate_map(image_path, output_path):
    # Step 1: Load the image
    try:
        image = load_image_as_grayscale(image_path)
    except FileNotFoundError as error:
        return False, str(error)
    except Exception as error:
        return False, "Failed to load image: " + str(error)

    # Step 2: Resize to fit the map grid
    resized = resize_image(image)

    # Step 3: Get the pixel values as a 2D list
    pixels = get_pixels(resized)

    # Step 4: Find the best threshold to separate dark and light
    threshold = find_threshold(pixels)

    # Step 5: Convert pixels to wall/open characters
    char_map = pixels_to_map(pixels, threshold)

    # Step 6: Check if the map is valid as-is
    is_valid, reason = check_map_is_valid(char_map)

    # Step 7: If the problem is too many walls, try cleaning up
    if not is_valid and get_wall_percentage(char_map) > MAX_WALL_PERCENT:
        char_map = remove_isolated_walls(char_map)
        is_valid, reason = check_map_is_valid(char_map)

    # add the tank spawn locations
    char_map = add_tank_spawns(char_map)

    # Step 8: If still not valid, report the error
    if not is_valid:
        return False, reason

    # Step 9: Write the map to the output file
    write_map_to_file(char_map, output_path)
    return True, char_map