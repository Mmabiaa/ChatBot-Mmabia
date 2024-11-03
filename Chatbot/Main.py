from GUI import ChatApp
import tkinter as tk

if __name__ == "__main__":

        root = tk.Tk()
        app = ChatApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Properly handle closing
        # Configure tag styles for user and bot messages
        app.chat_log.tag_configure("user", justify='right')
        app.chat_log.tag_configure("bot", justify='left')
        root.mainloop()
    
