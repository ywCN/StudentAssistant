from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
#from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.widget import Widget

# Base application for the SWAARJA Student Assistant Application
# Authors: Dan Jackson, Alla Alharazi, Eileen Roberson
# Modification of the prototype SA application written by Zach Ankuda

Window.size = (600, 700)
Window.clearcolor = (1, 1, 1, 1)

focus_btn_color = (2, 0 ,0, 1)
active_btn_color = (1, 0, 0, 1)

class HomeScreen(Screen):
    pass

class CustomPopup(Popup):
    pass

class StudyPlanScreen(Screen):
    pass

#  Backing class for the main page for searching and viewing
# information on courses.
class CoursesScreen(Screen):
	#Basic feature state of the courses screen.  Available states:
	# 'avail', 'desc', 'times'
	#avail = crs_go_btn on_press handler will search for available
	# courses based on the department taken from crs_search_txtIn.
	#desc = crs_go_btn on_press handler will search for a course
	# description based on the course ID taken from crs_search_txtIn.
	#times = crs_go_btn on_press handler will search for course times
	# based on the course ID taken from crs_search_txtIn.
    active_crs_state = 'avail'

    def set_course_avail_state(self):
        self.ids.crs_srch_lbl.text = 'Department:'
        self.ids.crs_srch_txtin.text = 'ex. SSW'
        self.ids.avail_btn.background_color = focus_btn_color
        self.ids.times_btn.background_color = active_btn_color
        self.ids.desc_btn.background_color = active_btn_color
        self.active_crs_state = 'avail'

    def set_course_times_state(self):
        self.ids.crs_srch_lbl.text = 'Course ID:'
        self.ids.crs_srch_txtin.text = 'ex. SSW555'		
        self.ids.avail_btn.background_color = active_btn_color
        self.ids.times_btn.background_color = focus_btn_color
        self.ids.desc_btn.background_color = active_btn_color
        self.active_crs_state = 'times'

    def set_course_desc_state(self):
        self.ids.crs_srch_lbl.text = 'Course ID:'
        self.ids.crs_srch_txtin.text = 'ex. SSW555'
        self.ids.avail_btn.background_color = active_btn_color
        self.ids.times_btn.background_color = active_btn_color
        self.ids.desc_btn.background_color = focus_btn_color
        self.active_crs_state = 'desc'

    def get_course_id_text(self):
        #course_id TextInput text validation function
        #@TODO Add additional text validation after
        # coordinating with server team
        def validate_course_id_text():
            return(len(self.ids.crs_srch_txtin.text) == 6)

    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()
	
    def go_btn_handler(self):
        #@TODO: why doesn't this call work if the active_crs_state
        # hasn't changed between calls to go_btn_handler?
        self.reset_crs_srch_box()
		
        #Switch that populates the crs_disp_box differently
        # based on the CourseScreen active_crs_state
        if self.active_crs_state == 'avail':
            req = self.create_url_request()

            #iterates over the results in the req object and
            # creates a set of button and labels for each result.
            # Adds these to the crs_disp_box display area.
            for x in range(0, 5):
                res = req.result[x]
                c_id_btn = Button(on_press = CoursesScreen.open_popup,
                            text=res["course_id"],
                            background_color =(1.0, 0.0, 0.0, 1.0),
				 size_hint_y=(None), size=(100, 50))
                c_name_label = Label(text=res["course_name"],
                            color=(0, 0 ,0 ,1))
                c_seats_label = Label(text=str(res['status']),
                            color= (0, 0, 0, 1))         
                self.ids.crs_disp_box.add_widget(c_id_btn)
                self.ids.crs_disp_box.add_widget(c_name_label)
                self.ids.crs_disp_box.add_widget(c_seats_label)
        elif self.active_crs_state == 'times':
            req = self.create_url_request()

        elif self.active_crs_state == 'desc':
            req = self.create_url_request()

    #Creates and reutrns the URLRequest based on CourseScreens 
    # active state 	
    def create_url_request(self):
        #set header type
        headers = {'Accept' : 'application/json; indent=4'}

        #initialize url string for the URLRequest
        server = 'http://34.207.67.202:8080/'
        rpc = ''
        search = ''

        #set the url string for the URLRequest
        if self.active_crs_state == 'avail':
            rpc = 'available/'
            search = ''
        elif self.active_crs_state == 'desc':
            rpc = ('course_description/'
                'get_course_description/?search_id=')
            search = 'SSW640'
        elif self.active_crs_state == 'times':
            rpc = 'times/'
            search = ''

        #Construct the URLRequest object
        req = UrlRequest(
            server+rpc, 
        req_headers=headers)
        req.wait()

        #return the URLRequest object	
        return req

    #helper function to clear the display space
    def reset_crs_srch_box(self):
        self.ids.crs_disp_box.clear_widgets()
        self.ids.crs_srch_txtin.text = ''

class ProfessorsScreen(Screen):
    pass

class BuildingsScreen(Screen):
    pass

#Start of Dan's classes.
class TeachersScreen(Screen):
    pass

class samainapp(App):
    def build(self):
        self.title = 'Student Assistant Application'
        pass

if __name__=='__main__':
    samainapp().run()
