import PySimpleGUI as sg

# Initial list of items
items = ["Item 1", "Item 2", "Item 3"]

layout = [
    [sg.Listbox(values=items, size=(30, 6), key="-LISTBOX-", enable_events=True)],
    [sg.Button("Remove Selected Item")],
    [sg.Button("Exit")]
]

window = sg.Window("Remove Items from Listbox", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Remove Selected Item":
        selected_indices = window["-LISTBOX-"].get_indexes()
        
        if selected_indices:
            selected_index = selected_indices[0]
            print(selected_index)
            
            items.pop(selected_index)
            window["-LISTBOX-"].update(values=items)

window.close()