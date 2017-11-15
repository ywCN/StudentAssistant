from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import json

# Base application for the SWAARJA Student Assistant Application
# Authors: Dan Jackson, Alla Alharazi, Eileen Roberson
# Modification of the prototype SA application written by Zach Ankuda

Window.size = (600, 700)
Window.clearcolor = (1, 1, 1, 1)

focus_btn_color = (2, 0, 0, 1)
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
    """Backing class for the page for recording, saving, editing, and
    retrieving a degree course plan.
    """

    '''Save Button handler that stores the currently entered 
    study plan info as a JSON object and file on the local file 
    system.
    '''
    def save_handler(self):        
        study_plan = dict()
        study_plan['is_grad'] = self.ids.grad_checkbox.state
        for x in self.ids.stdypln_box.children:
            study_plan[x.children[1].text] = x.children[0].text
        try:
            with open('study_plan', 'w') as outfile:
                json.dump(study_plan, outfile)      
        except Exception as ex:
            print('Study plan file write error: ', ex)
            
    '''Load button handler that retrieves the user's previously
    saved study plan from the study_plan JSON object file.
    '''
    def load_handler(self):
        try:
            with open('study_plan') as json_data:
                course_list = json.load(json_data)

                if course_list['is_grad'] == 'down':
                    self.ids.grad_checkbox.state = 'down'
                    self.ids.undergrad_checkbox.state = 'normal'
                else:
                    self.ids.grad_checkbox.state = 'normal'
                    self.ids.undergrad_checkbox.state = 'down'           
                for key, value in course_list.items():
                    for x in self.ids.stdypln_box.children:
                        if x.children[1].text == key:
                            x.children[0].text = value
        except Exception as ex: 
            print('Study plan file load error: ', ex)
            
    def reset_handler(self):
        for x in self.ids.stdypln_box.children:
            x.children[0].text = ''


class CoursesScreen(Screen):
    """Backing class for the main page for searching and viewing
    information on courses.
    """

    '''Basic function state of the courses screen.  
    avail = crs_go_btn on_press handler will search for available
    courses based on the department taken from crs_search_txtIn.
    times = crs_go_btn on_press handler will search for course times
    based on the course ID taken from crs_search_txtIn.
    '''
    active_crs_state = 'avail'

    ''' Set state to Courses Available function ('avail')
    '''
    def set_course_avail_state(self):
        self.ids.crs_srch_lbl.text = 'Department:'
        self.ids.crs_srch_txtin.text = 'ex. SSW'
        self.ids.avail_btn.background_color = focus_btn_color
        self.ids.times_btn.background_color = active_btn_color
        self.active_crs_state = 'avail'
        
    ''' Set state to Course Times function ('times')
    '''
    def set_course_times_state(self):
        self.ids.crs_srch_lbl.text = 'Course ID:'
        self.ids.crs_srch_txtin.text = 'ex. SSW555'		
        self.ids.avail_btn.background_color = active_btn_color
        self.ids.times_btn.background_color = focus_btn_color
        self.active_crs_state = 'times'
    
    '''Creates and displays a Popup object when a Course ID display
    button is clicked. Displays the Course ID, Course Name, Course
    Description, Course Time, Course Status.
    '''
    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.title = self.text
        the_popup.auto_dismiss = True                                     

        req = self.parent.parent.parent.parent.parent.create_url_request(
            'desc', self.text)
        res = req.result[0]
        
        layout = BoxLayout(
            orientation = 'vertical', spacing = 2,
            height = 1000, width= 900,
            pos_hint= {'center_x': 0.2, 'center_y': 0.5})
        #work on position pos_hint= {'right': 0.2, 'center_x': 1}
        a = Label (
            text = 'Course Name: ' + res['course_name'],
            color = (0,0,0,1))   
        C = Label ( text = ' ')
        b = Label (
            text = 'Course Description: ' + res['course_description'],
            color = (0,0,0,1),text_size=(400,None))
        CC = Label ( text = '')
        c = Label (
            text = 'Course Time: ' + res['time'],
            color = (0,0,0,1))            
        d = Label (
            text = 'Course Status: '+ res['status'],
            color = (0,0,0,1))  
        CCC = Label ( text = ' ')

        f = Button (
            size_hint= (0.5,0.1),
            pos_hint= {'right': 0.5, 'center_x': 0.5},
            text = "close",
            background_color =  (1.0, 0.0, 0.0, 1.0),
            on_press = the_popup.dismiss)
        
        layout.add_widget(a)
        layout.add_widget(C)
        layout.add_widget(b)
        layout.add_widget(CC)
        layout.add_widget(c)        
        layout.add_widget(d)
        layout.add_widget(CCC)
        layout.add_widget(f)
        the_popup.content = layout
        
        the_popup.open()

    ''' Initiates a create_url_request call to the server based on the
    currently selected state of the Courses page and the value in the 
    crs_srch_txtin. Displays the results in the crs_disp_box.
    '''
    def go_btn_handler(self):
        self.reset_crs_srch_box()
        
        # Switch that populates the crs_disp_box differently
        # based on the CourseScreen active_crs_state
        req = self.create_url_request(self.active_crs_state,
                                      self.ids.crs_srch_txtin.text)
        if len(req.result) > 0:
            if self.active_crs_state == 'avail':                
                # Iterates over the results in the req object and
                # creates a set of button and labels for each result.
                # Adds these to the crs_disp_box display area.
                for x in range(0, len(req.result)):
                    res = req.result[x]
                    c_id_btn = Button(
                            on_press=CoursesScreen.open_popup,
                            text=res["course_id"],
                            background_color=(1.0, 0.0, 0.0, 1.0),
                            size_hint_y=None, size=(80, 50))
                    c_name_label = Label(text=res["course_name"],
                                         color=(0, 0, 0, 1))
                    c_seats_label = Label(text=str(res['status']), 
                                          color=(0, 0, 0, 1))
                    self.ids.crs_disp_box.add_widget(c_id_btn)
                    self.ids.crs_disp_box.add_widget(c_name_label)
                    self.ids.crs_disp_box.add_widget(c_seats_label)
            elif self.active_crs_state == 'times':
                # Iterates over the results in the req object and
                # creates a set of button and labels for each result.
                # Adds these to the crs_disp_box display area.
                for x in range(0, len(req.result)):
                    res = req.result[x]
                    c_id_btn = Button(
                            on_press=CoursesScreen.open_popup,
                            text=res["course_id"],
                            background_color=(1.0, 0.0, 0.0, 1.0),
                            size_hint_y=None, size=(80, 50))
                    c_name_label = Label(text=res["course_name"],
                                         color=(0, 0, 0, 1))
                    c_seats_label = Label(text=str(res['time']), 
                                          color=(0, 0, 0, 1))
                    self.ids.crs_disp_box.add_widget(c_id_btn)
                    self.ids.crs_disp_box.add_widget(c_name_label)
                    self.ids.crs_disp_box.add_widget(c_seats_label)
        else:
            c_name_label = Label(text='NO RESULTS',
                                 color=(0, 0, 0, 1))
            self.ids.crs_disp_box.add_widget(c_name_label)
            
    '''Creates and returns the URLRequest based on CourseScreens 
    active state'''
    def create_url_request(self, state, srch_id):
        # set header type
        headers = {'Accept': 'application/json; indent=4'}

        # initialize url string for the URLRequest
        server = 'http://34.207.67.202:8080/'
        rpc = ''
        search = ''

        # set the url string for the URLRequest
        if state == 'avail':
            rpc = ('available/'
                   'get_available_course/')
            if len(srch_id) > 0 and srch_id != 'ex. SSW':
                rpc = rpc + '?search_dept_id='
                search = srch_id
        elif state == 'desc':
            rpc = ('course_description/'
                   'get_course_description/')
            if len(srch_id) > 0 and srch_id != 'ex. SSW555':
                rpc = rpc + '?search_id='
                search = srch_id
        elif state == 'times':
            rpc = ('course_description/'
                   'get_course_description/')
            if len(srch_id) > 0 and srch_id != 'ex. SSW555':
                rpc = rpc + '?search_id='
                search = srch_id

        # Construct the URLRequest object
        req = UrlRequest(
            server+rpc+search, 
            req_headers=headers)
        req.wait()
        # return the URLRequest object
        return req

    '''Clears the display box area.
    '''
    def reset_crs_srch_box(self):
        self.ids.crs_disp_box.clear_widgets()


class ProfessorsScreen(Screen):
    pass


class BuildingsScreen(Screen):
    pass


class samainapp(App):
    def build(self):
        self.title = 'Student Assistant Application'
        pass


if __name__ == '__main__':
    samainapp().run()
