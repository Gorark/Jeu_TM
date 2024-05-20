import FreeSimpleGUI as sg
from time import sleep
sg.theme('Dark Grey 13')
def layout1():
    money=0
    tab_layout1 = [[sg.Text("Choose your Mission:"),sg.Listbox(["Mission 1", "Mission Proposal 2", "Mission Proposal 3", "Mission Proposal 4", "Mission Proposal 5"],size=(300, 50),enable_events=True,key='MissionList')]]
    tab_layout2 = [[sg.Button('Team Management'),]]
    tab_layout3 = [[sg.Listbox(["Password Cracker", "Mission Proposal 2", "Mission Proposal 3", "Mission Proposal 4", "Mission Proposal 5"],size=(300, 50),enable_events=True,key='Market')]]
    layout = [[sg.Text(f"Money:{money}",key="pippo", font=("Calibri", 20))], [sg.Button("Free money")] ]
    #layout.append([sg.Graph(background_color='gray', graph_bottom_left=(0,0), graph_top_right=(2500, 1250), canvas_size=(2500, 1250),key="fond")])
    layout.append([sg.TabGroup([[sg.Tab("Mission", tab_layout1), sg.Tab("Team", tab_layout2),sg.Tab("Market", tab_layout3)]])])
    

    window = sg.Window('Generated Layouts', layout, finalize=True)
    #rectangle = window['fond'].DrawRectangle((10,10), (1250,1240), fill_color='gray', line_color='black'  )  
    sg.Popup("Welcome to CyberOps Entreprises.",no_titlebar=True,font="Default 20")
    sleep(0.2)
    sg.Popup("You are probably confused we're going to show you around don't worry\n\nFirst head to the [Missions] tab and press the [Mission 1] button for a little check",no_titlebar=True,font="Default 20")
    event, values = window.read()
    
    #print(event, values)
    while True:                             # Event Loop
        event, values = window.read()       # type: str, dict
        #print(event)
        if event=="Free money":
            money+=300
            window['pippo'].update(f"Money:{money}")

            #print(money)
        if event in (sg.WIN_CLOSED, '-EXIT-'):         # If the user exits
            break
        if event == 'MissionList' and len(values['MissionList']):
            if "Mission 1" in values['MissionList']:
                if sg.popup_yes_no("You have selected mission 1.\nFrom: Your Sensei\nWe need to check that you are a reasonable guy and not a dumbass.\nReward: 1000.-\nDo you want to choose this mission?",no_titlebar=True)=="Yes":
                    if sg.popup_yes_no("You chose this mission, now answer the question to complete it.\nThis is the question:\nIf you enter a stranger's pc do you know the password?",no_titlebar=True)=="Yes":
                        sg.popup("You lost, it is protected you need a tool to know it",no_titlebar=True)
                        sg.WIN_CLOSED==None
                    else:
                        sg.popup("Few... we were right,you are a trustable person.The money will be transfered in your account.",no_titlebar=True)
                        money+=1000
                        window['pippo'].update(f"Money Counter:{money}")
                        sg.WIN_CLOSED==None

                else:
                    sg.popup("Why are you here then duh.",no_titlebar=True)
                    sg.WIN_CLOSED==None
    window.close()
layout1()