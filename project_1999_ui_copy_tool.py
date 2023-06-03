# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog
import shutil
import glob

# Function to save the last selected directory to a file
def save_last_directory(directory_path):
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "last_directory.txt")
    with open(file_path, "w") as file:
        file.write(directory_path)

# Function to load the last selected directory from the file
def load_last_directory():
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "last_directory.txt")
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return ""

def update_file_dropdown():
    # Clear the file dropdown
    file_dropdown['menu'].delete(0, 'end')

    # Get the directory path
    directory_path = directory_entry.get()

    # Get server files
    filesGreenAndRed = glob.glob(os.path.join(directory_path, "UI_*_P1999*.ini"))
    filesBlue = glob.glob(os.path.join(directory_path, "UI_*project1999.ini"))
    files = filesGreenAndRed + filesBlue
    files.sort()

    # Add the files to the file dropdown
    for file in files:
        file_path =  os.path.basename(file)
        server = get_character_server(file_path)
        if (server == "(Blue)"):
            display_value = file_path.split("_project1999", 1)[0].replace("UI_", "") + f" {server}"
        else:    
            display_value = file_path.split("_P1999", 1)[0].replace("UI_", "") + f" {server}"
        file_dropdown['menu'].add_command(label=display_value, command=lambda file=file_path, display=display_value: select_file(file, display))

    # Set the default value for the file dropdown
    selected_file_label.set("Select file")

def update_destination_dropdown():
    # Clear the destination dropdown ####
    destination_dropdown['menu'].delete(0, 'end')

    # Get the directory path
    directory_path_destination = directory_entry.get()

    # Get server files
    filesGreenAndRed = glob.glob(os.path.join(directory_path_destination, "UI_*_P1999*.ini"))
    filesBlue = glob.glob(os.path.join(directory_path_destination, "UI_*project1999.ini"))
    files_destination = filesGreenAndRed + filesBlue
    files_destination.sort()

    # Add the files to the file dropdown
    for file in files_destination:
        file_path =  os.path.basename(file)
        server = get_character_server(file_path)
        display_value = ""
        if (server == "(Blue)"):
            display_value = file_path.split("_project1999", 1)[0].replace("UI_", "") + f" {server}"
        else:    
            display_value = file_path.split("_P1999", 1)[0].replace("UI_", "") + f" {server}"
        destination_dropdown['menu'].add_command(label=display_value, command=lambda file=file_path, display=display_value: select_destination(file, display))

    # Set the default value for the destination dropdown ####
    selected_destination_label.set("Select file")

def copy_and_rename():
    # get files
    ui_layout_source_file = os.path.join(directory_entry.get(), selected_file.get())
    friends_and_macros_source_file = os.path.join(directory_entry.get(), selected_file.get().replace("UI_", ""))
    ui_layout_destination_file = os.path.join(directory_entry.get(), selected_destination.get())
    friends_and_macros_destination_file = os.path.join(directory_entry.get(), selected_destination.get().replace("UI_", ""))
    
    # determine if either dropdown not selected
    if selected_file.get() == "Select file" or selected_destination.get() == "Select file":
        success_label.config(text="Select source and destination characters", fg="red")
    # determine if selected same file for both dropdowns
    elif ui_layout_source_file == ui_layout_destination_file:
        success_label.config(text="Please select a different destination character", fg="red")
    else:
        # get checkbox values
        copy_ui_layout_selected = copy_ui_layout.get()
        copy_macro_and_friends_selected = copy_macro_and_friends.get()
        # determine if at least 1 checkbox setting is true
        if not copy_ui_layout_selected and not copy_macro_and_friends_selected: 
            success_label.config(text="Please select either UI Layout or Macro/Friends", fg="red")
        else:        
            try:
                if copy_ui_layout_selected:
                    shutil.copyfile(ui_layout_source_file, ui_layout_destination_file)
                if copy_macro_and_friends_selected:
                    shutil.copyfile(friends_and_macros_source_file, friends_and_macros_destination_file)
                success_label.config(text="Success!", fg="green")
            except Exception as e:
                success_label.config(text="Error!", fg="red")

def select_directory():
    directory_path = filedialog.askdirectory(initialdir=load_last_directory())
    if directory_path:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(tk.END, directory_path)
        save_last_directory(directory_path)

        # Update the file dropdown
        update_file_dropdown()

        # If a file is already selected, update the destination dropdown
        update_destination_dropdown()

        clear_success()

def select_file(selection, display_value):
    selected_file_label.set(display_value);
    selected_file.set(selection)
    clear_success()

def select_destination(selection, display_value):
    selected_destination_label.set(display_value);
    selected_destination.set(selection)
    clear_success()

def clear_success():
    # Clear the success indicator
    success_label.config(text="")
    
def get_character_server(file_path):
    if "project1999.ini" in file_path:
        return "(Blue)"
    elif "P1999PVP.ini" in file_path:
        return "(Red)"
    else:
        # For green and future servers
        start = "_P1999"
        end = ".ini"
        # Find the starting and ending indices
        start_index = file_path.index(start) + len(start)
        end_index = file_path.index(end)
        # Extract the server between start and end
        server = file_path[start_index:end_index]
        return f"({server})"

def close_window():
    window.destroy()

# Create the main window
window = tk.Tk()
window.title("Project 1999 - UI Copy Tool")

# Create the UI elements
directory_label = tk.Label(window, text="Project 1999 directory:")
directory_label.grid(row=0, column=0, sticky="w")
directory_entry = tk.Entry(window)
directory_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = tk.Button(window, text="Browse", command=select_directory)
browse_button.grid(row=0, column=2, padx=5, pady=5)

file_label = tk.Label(window, text="Character file:")
file_label.grid(row=1, column=0, sticky="w")
selected_file = tk.StringVar(window)
selected_file_label = tk.StringVar(window)
file_dropdown = tk.OptionMenu(window, selected_file_label, "Select Project 1999 directory")
file_dropdown.grid(row=1, column=1, padx=5, pady=5)

destination_label = tk.Label(window, text="Destination Character File:")
destination_label.grid(row=2, column=0, sticky="w")
selected_destination = tk.StringVar(window)
selected_destination_label = tk.StringVar(window)
destination_dropdown = tk.OptionMenu(window, selected_destination_label, "Select Project 1999 directory")
destination_dropdown.grid(row=2, column=1, padx=5, pady=5)

copy_ui_layout = tk.BooleanVar(value=True)
copy_ui_layout_checkbox = tk.Checkbutton(window, text="UI Layout", variable=copy_ui_layout)
copy_ui_layout_checkbox.grid(row=3, column=0, padx=(20), pady=(10, 0), sticky="w")

copy_macro_and_friends = tk.BooleanVar(value=True)
copy_macro_and_friends_checkbox = tk.Checkbutton(window, text="Macros/Friends", variable=copy_macro_and_friends)
copy_macro_and_friends_checkbox.grid(row=3, column=1, pady=(10, 0), sticky="w")

copy_button = tk.Button(window, text="Copy", command=copy_and_rename, font=("TkDefaultFont", 10, "bold"), relief=tk.RAISED)
copy_button.grid(row=4, column=0, columnspan=3, padx=(40,40), ipadx=75, pady=(20, 0), sticky="we")

success_label = tk.Label(window, text="")
success_label.grid(row=5, column=0, columnspan=2, pady=5)

# Load the last selected directory
last_directory = load_last_directory()
if last_directory:
    directory_entry.insert(tk.END, last_directory)
    update_file_dropdown()
    update_destination_dropdown()

window.protocol("WM_DELETE_WINDOW", close_window)

try:
    # Start the main event loop
    window.mainloop()
except KeyboardInterrupt:
    close_window()

# run pyinstaller --onefile --noconsole your_script.py to rebuild executable
