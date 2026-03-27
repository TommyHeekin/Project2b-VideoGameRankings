#implement interactable interface that sends instructions to each data structure with certain parameters (game genre, price, popularity, etc.)

#credits to customtkinter for ui design
#credits to customtkinter for ui design, specifically https://customtkinter.tomschimansky.com/documentation/widgets for specific design 
#further credit to https://github.com/avalon60/ctk_theme_builder for tutorials on color and other elements

import customtkinter

#Radiobutton, so only 1 option may be chosen
#Class based implementations to easily scale number of options without hardcoding
class MyRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values, grid):
        #initialize values
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=0)
        self.values = values
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        #set location of buttons
        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i//grid, column=i%grid, padx=40, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    #return selected option
    def get(self):
        return self.variable.get()

    #change selected option
    def set(self, value):
        self.variable.set(value)

#exact same implementation but checkboxes instead for genre
class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values, grid):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=0)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            #checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            checkbox.grid(row=i//grid, column=i%grid, padx=40, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Create Window
        self.title("Game Recommendation")
        self.geometry("900x780")

        #Ensure widgets can expand horizontally 
        self.grid_columnconfigure((0, 1,2,3,4,5), weight=1)
        self.grid_rowconfigure(0, weight=0)

        #genre box creation
        values = ['Action', 'Adult', 'Adventure', 'Baseball', 'Battle', 'Board', 'Card', 'Casino', 'Compilation', 'Editor', 'Educational',
                   'Fighting', 'First-Person', 'Flight', 'Hunting', 'Music', 'None', 'Other', 'Party', 'Pinball', 'Platformer', 'Productivity',
                     'Puzzle', 'RPG', 'Racing', 'Shooter', 'Simulation', 'Sports', 'Strategy', 'Trivia', 'Virtual Pet', 'Word Games', 'Wrestling']
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Genre", values=values, grid=4)
        self.scrollable_checkbox_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="news", columnspan=5)

        #search button
        self.button = customtkinter.CTkButton(self, text="Search", command=self.button_callback, height = 40)
        self.button.grid(row=6, column=0, padx=10, pady=10, sticky="news", columnspan=5)
        self.button.grid_columnconfigure(0, weight=1)

       # rating slider
        self.slider = customtkinter.CTkSlider(self, from_=0, to=100, command=self.slider_event)
        self.slider.grid(row=2, column=0, padx=10, pady=10, sticky="ews", columnspan=5)
        self.slider.grid_columnconfigure(0, weight=1)
        
        #allows user to see chosen rating
        self.textbox1 = customtkinter.CTkTextbox(self, font=("Arial", 18), height=5)
        self.textbox1.insert("0.0", "Minumum Rating:")  # insert at line 0 character 0
        self.text = self.textbox1.get("0.0", "end")  # get text from line 0 character 0 till the end
        self.textbox1.configure(state="disabled")  # configure textbox to be read-only
        self.textbox1.grid(row=1, column=1, padx=0, pady=10, sticky="news", columnspan=1)
        self.textbox1.grid_columnconfigure(0, weight=1)

        self.updateRating(50.0)


        #disable slider if rating is disabled
        def switch_event():
            switched = self.switch.get()
            if switched == "on":
            
                self.slider.configure(state="normal")
                self.updateRating(50.0)
                self.slider.set(50.0)
                
            else:
                self.slider.set(0.0)
                self.slider.configure(state="disabled")
                self.textbox1.configure(state="normal")
                self.text = self.textbox1.delete("0.0", "end")  # get text from line 0 character 0 till the end
                self.textbox1.insert("0.0", "Disabled")  # insert at line 0 character 0
                self.textbox1.configure(state="disabled")


        #enable/disable rating switch
        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(self, text="Enable Rating", command=switch_event,
                                        variable=self.switch_var, onvalue="on", offvalue="off", font=("Arial", 18))
        self.switch.grid(row=1, column=0, padx=(50,0), pady=(10, 10), sticky="news", columnspan=1)

        
        #console radiobutton
        values = [ 'Android', 'Arcade', 'Atari 2600', 'Atari 5200',
            'Commodore 64/128', 'DVD / HD Video Game', 'Dreamcast', 'Dreamcast VMU', 'Game Boy', 'Game Boy Advance', 'Game Boy Color',
              'Game.Com', 'GameCube', 'Genesis', 'Linux', 'Lynx', 'Macintosh', 'Master System', 'N-Gage', 'NES', 'NeoGeo', 'NeoGeo Pocket Color',
                'Nintendo 3DS', 'Nintendo 64', 'Nintendo 64DD', 'Nintendo DS', 'Nintendo DSi', 'PC', 'PlayStation', 'PlayStation 2', 'PlayStation 3',
                  'PlayStation 4', 'PlayStation Portable', 'PlayStation Vita', 'Pocket PC', 'Saturn', 'Sega 32X', 'Sega CD', 'Super NES', 'TurboGrafx-16',
                    'TurboGrafx-CD', 'Vectrex', 'Web Games', 'Wii', 'Wii U', 'Windows Phone', 'Windows Surface', 'Wireless', 'WonderSwan', 'WonderSwan Color',
                      'Xbox', 'Xbox 360', 'Xbox One', 'iPad', 'iPhone', 'iPod']

        self.scrollable_checkbox_frame1 = MyRadiobuttonFrame(self, title="Device", values=values, grid=3)
        self.scrollable_checkbox_frame1.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="news", columnspan=5)


        #main title
        self.textbox = customtkinter.CTkTextbox(self, font=("Arial", 50), height= 50)

        self.textbox.insert("0.0", "Game Recommender") 
        self.text = self.textbox.get("0.0", "end") 
        self.textbox.configure(state="disabled")  
        self.textbox.grid(row=0, column=0, padx=10, pady=15, sticky="news", columnspan=5)
        self.textbox.grid_columnconfigure(0, weight=1)


        customtkinter.deactivate_automatic_dpi_awareness()

    #updating rating textbox
    def updateRating(self, value):
        self.textbox1.configure(state="normal")
        self.text = self.textbox1.delete("0.0", "end")  
        self.textbox1.insert("0.0", "Minumum Rating: " + str(round(value/10, 1))) #ensure rating is only 1-10 with 1 decimal place
        self.textbox1.configure(state="disabled")

    #update rating textbox when slider is moved
    def slider_event(self, value):
        self.updateRating(value)

    #return values for search
    def button_callback(self):
        args = [self.scrollable_checkbox_frame.get(), round(self.slider.get()/10, 1), self.scrollable_checkbox_frame1.get()]
        print("Genres:", args[0])
        print("Min Rating:", args[1])
        print("Console:", args[2])
        self.slider_event(self.slider.get())
customtkinter.set_appearance_mode("dark")
app = App()
app.mainloop()