from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

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

class MyTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # limit to 6 chars
        substring = substring[:6 - len(self.text)]
        return super(MyTextInput, self).insert_text(
            substring, from_undo=from_undo)

class StudyPlanScreen(Screen):
    pass

#Backing class for the main page for searching and viewing
# information on courses.
class CoursesScreen(Screen):
    '''Basic feature state of the courses screen.  Available states:
    avail, desc, times
    avail = crs_go_btn on_press handler will search for available
    courses based on the department taken from crs_search_txtIn.
    desc = crs_go_btn on_press handler will search for a course
    description based on the course ID taken from crs_search_txtIn.
    times = crs_go_btn on_press handler will search for course times
    based on the course ID taken from crs_search_txtIn.'''

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
        the_popup.title = self.text
        the_popup.auto_dismiss = True

        req = self.parent.parent.parent.parent.create_url_request(
            'desc', self.text)
        res = req.result[0]
        the_popup.content = Label(text=res['course_description'],
            color=(0, 0 ,0 ,1))
        the_popup.open()
	
    def go_btn_handler(self):
        #@TODO: why doesn't this call work if the active_crs_state
        # hasn't changed between calls to go_btn_handler?
        self.reset_crs_srch_box()
        display_limit = 7
        
        '''Switch that populates the crs_disp_box differently
        based on the CourseScreen active_crs_state'''
        if self.active_crs_state == 'avail':
            req = self.create_url_request(self.active_crs_state,
                self.ids.crs_srch_txtin.text)
            if len(req.result)>0:
                '''Iterates over the results in the req object and
                creates a set of button and labels for each result.
                Adds these to the crs_disp_box display area.'''
                for x in range(0,len(req.result)):
                    res = req.result[x]
                    c_id_btn = Button(
                            on_press = CoursesScreen.open_popup,
                            text=res["course_id"],
                            background_color =(1.0, 0.0, 0.0, 1.0),
                            size_hint_y=(None), size=(80, 50))
                    c_name_label = Label(text=res["course_name"],
                            color=(0, 0 ,0 ,1))
                    c_seats_label = Label(text=str(res['status']), 
                            color= (0, 0, 0, 1))         
                    self.ids.crs_disp_box.add_widget(c_id_btn)
                    self.ids.crs_disp_box.add_widget(c_name_label)
                    self.ids.crs_disp_box.add_widget(c_seats_label)
                    '''Workaround to autoscrolling in cases when there
                    are too many results to display on screen.'''
                    if x == display_limit:
                        c_limit_btn = Button(
                            text='TOO MANY COURSES',
                            background_color =(1.0, 0.0, 0.0, 1.0),
                            size_hint_y=(None), size=(100, 50))
                        self.ids.crs_disp_box.add_widget(c_limit_btn)
                        break
            else:
                c_name_label = Label(text='NO RESULTS',
                    color=(0, 0 ,0 ,1))
                self.ids.crs_disp_box.add_widget(c_name_label)

        elif self.active_crs_state == 'times':
            req = self.create_url_request(self.active_crs_state,'')

        elif self.active_crs_state == 'desc':
            req = self.create_url_request(self.active_crs_state,'')

    '''Creates and reutrns the URLRequest based on CourseScreens 
    active state'''
    def create_url_request(self,state,srch_id):
        #set header type
        headers = {'Accept' : 'application/json; indent=4'}

        #initialize url string for the URLRequest
        server = 'http://34.207.67.202:8080/'
        rpc = ''
        search = ''

        #set the url string for the URLRequest
        if state == 'avail':
            rpc = ('available/'
			    'get_available_course/')
        elif state == 'desc':
            rpc = ('course_description/'
                'get_course_description/')
        elif state == 'times':
            rpc = 'times/'
        
        if len(srch_id)>0 and srch_id != 'ex. SSW':
            rpc = rpc + '?search_dept_id='
            search = srch_id
			
			
        #Construct the URLRequest object
        req = UrlRequest(
            server+rpc+search, 
        req_headers=headers)
        req.wait()
        print(server+rpc+search)
        #return the URLRequest object	
        return req

    #helper function to clear the display space
    def reset_crs_srch_box(self):
        self.ids.crs_disp_box.clear_widgets()
        #self.ids.crs_srch_txtin.text = ''

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
