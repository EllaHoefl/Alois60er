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
window = pyglet.window.Window(fullscreen = True)
background = pyglet.resource.image('background.png')

# Batch layer for all the stones and gem drawings
batch = pyglet.graphics.Batch()

# Size definition for a single square
unit_size = window.height/22

# Wall image
stone_image = pyglet.image.load('stone.png')
stone_image_size = float(stone_image.height)

# Player image and values
player_image = pyglet.image.load('alois.png')
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

def add_quiz(image_files):
    global quizes
    quiz = []
    for image in image_files:
        quiz.append(pyglet.resource.image(image))
    quizes.append(quiz)

# Startbild
add_quiz(['start.jpg'])
# Erstes Quiz
add_quiz(['Hibiskus_1.JPG','Hibiskus_2.JPG','Hibiskus_3.JPG','Hibiskus_4.JPG','Hibiskus_5.JPG','Hibiskus_6.JPG','Hibiskus_7.JPG','Frauenschuh_1.jpg','Frauenschuh_2.jpg','Frauenschuh_3.jpg','Frauenschuh_4.jpg','Frauenschuh_5.jpg','Frauenschuh_6.jpg','Frauenschuh_7.jpg'])
# Zweites Quiz
add_quiz(['Ehe_1.jpg','Ehe_2.jpg','Ehe_3.jpg','Ehe_4.jpg','Ehe_5.jpg','Ehe_6.jpg','Ehe_7.jpg','Ehe_8.jpg','Ehe_9.jpg','Ehe_10.jpg','Ehe_11.jpg','Ehe_12.jpg','Ehe_13.jpg','Ehe_14.jpg','Ehe_15.jpg','Ehe_16.jpg','Ehe_17.jpg','Ehe_18.jpg','Ehe_19.jpg','Ehe_20.jpg','Ehe_21.jpg','Ehe_22.jpg','Ehe_23.jpg'])
# Drittes Quiz
add_quiz(['Mauerbau.jpeg'])
# Viertes Quiz
add_quiz(['Freunde_1.jpg'])
# Fuenftes Quiz
add_quiz(['Fortfahren_1.jpg'])
# Sechstes Quiz
add_quiz(['Geschwister_1.jpg','Geschwister_2.jpg'])
# Siebtes Quiz
add_quiz(['Motorrad.jpg'])
# Achtes Quiz
add_quiz(['Nigeria.jpg'])

image_index = 0
quiz_index = 0

show_quiz = True


def update_game(delta_time):
    global image_index
    if not show_quiz:
        return;
    if image_index < len(quizes[quiz_index])-1:
        image_index += 1

def update_stones():
    global stone_sprites
    stone_sprites = []
    for row in range(21):
        y = (row+1) * unit_size
        for column in range(window.width/unit_size):
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
        stone_sprite = pyglet.sprite.Sprite(gem, window.width - (gem_index * unit_size), 0, batch=batch)
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
    if not show_quiz:
        if symbol == key.LEFT and is_valid(-1, 0):
            player_position_x -= 1
        elif symbol == key.RIGHT and is_valid(1, 0):
            player_position_x += 1
        elif symbol == key.UP and is_valid(0, 1):
            player_position_y += 1
        elif symbol == key.DOWN and is_valid(0, -1):
            player_position_y -= 1
    elif show_quiz and symbol == key.ENTER:
        show_quiz = False


@window.event
def on_draw():
    window.clear()
    check_for_gems()
    if show_quiz:
        quizes[quiz_index][image_index].blit(0,0, width=window.width, height=window.height)
    else:
        background.blit(0, unit_size, width=window.width, height=window.height-unit_size)

        update_stones()
        batch.draw()

        draw_player()
        player.draw()

pyglet.clock.schedule_interval(update_game, 2)
pyglet.app.run()