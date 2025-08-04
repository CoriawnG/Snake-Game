import tkinter as tk
import random

# Initialize game window
root = tk.Tk()
root.title("Snake Game")
root.geometry("500x500")
canvas = tk.Canvas(root, bg="black", width=500, height=500)
canvas.pack()

# Snake and Food
snake = [(240, 240), (230, 240), (220, 240)]  # List of snake segments
food = (random.randint(0, 49) * 10, random.randint(0, 49) * 10)  # Random food position
direction = "Right"
next_direction = "Right"
score = 0
game_over = False

# Draw initial state
def draw_snake():
    canvas.delete("snake")
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0]+10, segment[1]+10, fill="green", tags="snake")

def draw_food():
    canvas.delete("food")
    canvas.create_rectangle(food[0], food[1], food[0]+10, food[1]+10, fill="red", tags="food")

def reset_game():
    global snake, food, direction, next_direction, score, game_over
    snake = [(240, 240), (230, 240), (220, 240)]  # Reset snake position
    food = (random.randint(0, 49) * 10, random.randint(0, 49) * 10)  # Generate new food
    direction = "Right"
    next_direction = "Right"
    score = 0
    game_over = False
    canvas.delete("all")  # Clear canvas
    draw_snake()
    draw_food()
    move_snake()

def move_snake():
    global food, score, direction, next_direction, game_over

    # Update direction safely
    direction = next_direction

    if game_over:
        return

    # Update snake position
    head_x, head_y = snake[0]
    if direction == "Up":
        head_y -= 10
    elif direction == "Down":
        head_y += 10
    elif direction == "Left":
        head_x -= 10
    elif direction == "Right":
        head_x += 10
    snake.insert(0, (head_x, head_y))  # Add new head

    # Check if snake eats food
    if snake[0] == food:
        score += 1
        food = (random.randint(0, 49) * 10, random.randint(0, 49) * 10)
    else:
        snake.pop()  # Remove tail if no food eaten

    # Check for collision
    if (head_x < 0 or head_x >= 500 or head_y < 0 or head_y >= 500 or
        snake[0] in snake[1:]):
        game_over = True
        canvas.create_text(250, 250, text="Game Over", fill="white", font=("Helvetica", 24))
        canvas.create_text(250, 280, text="Press 'R' To Retry", fill="white", font=("Helvetica", 16))
        return

    draw_snake()
    draw_food()
    root.after(100, move_snake)

def change_direction(event):
    global next_direction
    # Prevent the snake from reversing direction
    if event.keysym == "Up" and direction != "Down":
        next_direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        next_direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        next_direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        next_direction = "Right"
    elif event.keysym == "r":  # Restart the game when "R" is pressed
        reset_game()

def create_retry_button():
    retry_button = tk.Button(root, text="Retry", command=reset_game, bg="white", fg="black", font=("Helvetica", 12))
    retry_button.pack()

# Bind keys for movement and restart
root.bind("<Up>", change_direction)
root.bind("<Down>", change_direction)
root.bind("<Left>", change_direction)
root.bind("<Right>", change_direction)
root.bind("<r>", change_direction)  # Bind "R" key to restart

# Start game
draw_snake()
draw_food()
move_snake()
create_retry_button()

root.mainloop()