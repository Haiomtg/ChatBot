import requests
from nltk.chat.util import Chat, reflections
import re
import random
from googletrans import Translator
import operator
import math
import sympy as sp

# Define pairs of patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I help you today?",]
    ],
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"how are you?",
        ["I'm doing well, thank you!", "I'm just a computer program, but thanks for asking!"]
    ],
    [
        r"what is your name?",
        ["I am a chatbot created by Python.",]
    ],
    [
        r"quit",
        ["Bye! Take care!"]
    ],
    [
        r"weather (.*)",
        ["Please tell me the location for the weather."]
    ],
    [
        r"time (.*)",
        ["Please tell me the location for the time checking."]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that."]
    ],
    [
        r"translate (.*) to (.*)",
        ["Translating..."]
    ],
    [
        r"calculate (.*)",
        ["Calculating..."]
    ],
    [
        r"solve (.*) for x",
        ["Solving..."]
    ]
]

# Create a chatbot instance
chatbot = Chat(pairs, reflections)

# Initialize the translator
translator = Translator()

def evaluate_math_expression(expression):
    try:
        # Remove any unwanted characters
        expression = re.sub(r'[^0-9+\-*/().^sin|cos|tan|log|sqrt| ]', '', expression)
        
        # Replace power operator for Python's eval
        expression = expression.replace('^', '**')
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": None}, {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e
        })
        
        return f"The result is: {result}"
    except Exception as e:
        return "Error: Invalid mathematical expression."

def translate_text(text, dest_language):
    try:
        translation = translator.translate(text, dest=dest_language)
        return f"Translation: {translation.text}"
    except Exception as e:
        return "Error: Unable to perform translation."

# Function to get weather data
def get_weather(location):
    api_key = "12461a8e04d978dc0ad0656c14540fd5"  # Replace with your OpenWeatherMap API key
    geocoding_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    
    # Get latitude and longitude from the Geocoding API
    response = requests.get(geocoding_url)
    data = response.json()
    
    if response.status_code == 200:
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        
        # Now use lat and lon to get the weather data
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_response.status_code == 200:
            main = weather_data["main"]
            weather_desc = weather_data["weather"][0]["description"]
            temperature = main["temp"]
            return f"The weather in {location} is {weather_desc} with a temperature of {temperature}°C."
        else:
            return "Weather data not available."
    else:
        return f"Error: {data.get('message', 'Location not found.')}"
    
def get_time(location):
    apiGeo_key = "12461a8e04d978dc0ad0656c14540fd5"  # Replace with your OpenWeatherMap API key
    geocoding_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={apiGeo_key}"
    
    # Get latitude and longitude from the Geocoding API
    responseGeo = requests.get(geocoding_url)
    data = responseGeo.json()
    if responseGeo.status_code == 200:
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        timeZone_url = f"https://api.api-ninjas.com/v1/timezone?lat={lat}&lon={lon}"
        api_key = 'RaSiEYsbffrO9+0ashd0WQ==EoaAhSr5RODbrE2P'
        response = requests.get(timeZone_url, headers={'X-Api-Key': api_key})
    
        if response.status_code == requests.codes.ok:
            time_zone_data = response.json()  # Parse the JSON response
            timezone = time_zone_data.get("timezone", "Timezone not found")  # Get the timezone value

            time_url = f"http://worldtimeapi.org/api/timezone/{timezone}"
            response = requests.get(time_url)    
            if response.status_code == 200:
                time_data = response.json()
                current_time = time_data.get("datetime", "Datetime not Found")
                return f"The current time in {location} is {current_time}."
            else:
                return "Error: Unable to retrieve time data. Please check the location."
        else:
            return "Error: Unable to retrieve time data. Please check the location."
    else:
        return f"Error: {data.get('message', 'Location not found.')}"




def solve_equation(equation):
    try:
        # Define the variable
        x = sp.symbols('x')
        
        # Split the equation into left and right parts
        left, right = equation.split('=')
        
        # Create the sympy equation
        sympy_eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
        
        # Solve the equation
        solution = sp.solve(sympy_eq, x)
        
        return f"The solution for x is: {solution}"
    except Exception as e:
        return "Error: Invalid equation format."
