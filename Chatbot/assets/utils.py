import logging

# Set up logging configuration
logging.basicConfig(filename='chatbot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def log_user_input(user_input):
    """Log the user's input to a file."""
    logging.info(f"User: {user_input}")

def log_bot_response(bot_response):
    """Log the bot's response to a file."""
    logging.info(f"Bot: {bot_response}")

def sanitize_input(user_input):
    """Sanitize user input by stripping whitespace and converting to lowercase."""
    return user_input.strip().lower()

def format_response(response):
    """Format the bot's response for display."""
    return f"Bot: {response}"

def reset_log():
    """Reset the log file by clearing its contents."""
    open('chatbot.log', 'w').close()
