from tkinter import scrolledtext, messagebox
import tkinter as tk
from chatbot import *
import os, random

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Assistant Chatbot - Mmabiaa")
        self.root.geometry("400x550")
        self.root.configure(bg="black")

        # Chat log with a scrollbar
        self.chat_log = scrolledtext.ScrolledText(root, bg="white", state="disabled", wrap=tk.WORD, font=("Helvetica", 12))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entry box
        self.entry_box = tk.Entry(root, bg="white", font=("Helvetica", 12))
        self.entry_box.pack(padx=10, pady=(0, 10), fill=tk.X, expand=True)
        self.entry_box.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.send_button.pack(pady=(0, 10))

        # Initialize game state variables
        self.players = []
        self.current_player = 0
        self.scores = {}
        self.game_running = False

        # Initial greeting message
        self.greet_user()

    def greet_user(self):
        """Send a greeting message when the app is first opened."""
        greeting = "Hey, I am Mmabia, your personal AI. How can I assist you today?"
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"Bot: {greeting}\n", "bot")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.strip() == "":
            return  # Ignore empty messages

        # Display user input
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"You: {user_input}\n", "user")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

        logging.debug(f'User Input: {user_input}')

        # Process user input through the chatbot response function
        response = self.get_response(user_input)
        logging.debug(f'Bot response: {response}')

        # Display chatbot response
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"Bot: {response}\n", "bot")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

        # Clear the entry box after sending the message
        self.entry_box.delete(0, tk.END)

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.strip() == "":
            return  # Ignore empty messages

        # Display user input
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"You: {user_input}\n", "user")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

        logging.debug(f'User Input: {user_input}')

        # Process user input through the chatbot response function
        response = self.get_response(user_input)
        logging.debug(f'Bot response: {response}')

        # Display chatbot response
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"Bot: {response}\n", "bot")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

        # Clear the entry box after sending the message
        self.entry_box.delete(0, tk.END)

    def get_response(self, user_input):
        # Handle all the responses for the different features
        if self.game_running:
            if "roll" in user_input.lower():
                return self.roll_dice()
            elif "quit" in user_input.lower() or "end game" in user_input.lower():
                return self.end_dice_game()

        # Handling to-do list commands
        if "add task" in user_input.lower():
            task = user_input.replace("add task", "").strip()
            return self.add_task(task)
        elif "remove task" in user_input.lower():
            task = user_input.replace("remove task", "").strip()
            return self.remove_task(task)
        elif "show tasks" in user_input.lower() or "todo list" in user_input.lower():
            return self.show_tasks()

        # Password manager interactions
        if "set password" in user_input.lower():
            account_name = user_input.split("for")[1].strip()
            password = user_input.split("set password")[1].split("for")[0].strip()
            return self.set_password(account_name, password)
        elif "retrieve password" in user_input.lower():
            account_name = user_input.replace("retrieve password for", "").strip()
            return self.retrieve_password(account_name)

        # Default response from chatbot.py
        return get_response(user_input)

    def start_dice_game(self):
        """Start the dice game, asking for number of players."""
        self.players = []
        self.current_player = 0
        self.scores = {}
        self.game_running = True
        return "Welcome to the Dice Game! How many players are there?"

    def roll_dice(self):
        """Handle the dice roll for the game."""
        roll_value = random.randint(1, 6)
        if roll_value == 1:
            self.scores[self.players[self.current_player]] = 0  # Player loses all points for this round
            self.current_player = (self.current_player + 1) % len(self.players)
            return f"Player {self.players[self.current_player]} rolled a 1! All points lost for this turn."
        else:
            self.scores[self.players[self.current_player]] += roll_value
            self.current_player = (self.current_player + 1) % len(self.players)
            return f"Player {self.players[self.current_player]} rolled a {roll_value}. Current score: {self.scores[self.players[self.current_player]]}"

    def end_dice_game(self):
        """End the dice game and display the winner."""
        self.game_running = False
        winner = max(self.scores, key=self.scores.get)
        return f"Game over! The winner is {winner} with {self.scores[winner]} points."

    def add_task(self, task):
        """Add task to the to-do list."""
        try:
            with open('tasks.txt', 'a') as file:
                file.write(f"{task}\n")
            return f"Task '{task}' added."
        except Exception as e:
            logging.error(f"Error adding task: {e}")
            return "Error adding task."

    def remove_task(self, task):
        """Remove task from the to-do list."""
        try:
            with open('tasks.txt', 'r') as file:
                tasks = file.readlines()
            with open('tasks.txt', 'w') as file:
                for t in tasks:
                    if t.strip() != task:
                        file.write(t)
            return f"Task '{task}' removed."
        except Exception as e:
            logging.error(f"Error removing task: {e}")
            return "There was an error removing the task."

    def show_tasks(self):
        """Display all tasks in the to-do list."""
        try:
            if os.path.exists('tasks.txt'):
                with open('tasks.txt', 'r') as file:
                    tasks = file.readlines()
                if tasks:
                    return "\n".join([task.strip() for task in tasks])
                else:
                    return "No tasks found."
            else:
                return "No tasks file found."
        except Exception as e:
            logging.error(f"Error reading tasks: {e}")
            return "There was an error fetching the tasks."

    def set_password(self, account_name, password):
        """Set a password for an account."""
        # Password encryption logic goes here
        return f"Password for {account_name} has been set."

    def retrieve_password(self, account_name):
        """Retrieve a password for an account."""
        # Password decryption logic goes here
        return f"The password for {account_name} is: ********"

    def on_closing(self):
        logging.debug('Closing Application.')
        self.root.destroy()

# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
