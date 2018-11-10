import pyglet   # import libary pyglet by pip 
from pyglet.window import key

platform = pyglet.window.get_platform()
display = platform.get_default_display()
screens = display.get_screens()
screenid=min(len(screens)-1,1)
mainWindow = pyglet.window.Window(fullscreen=True, screen=screens[screenid])

backgroundImage = pyglet.resource.image('LabyrinthSpirte.jpg')
quizes = []

image_files = ['chromosomes_1.png','chromosomes_2.png','chromosomes_3.png','chromosomes.png']
quiz = []
for image in image_files:
    quiz.append(pyglet.resource.image(image))
quizes.append(quiz)

image_files = ['Alois_1.jpg','Alois_2.jpg','Alois_3.jpg','Alois_4.jpg','Alois_5.jpg']
quiz = []
for image in image_files:
    quiz.append(pyglet.resource.image(image))
quizes.append(quiz)

image_index = 0
quiz_index = 1
show_quiz_images = True


def update_game(delta_time):
    global image_index
    if image_index < len(quizes[quiz_index])-1:
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
        quizes[quiz_index][image_index].blit(0,0, width=mainWindow.width, height=mainWindow.height)
    else:
        backgroundImage.blit(0,0, width=mainWindow.width, height=mainWindow.height)

pyglet.clock.schedule_interval(update_game, 2)
pyglet.app.run()