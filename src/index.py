import pyglet   # import libary pyglet by pip 
from pyglet.window import key

platform = pyglet.window.get_platform()
display = platform.get_default_display()
screens = display.get_screens()
screenid=min(len(screens)-1,1)
mainWindow = pyglet.window.Window(fullscreen=True, screen=screens[screenid])

backgroundImage = pyglet.resource.image('LabyrinthSpirte.jpg')
image_files = ['chromosomes_1.png','chromosomes_2.png','chromosomes_3.png','chromosomes.png']
quiz_images = []
for image in image_files:
    quiz_images.append(pyglet.resource.image(image))
image_index = 0

show_quiz_images = True

def update_game(delta_time):
    global image_index
    if image_index < len(quiz_images)-1:
        image_index += 1

@mainWindow.event
def on_key_press(symbol, modifiers):
    global show_quiz_images
    if symbol == key.ENTER:
        show_quiz_images = False


@mainWindow.event
def on_draw():
    mainWindow.clear()
    if show_quiz_images:
        quiz_images[image_index].blit(0,0, width=mainWindow.width, height=mainWindow.height)
    else:
        backgroundImage.blit(0,0, width=mainWindow.width, height=mainWindow.height)

pyglet.clock.schedule_interval(update_game, 2)
pyglet.app.run()