import nltk
from nltk.chat.util import Chat, reflections
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import requests

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
        r"(.*)",
        ["I'm sorry, I don't understand that."]
    ]
]

# Create a chatbot instance
chatbot = Chat(pairs, reflections)

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

# Function to handle user input and chatbot response
def send_message():
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)
    chat_area.config(state='normal')
    chat_area.insert(tk.END, "You: " + user_input + "\n")
    
    if user_input.lower() == "quit":
        chat_area.insert(tk.END, "Chatbot: Bye! Take care!\n")
        root.quit()
    elif "weather" in user_input.lower():
        location = simpledialog.askstring("Location", "Please enter the location:")
        if location:
            weather_info = get_weather(location)
            chat_area.insert(tk.END, "Chatbot: " + weather_info + "\n")
    else:
        response = chatbot.respond(user_input)
        chat_area.insert(tk.END, "Chatbot: " + response + "\n")
    
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)  # Scroll to the end of the text area

# Function to clear chat history
def clear_chat():
    chat_area.config(state='normal')
    chat_area.delete(1.0, tk.END)
    chat_area.config(state='disabled')

# Function to change chatbot name
def change_name():
    new_name = simpledialog.askstring("Change Chatbot Name", "Enter new name for the chatbot:")
    if new_name:
        global chatbot_name
        chatbot_name = new_name
        chat_area.insert(tk.END, f"Chatbot name changed to: {chatbot_name}\n")

# Function to save chat history
def save_chat():
    with open("chat_history.txt", "w") as file:
        file.write(chat_area.get(1.0, tk.END))
    messagebox.showinfo("Save Chat", "Chat history saved to chat_history.txt")

# Set up the GUI
root = tk.Tk()
root.title("Chatbot")

chat_area = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
chat_area.grid(row=0, column=0, columnspan=2)

user_entry = tk.Entry(root, width=48)
user_entry.grid(row=1, column=0)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1)

clear_button = tk.Button(root, text="Clear Chat", command=clear_chat)
clear_button.grid(row=2, column=0)

change_name_button = tk.Button(root, text="Change Name", command=change_name)
change_name_button.grid(row=2, column=1)

save_button = tk.Button(root, text="Save Chat", command=save_chat)
save_button.grid(row=3, column=0, columnspan=2)

chatbot_name = "Chatbot"  # Default chatbot name
root.mainloop()
