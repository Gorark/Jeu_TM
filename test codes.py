import PySimpleGUI as sg

# Initial data for the table
data = [
    ["Tool 1", "Type A", "Available"],
    ["Tool 2", "Type B", "In Use"],
    ["Tool 3", "Type C", "Available"]
]

# Table headings
headings = ["Tool Name", "Type", "Status"]

# List to store selected row values
tools = []

# Define the layout
layout = [
    [sg.Table(values=data, headings=headings, max_col_width=25, auto_size_columns=True,
              display_row_numbers=True, justification='center', num_rows=5, key='-TABLE-',
              enable_events=True, enable_click_events=True)],
    [sg.Text("Selected Tools:"), sg.Text("", size=(40, 1), key='-TOOLS-')],
    [sg.Button("Exit")]
]

# Create the window
window = sg.Window("Tool Selection Table", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == '-TABLE-':
        selected_row_index = values['-TABLE-'][0]  # Get the index of the selected row
        selected_tools = data[selected_row_index][0]  # Get the data of the selected row and the first column
        tools.append(selected_row)  # Add the selected row to the tools list
        window['-TOOLS-'].update(tools)  # Update the Text element to show selected tools
        print(tools)

window.close()