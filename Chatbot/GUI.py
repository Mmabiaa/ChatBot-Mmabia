import tkinter as tk
from tkinter import scrolledtext
from Chatbot import get_response
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Using OOP
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Assistant Chatbot - Mmabia")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")

        # Chat log with a scrollbar
        self.chat_log = scrolledtext.ScrolledText(root, bg="#e6e6e6", state="disabled", wrap=tk.WORD, font=("Helvetica", 12))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entry box
        self.entry_box = tk.Entry(root, bg="white", font=("Helvetica", 12))
        self.entry_box.pack(padx=10, pady=(0, 10), fill=tk.X, expand=True)
        self.entry_box.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.send_button.pack(pady=(0, 10))

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.strip() == "":
            return  # Ignore empty messages

        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"You: {user_input}\n", "user")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

        logging.debug(f'User Input: {user_input}')
        response = get_response(user_input)
        logging.debug(f'Bot response: {response}')

        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, f"Bot: {response}\n", "bot")
        self.chat_log.config(state="disabled")
        self.chat_log.yview(tk.END)  # Auto-scroll to the bottom

        self.entry_box.delete(0, tk.END)  # Clear the input box

    def on_closing(self):
        logging.debug('Closing Application.')
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ChatApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Properly handle closing
        # Configure tag styles for user and bot messages
        app.chat_log.tag_configure("user", justify='right')
        app.chat_log.tag_configure("bot", justify='left')
        root.mainloop()
    except Exception as e:
        logging.debug(f'Error in main loop: {e}')
