import cohere
import tkinter as tk
from tkinter import messagebox

# Set your Cohere API key here
api_key = '1x80ZH7kbo388pl1NneQIAIuIIWhXJb9s4QObRLn'
co = cohere.Client(api_key)

class EmailPrompt:
    def __init__(self, user_prompt, recipient_name, sender_name, sender_position):
        self.user_prompt = user_prompt
        self.recipient_name = recipient_name
        self.sender_name = sender_name
        self.sender_position = sender_position

    def to_prompt(self):
        return f"""
### User Prompt: {self.user_prompt}

### Recipient Information:
- Name: {self.recipient_name}

### Sender Information:
- Name: {self.sender_name}
- Position: {self.sender_position}

### Generated Email:
"""

def generate_email(prompt: EmailPrompt):
    full_prompt = prompt.to_prompt()
    
    response = co.generate(
        model='command-xlarge-nightly',  # Use the appropriate model
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.7,
    )
    
    email_body = response.generations[0].text.strip()
    return email_body

def generate_email_and_display():
    user_prompt = entry_user_prompt.get()
    recipient_name = entry_recipient_name.get()
    sender_name = entry_sender_name.get()
    sender_position = entry_sender_position.get()

    if not user_prompt or not recipient_name or not sender_name or not sender_position:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    prompt = EmailPrompt(user_prompt, recipient_name, sender_name, sender_position)
    email_body = generate_email(prompt)
    
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, email_body)
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("AI Email Generator")

# Create and place the labels and entry widgets
tk.Label(root, text="Enter your email prompt:").grid(row=0, column=0, sticky=tk.W)
entry_user_prompt = tk.Entry(root, width=50)
entry_user_prompt.grid(row=0, column=1)

tk.Label(root, text="Enter recipient name:").grid(row=1, column=0, sticky=tk.W)
entry_recipient_name = tk.Entry(root, width=50)
entry_recipient_name.grid(row=1, column=1)

tk.Label(root, text="Enter your name:").grid(row=2, column=0, sticky=tk.W)
entry_sender_name = tk.Entry(root, width=50)
entry_sender_name.grid(row=2, column=1)

tk.Label(root, text="Enter your position:").grid(row=3, column=0, sticky=tk.W)
entry_sender_position = tk.Entry(root, width=50)
entry_sender_position.grid(row=3, column=1)

# Create and place the generate button
generate_button = tk.Button(root, text="Generate Email", command=generate_email_and_display)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create and place the text widget for displaying the result
result_text = tk.Text(root, height=15, width=70, state=tk.DISABLED)
result_text.grid(row=5, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()
