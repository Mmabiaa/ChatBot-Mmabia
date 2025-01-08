from weather import get_weather
from reminders import set_reminder, set_alarm, reminder_alert, alarm_alert
import logging, re, wolframalpha, threading, nltk, spacy
from nltk.chat.util import Chat, reflections
from transformers import pipeline
from sympy import sympify
from datetime import datetime, timedelta
from nltk.chat.util import Chat, reflections


# Load a pre-trained model for question answering
nlp_qa = pipeline("question-answering")


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure NLTK data is downloaded
nltk.download('punkt')

# Attempt to load the spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
    logging.debug('SpaCy model loaded successfully.')
except OSError:
    logging.error("Model 'en_core_web_sm' not found. Downloading and installing...")
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
    logging.debug('SpaCy model downloaded and loaded successfully.')

# Wolfram Alpha client
WOLFRAM_ALPHA_APP_ID = 'JUHEQJ-7QT668WQKU'  
wolfram_client = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I help you today?",]
    ],
    [
        r"hi|hey|hello|Mmabia|Hi|Hello|Hey",
        ["Hello!", "Hey there!",]
    ],
    [
        r'Thank you|thank you',
        ["You're welcome, feel free to ask more questions"]
    ],
    [
        r"what is your name?|What are you called|What is your name",
        ["I am Mmabia, a personal assistant chatbot.",]
    ],
    [
        r"how are you?|How are you|how are you|How are you?",
        ["I'm doing well, thank you! How can I assist you today?",]
    ],
    [
        r"what can you do?|what do you do|What can you do?|what can you do",
        ["I can help you with a variety of tasks like answering questions, setting reminders, providing weather updates, giving information, and performing calculations.",]
    ],
    [
        r"weather in (.*)|what is the weather at(.*)|what is the weather in(.*)",
        ["Hold on, let me check the weather in %1",]
    ],
    [
        r"what is the date today|what is today's date|show today's date|Toady's date|today's date",
        ["Today's date is %1",]
    ],
    [
        r"what is the time now|what time is it|Show current time|display Current time",
        ["The current time is %1",]
    ],
    [
        r"set a reminder for (.*)|Set a reminder for",
        ["Reminder set for %1",]
    ],
    [
        r"set an alarm for (.*)|Set an alarm for",
        ["Alarm set for %1",]
    ],
    [
        r"quit|goodbye|bye|Bye|Close|Goodbye|close",
        ["Goodbye! Have a great day!",]
    ],
    [
        r"what advice can you give me|What advice can you give me",
        ["Keep believing in God and have faith through Christ Jesus",]
    ],
    [
        r"what is your favourite colour|What is your favourite colour|What is your favourite colour",
        ["Aqua is my favorite color",]
    ],
    [
        r"what is your favourite food|What is your favourite food|What is your favourite food",
        ["I love eating Gob3 with my best friend Manny!!!",]
    ],
    [
        r"what is your favourite movie|What is your favourite movie|What is your favourite movie",
        ["My favorite movie is the CHI",]
    ],
    [
        r"who owns you|who is your author|Who designed you|who designed you",
        ["I was designed by Boateng Prince Agyenim, a student of UMaT",]
    ],
    [
        r"who is your creator|Who is your creator|Who is your creator",
        ["I was created by Boateng Prince Agyenim, a student of UMaT",]
    ],
    [
        r"I love you|i love you",
        ["I love you too",]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that. Can you please rephrase?",]
    ],
]

chatbot = Chat(pairs, reflections)

def get_response(user_input):
    logging.debug(f"Received user input: {user_input}")
    try:
        # Check if the input is a mathematical expression
        if is_math_expression(user_input):
            result = calculate_expression(user_input)
            if result is not None:
                return f"The result is {result}"
            else:
                return "I'm sorry, I couldn't calculate that. Please check the expression and try again."

        doc = nlp(user_input)
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # GPE (Geopolitical entity) for locations
                city = ent.text
                logging.debug(f"Recognized city: {city}")
                weather_response = get_weather(city)
                if weather_response:
                    return weather_response

        if re.search(r'date today|today\'s date', user_input, re.I):
            return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"

        if re.search(r'time now|time is it', user_input, re.I):
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

        if match := re.search(r'reminder for (.*)', user_input, re.I):
            reminder_time = match.group(1).strip()
            set_reminder(reminder_time)
            return f"Reminder set for {reminder_time}"

        if match := re.search(r'alarm for (.*)', user_input, re.I):
            alarm_time = match.group(1).strip()
            set_alarm(alarm_time)
            return f"Alarm set for {alarm_time}"

        response = chatbot.respond(user_input)
        if response and "I don't understand" not in response:
            return response
        else:
            wolfram_response = query_wolfram_alpha(user_input)
            if wolfram_response:
                return wolfram_response
            else:
                return "I'm sorry, I don't understand that. Can you please rephrase?"
    except Exception as e:
        logging.error(f'Error processing input: {e}')
        return "I'm sorry, something went wrong. Please try again."

def is_math_expression(user_input):
    # Simple check for mathematical expressions using regex
    return bool(re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', user_input))

def calculate_expression(expression):
    try:
        # Evaluate the expression safely
        result = sympify(expression)
        return result
    except Exception as e:
        logging.error(f'Error calculating expression: {e}')
        return None
    

def query_wolfram_alpha(query):
    try:
        res = wolfram_client.query(query)
        if res['@success'] == 'true':
            result = next(res.results).text
            logging.debug(f"Wolfram Alpha response: {result}")
            return result
        else:
            logging.error(f"No results from Wolfram Alpha for query: {query}")
            return None
    except Exception as e:
        logging.error(f'Error querying Wolfram Alpha: {e}')
        return None