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
from functools import partial
import json

# Base application for the SWAARJA Student Assistant Application
# Authors: Dan Jackson, Alla Alharazi, Eileen Roberson
# Modification of the prototype SA application written by Zach Ankuda

Window.size = (600, 700)
Window.clearcolor = [1, 1, 1, 1]

focus_btn_color = [2, 0, 0, 1]
active_btn_color = [1, 0, 0, 1]
taken_btn_color = [0, 1, 0, 1]


class HomeScreen(Screen):
    """ Initially loaded screen. Used also for static method container
    since this page will always exist.
    """

    """ Static method to create popups for specific critical info.
    It's the responsibility of the calling entity to define the
    content and title, since those will change depending on the
    context in which the popup is being created. make_popup handles
    its own Close Button and calling Popup.open() to show itself.
    """
    @staticmethod
    def make_popup(title, content):
        popup = CustomPopup()
        popup.title = title
        popup.auto_dismiss = True
        content.add_widget(Button(size_hint=(0.5, 0.1),
                                  text="Close",
                                  background_color=active_btn_color,
                                  pos_hint={'right': 0.5,
                                            'center_x': 0.5},
                                  on_press=popup.dismiss)
                           )
        popup.content = content
        popup.open()


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

    """ Save Button handler that stores the currently entered 
    study plan info as a JSON object and file on the local file 
    system.
    """
    def save_handler(self):

        courses_list = dict()
        courses_list['is_grad'] = self.ids.grad_checkbox.state
        courses_taken = dict()

        for x in self.ids.stdypln_box.children:
            courses_list[x.children[1].text] = x.children[0].text
            if x.children[1].background_color == taken_btn_color:
                courses_taken[x.children[1].text] = "yes"
            else:
                courses_taken[x.children[1].text] = "no"
        study_plan = [courses_list, courses_taken]
        try:
            with open('study_plan', 'w') as outfile:
                json.dump(study_plan, outfile)      
        except (IOError, ValueError) as io_ex:
            ex_box = BoxLayout(orientation='vertical',
                               spacing=2, height=500,
                               width=500)
            ex_label = Label(text=str(io_ex),
                             color=(0, 0, 0, 1))
            ex_box.add_widget(ex_label)
            HomeScreen.make_popup('StudyPlan file save error: ',
                                  ex_box)

    """ Load button handler that retrieves the user's previously
    saved study plan from the study_plan JSON object file.
    """
    def load_handler(self):
        try:
            with open('study_plan') as json_data:
                study_plan = json.load(json_data)
                course_list = study_plan[0]
                courses_taken = study_plan[1]
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
                for key, value in courses_taken.items():
                    for x in self.ids.stdypln_box.children:
                        if x.children[1].text == key and value == 'yes':
                            x.children[1].background_color = taken_btn_color
        except (IOError, ValueError) as io_ex:
            ex_box = BoxLayout(orientation='vertical',
                               spacing=2, height=500,
                               width=500)
            ex_label = Label(text=str(io_ex),
                             color=(0, 0, 0, 1))
            ex_box.add_widget(ex_label)
            HomeScreen.make_popup('StudyPlan file load error: ',
                                  ex_box)
            
    def reset_handler(self):
        for x in self.ids.stdypln_box.children:
            x.children[0].text = ''
            x.children[1].background_color = active_btn_color

    def toggle_taken(self,crs_button):
        if crs_button.background_color == active_btn_color:
            crs_button.background_color = taken_btn_color
        else:
            crs_button.background_color = active_btn_color


class CoursesScreen(Screen):
    """Backing class for the main page for searching and viewing
    information on courses.
    """

    """ Basic function state of the courses screen.  
    avail = crs_go_btn on_press handler will search for available
    courses based on the department taken from crs_search_txtIn.
    times = crs_go_btn on_press handler will search for course times
    based on the course ID taken from crs_search_txtIn.
    """
    active_crs_state = 'avail'

    """ Set state to Courses Available function ('avail')
    """
    def set_course_avail_state(self):
        self.ids.avail_btn.background_color = focus_btn_color
        self.ids.times_btn.background_color = active_btn_color
        self.active_crs_state = 'avail'
        
    """ Set state to Course Times function ('times')
    """
    def set_course_times_state(self):
        self.ids.avail_btn.background_color = active_btn_color
        self.ids.times_btn.background_color = focus_btn_color
        self.active_crs_state = 'times'

    """ Clears the display box area.
    """
    def reset_crs_handler(self):
        self.reset_crs_srch_box()
        self.ids.crs_srch_txtin.text = 'ex. SSW555'

    """ Clears the display box area.
    """
    def reset_crs_srch_box(self):
        self.ids.crs_disp_box.clear_widgets()

    """ Constructs the URLRequest object based on the currently 
    selected state of the Courses page and the value in the 
    crs_srch_txtin. 
    """
    def create_async_url(self):

        self.reset_crs_srch_box()                        
        url_string = CoursesScreen.create_url_string(self.active_crs_state,
                                                     self.ids.crs_srch_txtin.text)
        UrlRequest(url=url_string, on_success=partial(
                                            CoursesScreen.populate_disp,
                                            self))

    """ Creates the results widgets and displays them in the 
    crs_disp_box object. 
    """
    @staticmethod
    def populate_disp(self, req, result):

        if len(result) > 0 and req.error is None:
            # Iterates over the results in the req object and
            # creates a set of button and labels for each result.
            # Adds these to the crs_disp_box display area.
            for x in range(0, len(result)):
                res = result[x]
                c_id_btn = Button(
                        text=res["course_id"],
                        background_color=(1.0, 0.0, 0.0, 1.0),
                        size_hint_y=None,
                        size=(80, 50),
                        disabled=res["status"] == 'Closed')
                c_id_btn.bind(on_press=partial(CoursesScreen.create_popup, res["call_number"]))
                c_name_label = Label(text=res["course_name"],
                                     text_size=(200, None),
                                     color=(0, 0, 0, 1),
                                     halign='center')
                c_seats_label = Label(text=str("Day: " + res['day'] + "\n"
                                      + "Time: " + res['time']) + "\n"
                                      + "Status: " + res['status'],
                                      color=(0, 0, 0, 1),
                                      halign='center')
                self.ids.crs_disp_box.add_widget(c_id_btn)
                self.ids.crs_disp_box.add_widget(c_name_label)
                self.ids.crs_disp_box.add_widget(c_seats_label)
        else:
            c_name_label = Label(text='NO RESULTS',
                                 color=(0, 0, 0, 1))
            self.ids.crs_disp_box.add_widget(c_name_label)

    """ Creates and displays a Popup object when a Course ID display
    button is clicked. Uses the Course ID to construct a second 
    UrlRequest object to get course-specific info from the server.
    """
    @staticmethod
    def create_popup(call_number, function_reference):

        """ Creates and displays the actual popup object.
        """
        def open_popup(req, result):
            the_popup = CustomPopup()
            the_popup.title = result[0]['course_id']
            the_popup.auto_dismiss = True

            if req.error is None:
                res = result[0]
                # Section to prevent fault when data is missing
                # from database.
                if res['course_name'] is None:
                    popup_string = "No Course Name In Database" + '\n'
                else:
                    popup_string = 'Course Name: ' + res['course_name'] + '\n'
                if res['course_description'] is None:
                    popup_string += "No Course Description In Database" + '\n'
                else:
                    popup_string += 'Course Description: ' + \
                                    res['course_description'] + '\n'
                if res['semester'] is None:
                    popup_string += "No Course Semester In Database" + '\n'
                else:
                    popup_string += 'Course Semester: ' + res['semester'] + '\n'
                if res['day'] is None:
                    popup_string += "No Course Day In Database" + '\n'
                else:
                    popup_string += 'Course Day: ' + res['day'] + '\n'
                if res['time'] is None:
                    popup_string += "No Course Time In Database" + '\n'
                else:
                    popup_string += 'Course Time: ' + res['time'] + '\n'
                if res['campus'] is None:
                    popup_string += "No Course Campus Type In Database" + '\n'
                else:
                    popup_string += 'Course Campus Type: ' + res['campus'] + '\n'
                if res['status'] is None:
                    popup_string += "No Course Status/Availability In Database" + '\n'
                else:
                    popup_string += 'Course Status: ' + res['status']

                a = Label(text=popup_string,
                          color=(0, 0, 0, 1),
                          size_hint_y=None,
                          height=the_popup.height,
                          text_size=(580, None),
                          line_height=1.5,
                          valign="top", halign="center")
                the_popup.ids.scroll_popup.add_widget(a)
                the_popup.content = the_popup.ids.box_popup
                the_popup.open()
            else:
                HomeScreen.make_popup('Error',
                                      Label('There was an error '
                                            'contacting the database.\n'
                                            'Please try again later.'))

        url_string = ('http://34.207.67.202:8080/'
                      'course_description/'
                      'get_course_description/'
                      '?search_call_number=' + str(call_number))
        UrlRequest(url=url_string, on_success=open_popup)

    """ Returns a url string from a state descriptor and
    a search id
    """
    @staticmethod
    def create_url_string(state, srch_id):
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
        return server+rpc+search


class ProfessorsScreen(Screen):
    pass


class BuildingsScreen(Screen):
    pass


class SAMainApp(App):
    def build(self):
        self.title = 'Student Assistant Application'
        pass


if __name__ == '__main__':
    SAMainApp().run()
