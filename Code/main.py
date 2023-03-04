from tkinter import *
from helper_functions import *
from tkinter import filedialog
from tkinter import messagebox
import os

# Defining the window properties
Master = Tk()
Master.title("SEDS Encryption and Decryption Application")
Master.config(background="white")
Master.iconbitmap("R_Encryption.ico")
Window_Width = 600
Window_Height = 510
key = []
input_file_name = "Untitled"



# Check if entry input is integer
def check_int(event):
    input_char = event.char
    if str.isdigit(input_char) or input_char == "" or input_char == "\x08":
        return True
    else:
        return "break"


# get the screen dimension
Screen_Width = Master.winfo_screenwidth()
Screen_Height = Master.winfo_screenheight()

# find the center point
Center_X = int(Screen_Width / 2 - Window_Width / 2)
Center_Y = int(Screen_Height / 2 - Window_Height / 2)

# set the position of the window to the center of the screen
Master.geometry(f'{Window_Width}x{Window_Height}+{Center_X}+{Center_Y}')

# Welcome label
Welcome_Text = """Welcome to the SEDS 
Encryption and Decryption Application
from Rami Issa"""
Welcome_Label = Label(Master, font="Times 20 bold italic", text=Welcome_Text, background="white")
Welcome_Label.grid(row=0, column=0, columnspan=5, padx=75, pady=30)

# Key Length Label and Input
Key_Label = Label(Master, text="Please enter the encryption key length:",
                  font="Helvetica 12", background="white")
Key_Label.grid(row=1, column=0, columnspan=3, padx=(60, 5), pady=(10, 0), sticky=W)

initial_length = 10
Key_Entry = Entry(Master, justify=CENTER)
Key_Entry.bind('<KeyPress>', check_int)
Key_Entry.insert(0, str(initial_length))
Key_Entry.grid(row=1, column=3, columnspan=2, padx=(0, 5), pady=(10, 0))

# Round Number Label and Input
Round_Label = Label(Master, text="Please enter the number of rounds:",
                    font="Helvetica 12", background="white")
Round_Label.grid(row=2, column=0, columnspan=3, padx=(60, 5), pady=(10, 0), sticky=W)

initial_round_number = 1
Round_Entry = Entry(Master, justify=CENTER)
Round_Entry.bind('<KeyPress>', check_int)
Round_Entry.insert(0, str(initial_round_number))
Round_Entry.grid(row=2, column=3, columnspan=2, padx=(0, 5), pady=(10, 0))

# Encrypt or Decrypt Label and Radio buttons
Action_Label = Label(Master, text="Please select your action:",
                     font="Helvetica 12", background="white")
Action_Label.grid(row=3, column=0, columnspan=1, padx=(60, 5), pady=(10, 0), sticky=W)

Action_Value = StringVar()
Action_Value.set("Encrypt")

Encrypt_RB = Radiobutton(Master, text="Encrypt", variable=Action_Value, value="Encrypt", background="white")
Decrypt_RB = Radiobutton(Master, text="Decrypt", variable=Action_Value, value="Decrypt", background="white")

Encrypt_RB.grid(row=3, column=2, columnspan=1, padx=(0, 5), pady=(10, 0), sticky=E)
Decrypt_RB.grid(row=3, column=3, columnspan=1, padx=5, pady=(10, 0), sticky=E)

# Input Text Label
Input_Label = Label(Master, text="Input Text:", font="Helvetica 11", anchor=W, background="white")
Input_Label.grid(row=4, column=0, columnspan=1, sticky=W, padx=(35, 5), pady=(10, 0))

# Input Entry
Input_Text_Scrollbar = Scrollbar(Master, orient='vertical')
Input_Text_Scrollbar.grid(row=5, column=2, padx=(40, 5))

Input_Text = Text(Master, width=35, height=3, border=2, yscrollcommand=Input_Text_Scrollbar.set)
Input_Text_Scrollbar.config(command=Input_Text.yview)
Input_Text.grid(row=5, column=0, columnspan=3, padx=(10, 5))


# Select input text
def select_input():
    global input_file_name
    input_path = filedialog.askopenfilename(initialdir="C:/Users/Asus/Desktop", title="Select input image",
                                            filetypes=(("Text Files", "*.txt"),
                                                       ("All Files", "*.*")))
    if input_path != "":
        input_file_name = os.path.splitext(input_path)[0].split('/')[-1]
        with open(input_path, "r", encoding="utf-8") as f:
            input_file_text = f.readlines()
            Input_Text.delete("1.0", END)
            for line in input_file_text:
                Input_Text.insert(INSERT, line)


Input_Select_Button = Button(Master, text="Get Text from File", font="Helvetica 12",
                             padx=23, pady=2, command=select_input)
Input_Select_Button.grid(row=5, column=3, columnspan=2, pady=10, padx=(0, 30))

# Output Text Label
Input_Label = Label(Master, text="Output Text:", font="Helvetica 11", anchor=W, background="white")
Input_Label.grid(row=6, column=0, columnspan=1, sticky=W, padx=(35, 5), pady=(10, 0))

# Output Text
Output_Text_Scrollbar = Scrollbar(Master, orient='vertical')
Output_Text_Scrollbar.grid(row=7, column=2, padx=(40, 5))

Output_Text = Text(Master, width=35, height=3, border=2, yscrollcommand=Output_Text_Scrollbar.set, state=DISABLED)
Output_Text_Scrollbar.config(command=Output_Text.yview)
Output_Text.grid(row=7, column=0, columnspan=3, padx=(10, 5))


# Select output directory
def select_output():
    output_text = Output_Text.get("1.0", END)
    output_text = output_text[:-1]
    if output_text != "":
        output_path = filedialog.asksaveasfile(initialfile=input_file_name + ' - Encrypted.txt',
                                               defaultextension=".txt",
                                               initialdir="C:/Users/Asus/Desktop", title="Export Text",
                                               filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if output_path != "" and output_path is not None:
            with open(output_path.name, "w", encoding="utf-8") as f:
                f.write(output_text)


Output_Select_Button = Button(Master, text="Export Text", font="Helvetica 12",
                              padx=23, pady=2, command=select_output)
Output_Select_Button.grid(row=7, column=3, columnspan=2, pady=10, padx=(0, 30))


# Key generation function
def key_generation():
    global key
    answer = True
    if len(key) > 0:
        answer = messagebox.askyesno("Changing Encryption Key",
                                     "Warning:\n" +
                                     " Changing the encryption key will prevent you from\n" +
                                     " decrypting the messages encrypted with the current\n" +
                                     " encryption key.\n\n" +
                                     " Do you want to generate an new encryption key?")
    if answer:
        key_length = int(Key_Entry.get())
        key = generate_key(key_length)
        # Check if the encryption key has been generated successfully
        if len(key) > 0:
            messagebox.showinfo("Key Generated", "The encryption key has been generated successfully")
        else:
            messagebox.showerror("Error", "Error:\n A problem has occurred while generating the encryption key")


# Run the Encryption/Decryption operation
def run():
    global key
    # Check if the encryption key has been generated first
    if len(key) > 0:
        round_number = int(Round_Entry.get())

        is_encrypt = Action_Value.get() == "Encrypt"

        input_message = Input_Text.get("1.0", END)
        if input_message[0] == "\n" and len(input_message) == 1:
            # Message Box for alerting a warning for empty input text
            messagebox.showwarning("Empty Input Text", "Warning:\n The input text can't be empty")
        else:
            while input_message[-1] == "\n":
                input_message = input_message[:-1]
            if input_message != "":
                if is_encrypt:
                    tmp_count = input_message.count('\n')
                    if tmp_count % 3 == 1:
                        input_message += '\n'
                    output_text = encrypt(input_message, key, round_number)
                else:
                    output_text = decrypt(input_message, key, round_number)
                    if output_text[-1] == '\n':
                        output_text = output_text[:-1]
                Output_Text.config(state=NORMAL)
                Output_Text.delete("1.0", END)
                Output_Text.insert(INSERT, output_text)
                Output_Text.config(state=DISABLED)
    else:
        messagebox.showwarning("Empty Encryption Key", "Warning:\n The encryption key should be generated first")


# Key Generation Button
Generate_Key_Button = Button(Master, text="Generate Key", font="Helvetica 12 bold", border=2,
                             padx=5, pady=5, command=key_generation)
Generate_Key_Button.grid(row=8, column=3, columnspan=1, padx=0, pady=20)

# Run Button
Run_Button = Button(Master, text="Run", font="Helvetica 12 bold", border=2,
                    padx=5, pady=5, command=run)
Run_Button.grid(row=8, column=4, columnspan=1, padx=(0, 20), pady=20)

if __name__ == "__main__":
    Master.mainloop()
