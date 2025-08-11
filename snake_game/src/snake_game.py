import turtle as t
import time
import random

# --- Configuración general ---
WIDTH, HEIGHT = 600, 600
STEP = 20
DELAY = 0.1  # velocidad inicial

# --- Ventana ---
wn = t.Screen()
wn.title("Snake Retro 2D")
wn.bgcolor("black")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)

# --- Funciones auxiliares ---
def create_segment(x, y):
    seg = t.Turtle()
    seg.speed(0)
    seg.shape("square")
    seg.color("white")  # solo blanco
    seg.penup()
    seg.goto(x, y)
    return seg

def random_grid_pos():
    x = random.randrange(-WIDTH//2 + STEP, WIDTH//2 - STEP, STEP)
    y = random.randrange(-HEIGHT//2 + STEP, HEIGHT//2 - STEP, STEP)
    return x, y

# --- Snake ---
head = create_segment(0, 0)
snake = []
dx, dy = STEP, 0

# --- Comida ---
food = t.Turtle()
food.speed(0)
food.shape("square")  # igual que la serpiente, estilo retro
food.color("white")
food.penup()
food.goto(random_grid_pos())

# --- Marcador ---
score = 0
pen = t.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, HEIGHT//2 - 30)
pen.write("SCORE: 0", align="center", font=("Courier", 16, "normal"))

# --- Controles ---
def go_up():
    global dx, dy
    if dy == 0:
        dx, dy = 0, STEP

def go_down():
    global dx, dy
    if dy == 0:
        dx, dy = 0, -STEP

def go_left():
    global dx, dy
    if dx == 0:
        dx, dy = -STEP, 0

def go_right():
    global dx, dy
    if dx == 0:
        dx, dy = STEP, 0

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# --- Reinicio ---
def reset_game():
    global score, dx, dy, snake
    time.sleep(0.5)
    head.goto(0, 0)
    dx, dy = STEP, 0
    for seg in snake:
        seg.goto(1000, 1000)
    snake.clear()
    score = 0
    update_score()

def update_score():
    pen.clear()
    pen.write(f"SCORE: {score}", align="center", font=("Courier", 16, "normal"))

# --- Bucle principal ---
while True:
    wn.update()

    # mover cuerpo
    for i in range(len(snake) - 1, 0, -1):
        snake[i].goto(snake[i - 1].xcor(), snake[i - 1].ycor())
    if snake:
        snake[0].goto(head.xcor(), head.ycor())

    # mover cabeza
    head.setx(head.xcor() + dx)
    head.sety(head.ycor() + dy)

    # colisión con borde
    if (head.xcor() > WIDTH//2 - STEP or head.xcor() < -WIDTH//2 + STEP or
        head.ycor() > HEIGHT//2 - STEP or head.ycor() < -HEIGHT//2 + STEP):
        reset_game()

    # colisión con cuerpo
    for seg in snake:
        if head.distance(seg) < 10:
            reset_game()

    # comida
    if head.distance(food) < 15:
        food.goto(random_grid_pos())
        snake.append(create_segment(head.xcor(), head.ycor()))
        score += 1
        update_score()

    time.sleep(DELAY)
