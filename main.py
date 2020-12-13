from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
import random

# Load the design.kv file into this script
Builder.load_file('design.kv')

class LoginScreen(Screen):
    """Login Screen template class that inherits from Screen"""
    # current third highest class
    
    """
    Signup a user from the login screen
    """
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    """
    Login a user
    """
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username/password"


class SignUpScreen(Screen):
    """Sign Up screen template class that inherits from Screen"""
    
    """
    Add a user to the database
    """
    def add_user(self, uname, pword):
        # Open and read json file
        with open("users.json") as file:
            users = json.load(file)

        # Extract new username and password input from SignUpScreen
        users[uname] = {'username': uname, 'password': pword,
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        
        # Write new users dictionary into the json file
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    """Sign Up Screen class to be called when sign up is successful"""
    
    # Switch to the login_screen after creating a new users
    def login_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    """Login Screen Success class to navigate to the home page"""

    # Switch a user back to the login page
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    # Retrieve a quote from the appropriate 'feelings' file
    def get_quote(self, feel):
        # Convert input 'feel' to lowercase
        feel = feel.lower()

        # Store all available quote txts
        available_feelings = glob.glob("quotes/*txt")

        # Save the filename of each txt
        available_feelings = [Path(filename).stem for filename in 
                                available_feelings]

        # Check to see if the input feeling is within the txts
        if feel in available_feelings:
            # Open the relevant txt file, specifying utf-8 encoding
            with open(f"quotes/{feel}.txt", encoding='utf-8') as file:
                quotes = file.readlines()
                 # Select a random quote using the .choice() method
                self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling."

        #print(available_feelings)


class RootWidget(ScreenManager):
    """Root Widget template class that inherits from ScreenManager"""
    # second highest class
    pass

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    """Image Button class will combined the three given Parent objects"""
    # Order of parents is important ^
    pass

class MainApp(App):
    """MainApp class that inherits from App"""
    # highest class in hierarchy
    
    """
    Returns RootWidget object
    """
    def build(self):
        return RootWidget()

if __name__=='__main__':
    MainApp().run()