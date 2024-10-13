import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from chatbot_service import get_weather, chatbot, get_time, translate_text, evaluate_math_expression, solve_equation  # Importing the service functions
import re    

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
    elif "time" in user_input.lower():
        location = simpledialog.askstring("Location", "Please enter the location for the time:")
        if location:
            time_info = get_time(location)
            chat_area.insert(tk.END, "Chatbot: " + time_info + "\n")
    elif "translate" in user_input.lower():
        match = re.search(r'translate (.+) to (.+)', user_input.lower())
        if match:
            text_to_translate = match.group(1).strip()
            dest_language = match.group(2).strip()
            translation = translate_text(text_to_translate, dest_language)
            chat_area.insert(tk.END, "Chatbot: " + translation + "\n")
    elif "calculate" in user_input.lower():
        match = re.search(r'calculate (.*)', user_input.lower())
        if match:
            math_expression = match.group(1).strip()
            result = evaluate_math_expression(math_expression)
            chat_area.insert(tk.END, "Chatbot: " + result + "\n")
    elif "solve" in user_input.lower():
        match = re.search(r'solve (.*) for x', user_input.lower())
        if match:
            equation = match.group(1).strip()
            result = solve_equation(equation)
            chat_area.insert(tk.END, "Chatbot: " + result + "\n")
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

chat_area = scrolledtext.ScrolledText(root, state='disabled')
chat_area.grid(row=0, column=0, columnspan=5)

user_entry = tk.Entry(root, width=50)
user_entry.grid(row=1, column=0, columnspan=4)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=4)

clear_button = tk.Button(root, text="Clear Chat", command=clear_chat)
clear_button.grid(row=2, column=0)

change_name_button = tk.Button(root, text="Change Name", command=change_name)
change_name_button.grid(row=2, column=1)

save_button = tk.Button(root, text="Save Chat", command=save_chat)
save_button.grid(row=2, column=2, columnspan=2)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.grid(row=3, column=2, columnspan=2)

chatbot_name = "Chatbot"  # Default chatbot name



root.mainloop()
