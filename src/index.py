import pyglet   # import libary pyglet by pip 
from pyglet.window import key

# Labyrinth definitions, including walls and gems
labyrinth_file = open("labyrinth.txt", "r")
labyrinth_lines = labyrinth_file.readlines() 
labyrinth = []
gems = []
for line in labyrinth_lines:
    row = []
    gem_row = []
    for char in line:
        if char.isspace():
            row.append(False)
            gem_row.append(-1)
        elif char == ".":
            row.append(True)
            gem_row.append(-1)
        else:
            row.append(False)
            gem_row.append(ord(char) - 65)
    labyrinth.append(row)
    gems.append(gem_row)

# Pyglet window and background
window = pyglet.window.Window(fullscreen = False)
background = pyglet.resource.image('background.png')

window_width = int(window.width)
window_height = int(window.height)

# Batch layer for all the stones and gem drawings
batch = pyglet.graphics.Batch()

# Size definition for a single square
unit_size = window_height/22

# Wall image
stone_image = pyglet.image.load('stone.png')
stone_image_size = float(stone_image.height)

# Player image and values
player_image = pyglet.image.load('alois.jpg')
player_image_size = float(player_image.height)
player = pyglet.sprite.Sprite(player_image)
player.scale = unit_size / player_image_size
player.x = 0
player.y = unit_size * 2
player_position_x = 0
player_position_y = 1

# How many fields the labyrinth needs to be shifted right
labyrinth_shift = 0

# Gem images - using a grid image
gems_image = pyglet.image.load('gems.png')
gems_seq = pyglet.image.ImageGrid(gems_image, 4, 5)

gems_gained = []


# Image quiz definitions
quizes = []
wait_for_space = []

def add_quiz(wait, image_files):
    global quizes
    quiz = []
    wait_for_space.append(wait)
    for image in image_files:
        quiz.append(pyglet.resource.image(image))
    quizes.append(quiz)

# Startbild
add_quiz([], ['start.jpg'])
# Erstes Quiz
add_quiz([5,6,12,13], [
    'Blumen_1.jpg','Blumen_2.jpg','Blumen_3.jpg','Blumen_4.jpg','Blumen_5.jpg','Blumen_6.jpg','Blumen_7.jpg','Blumen_8.jpg','Blumen_9.jpg',
    'Blumen_10.jpg','Blumen_11.jpg','Blumen_12.jpg','Blumen_13.jpg','Blumen_14.jpg','Blumen_15.jpg','Blumen_16.jpg','Blumen_17.jpg',
    'Blumen_18.jpg','Blumen_19.jpg','Blumen_20.jpg','Blumen_21.jpg','Blumen_22.jpg','Blumen_23.jpg','Blumen_24.jpg','Blumen_25.jpg',
    'Blumen_26.jpg','Blumen_27.jpg','Blumen_28.jpg'
])
# Zweites Quiz
add_quiz([7,22], [
    'Ehe_1.jpg','Ehe_2.jpg','Ehe_3.jpg','Ehe_4.jpg','Ehe_5.jpg','Ehe_6.jpg','Ehe_7.jpg','Ehe_8.jpg','Ehe_9.jpg','Ehe_10.jpg',
    'Ehe_11.jpg','Ehe_12.jpg','Ehe_13.jpg','Ehe_14.jpg','Ehe_15.jpg','Ehe_16.jpg','Ehe_17.jpg','Ehe_18.jpg','Ehe_19.jpg','Ehe_20.jpg',
    'Ehe_21.jpg','Ehe_22.jpg','Ehe_23.jpg','Ehe_24.jpg','Ehe_25.jpg','Ehe_26.jpg','Ehe_27.jpg','Ehe_28.jpg','Ehe_29.jpg','Ehe_30.jpg','Ehe_31.jpg'
])
# Drittes Quiz
add_quiz([], ['Mauerbau.jpg'])
# Viertes Quiz
add_quiz([], ['Freunde_1.jpg','Freunde_2.jpg','Freunde_3.jpg','Freunde_4.jpg','Freunde_5.jpg','Freunde_6.jpg','Freunde_7.jpg'])
# Fuenftes Quiz
add_quiz([], ['Fortfahren_1.jpg','Fortfahren_2.jpg','Fortfahren_3.jpg','Fortfahren_4.jpg','Fortfahren_5.jpg','Fortfahren_6.jpg'])
# Sechstes Quiz
add_quiz([], [
    'Geschwister_1.jpg','Geschwister_2.jpg','Geschwister_3.jpg','Geschwister_4.jpg','Geschwister_5.jpg','Geschwister_6.jpg',
    'Geschwister_7.jpg','Geschwister_8.jpg','Geschwister_9.jpg','Geschwister_10.jpg','Geschwister_11.jpg','Geschwister_13.jpg',
    'Geschwister_14.jpg','Geschwister_15.jpg','Geschwister_16.jpg','Geschwister_17.jpg','Geschwister_18.jpg','Geschwister_19.jpg',
    'Geschwister_20.jpg','Geschwister_21.jpg','Geschwister_22.jpg','Geschwister_23.jpg','Geschwister_24.jpg','Geschwister_25.jpg'
])
# Siebtes Quiz
add_quiz([], ['Motorrad.jpg'])
# Achtes Quiz
add_quiz([], ['Nigeria.jpg'])

IMAGE_DISPLAY_DURATION = 2.0

image_index = 0
image_time_remaining = IMAGE_DISPLAY_DURATION
quiz_index = 0

show_quiz = True


def update_game(delta_time):
    global image_index
    global image_time_remaining

    if not show_quiz:
        return;
    if image_index < len(quizes[quiz_index])-1 and not image_index in wait_for_space[quiz_index]:
        image_time_remaining -= delta_time
        if image_time_remaining <= 0.0:
            image_index += 1
            image_time_remaining = IMAGE_DISPLAY_DURATION

def update_stones():
    global stone_sprites
    stone_sprites = []
    for row in range(21):
        y = (row+1) * unit_size
        for column in range(int(window_width/unit_size)):
            x = column * unit_size
            if column + labyrinth_shift >= len(labyrinth[row]):
                continue
            if labyrinth[row][column + labyrinth_shift]:
                stone_sprite = pyglet.sprite.Sprite(stone_image, x, y, batch=batch)
                stone_sprite.scale = unit_size / stone_image_size
                stone_sprites.append(stone_sprite)
            elif gems[row][column + labyrinth_shift] >= 0:
                gem = gems_seq[gems[row][column + labyrinth_shift]]
                stone_sprite = pyglet.sprite.Sprite(gem, x, y, batch=batch)
                stone_sprite.scale = unit_size / stone_image_size
                stone_sprites.append(stone_sprite)

    gem_index = 0
    for gem_type in gems_gained:
        gem = gems_seq[gem_type]
        gem_index += 1
        stone_sprite = pyglet.sprite.Sprite(gem, window_width - (gem_index * unit_size), 0, batch=batch)
        stone_sprite.scale = unit_size / stone_image_size
        stone_sprites.append(stone_sprite)

def check_for_gems():
    global gems
    global labyrinth_shift
    global quiz_index
    global image_index
    global show_quiz
    global gems_gained
    gem = gems[player_position_y][player_position_x]
    if gem >= 0:
        labyrinth_shift += 12
        gems[player_position_y][player_position_x] = -1
        quiz_index = gem
        gems_gained.append(gem)
        image_index = 0
        show_quiz = True

def draw_player():
    global player
    player.x = (player_position_x - labyrinth_shift) * unit_size
    player.y = (player_position_y + 1) * unit_size

def is_valid(x, y):
    temp_x = player_position_x + x
    temp_y = player_position_y + y
    if temp_x < 0 or temp_x >= len(labyrinth[0]):
        return False
    if temp_y < 1 or temp_y >= len(labyrinth) -1:
        return False
    if labyrinth[temp_y][temp_x]:
        return False
    return True


@window.event
def on_key_press(symbol, modifiers):
    global show_quiz
    global player_position_x
    global player_position_y
    global image_index
    if not show_quiz:
        if symbol == key.LEFT and is_valid(-1, 0):
            player_position_x -= 1
        elif symbol == key.RIGHT and is_valid(1, 0):
            player_position_x += 1
        elif symbol == key.UP and is_valid(0, 1):
            player_position_y += 1
        elif symbol == key.DOWN and is_valid(0, -1):
            player_position_y -= 1
    elif show_quiz and symbol == key.SPACE:
        if image_index == len(quizes[quiz_index]) - 1:
            show_quiz = False
        elif image_index in wait_for_space[quiz_index]:
            image_index += 1


@window.event
def on_draw():
    window.clear()
    check_for_gems()
    if show_quiz:
        quizes[quiz_index][image_index].blit(0,0, width=window_width, height=window_height)
    else:
        background.blit(0, unit_size, width=window_width, height=window_height-unit_size)

        update_stones()
        batch.draw()

        draw_player()
        player.draw()

pyglet.clock.schedule_interval(update_game, 1.0/120.0)
pyglet.app.run()