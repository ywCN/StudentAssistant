# Add Authors name:

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.widget import Widget
 
Window.size = (600, 900)
Window.clearcolor = (1, 1, 1, 1)


focus_btn_color = (2,0,0,1)
active_btn_color = (1,0,0,1)
active_crs_state = 'avail'
 
 
class HomeScreen(Screen):
	pass

class StudyPlanScreen(Screen):
	pass
class CoursesScreen(Screen):
	
	def set_course_avail_state(self):	
		self.ids.crs_srch_lbl.text = 'Department:'
		self.ids.crs_srch_txtin.text = 'ex. SSW'
		self.ids.avail_btn.background_color = focus_btn_color
		self.ids.times_btn.background_color = active_btn_color
		self.ids.desc_btn.background_color = active_btn_color
		
	def set_course_times_state(self):
		self.ids.crs_srch_lbl.text = 'Course ID:'
		self.ids.crs_srch_txtin.text = 'ex. SSW555'		
		self.ids.avail_btn.background_color = active_btn_color
		self.ids.times_btn.background_color = focus_btn_color
		self.ids.desc_btn.background_color = active_btn_color
		
	def set_course_desc_state(self):
		self.ids.crs_srch_lbl.text = 'Course ID:'
		self.ids.crs_srch_txtin.text = 'ex. SSW555'	
		self.ids.avail_btn.background_color = active_btn_color
		self.ids.times_btn.background_color = active_btn_color
		self.ids.desc_btn.background_color = focus_btn_color

	def get_course_id_text(self):	
		#course_id TextInput text validation function
		#@TODO Add additional text validation after
		# coordinating with server team
		def validate_course_id_text():
			return(len(self.ids.crs_srch_txtin.text) == 6)		
		print(validate_course_id_text())
		
	def go_btn_handler(self):
		if active_crs_state == 'avail':
		
			self.ids.crs_disp_box.clear_widgets()	
			#URL request section
			headers = {'Accept' : 'application/json; indent=4'}		
			req = UrlRequest(
				'http://34.207.67.202:8080/available/', 
				req_headers=headers)
			req.wait()		
			print(*req.result, sep='/n')	
			for x in range(0, 5):
				res = req.result[x]
				c_id_btn = Button(
							text=res["course_id"], background_color =(1.0, 0.0, 0.0, 1.0))			
				c_name_label = Label(text=res["course_name"],color=(0,0,0,1))
				c_seats_label = Label(text=str(res['status']),color= (0,0,0,1))
                
				self.ids.crs_disp_box.add_widget(c_id_btn)
				self.ids.crs_disp_box.add_widget(c_name_label)
				self.ids.crs_disp_box.add_widget(c_seats_label)	
			self.ids.crs_disp_box.add_widget(Widget())	
			
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

class CoursesAvailScreen(Screen):
		
	def get_courses_available(self):
		#clear widgets from display area
		self.ids.courses_avail_section.clear_widgets()	

		#URL request section
		#@TODO update to remove hard-coded indexing once server call is available
		headers = {'Accept' : 'application/json; indent=4'}		
		req = UrlRequest('http://127.0.0.1:8000/courses_available/', req_headers=headers)
		req.wait()
		res = req.result[0]
		
		#debug print statement
		print(res)
					
		#This section currently only displays the following default widgets upon successful resolution  
		#of the UrlRequest /courses_available/
		#
		#@TODO dynamically create and display widgets based on the contents of req.result
		#@TODO update look and feel of this tab to conform to the iOS prototype visuals
		#NOTE that the req.result array currently is hard coded to index 0, this will need to
		#to be considered once a valid return is gotten from the server
		layout_inner1 = BoxLayout(orientation='horizontal')
		layout_inner1.add_widget(Label(text = "Course ID 1"))
		layout_inner1.add_widget(Label(text = "Course Name"))
		layout_inner1.add_widget(Label(text = "Course Time"))
		
		layout_inner2 = BoxLayout(orientation='horizontal')
		layout_inner2.add_widget(Label(text = "Course ID 2"))
		layout_inner2.add_widget(Label(text = "Course Name"))
		layout_inner2.add_widget(Label(text = "Course Time"))
		
		layout_inner3 = BoxLayout(orientation='horizontal')
		layout_inner3.add_widget(Label(text = "Course ID 3"))
		layout_inner3.add_widget(Label(text = "Course Name"))
		layout_inner3.add_widget(Label(text = "Course Time"))
				
		layout_outer = BoxLayout(orientation='vertical')
		layout_outer.add_widget(layout_inner1)
		layout_outer.add_widget(layout_inner2)
		layout_outer.add_widget(layout_inner3)
			
		self.ids.courses_avail_section.clear_widgets()
		self.ids.courses_avail_section.add_widget(layout_outer)
		
	def clear_courses_available(self):
		self.ids.courses_avail_section.clear_widgets()	
        
class CourseDescriptionScreen(Screen):
	
	def get_course_description(self):
		headers = {'Accept': 'application/json; indent=4'}
		#This is how you grab the text to perform the search and retrievel
	 	#searched = self.ids.course_id.text
		req = UrlRequest('http://127.0.0.1:8000/course_description/', req_headers=headers)
		req.wait()
		res = req.result[0]
		#print req.result
		layout = BoxLayout(orientation='vertical')
		course_id = res['course_id']
		course_name = res['course_name']
		course_description = res['course_description']
		id_label = Label(text=course_id, halign='left', valign='middle')
		name_label = Label(text=course_name)
		description_label = Label(text=course_description, size_hint=(1,None))
		description_label.bind(
			width=lambda*x:description_label.setter('text_size')(description_label,(description_label.width,None)),
			texture_size=lambda*x:description_label.setter('height')(description_label,description_label.texture_size[1]))
		layout.add_widget(id_label)
		layout.add_widget(name_label)
		layout.add_widget(description_label)
		self.ids.course_description_section.clear_widgets()
		self.ids.course_description_section.add_widget(layout)
class CourseTimeScreen(Screen):
		
	def get_course_times(self):
		#clear widgets from display area
		self.ids.course_time_section.clear_widgets()	

		#URL request section
		#@TODO update to remove hard-coded indexing once server call is available
		headers = {'Accept' : 'application/json; indent=4'}		
		req = UrlRequest('http://127.0.0.1:8000/courses_available/', req_headers=headers)
		req.wait()
		res = req.result[0]
		
		#debug print statement
		print(res)
					
		#This section currently only displays the following default widgets upon successful resolution  
		#of the UrlRequest /courses_available/
		#
		#@TODO dynamically create and display widgets based on the contents of req.result
		#@TODO update look and feel of this tab to conform to the iOS prototype visuals
		#NOTE that the req.result array currently is hard coded to index 0, this will need to
		#to be considered once a valid return is gotten from the server				
		headers = {'Accept' : 'application/json; indent=4'}
		self.ids.course_time_section.clear_widgets()

		layout_inner1 = BoxLayout(orientation='horizontal')
		layout_inner1.add_widget(Label(text = "Course ID"))
		layout_inner1.add_widget(Label(text = "Course Name"))
		layout_inner1.add_widget(Label(text = "Course Time"))
		
		layout_inner2 = BoxLayout(orientation='horizontal')
		layout_inner2.add_widget(Label(text = "Course ID"))
		layout_inner2.add_widget(Label(text = "Course Name"))
		layout_inner2.add_widget(Label(text = "Course Time"))
		
		layout_inner3 = BoxLayout(orientation='horizontal')
		layout_inner3.add_widget(Label(text = "Course ID"))
		layout_inner3.add_widget(Label(text = "Course Name"))
		layout_inner3.add_widget(Label(text = "Course Time"))
		
		
		layout_outer = BoxLayout(orientation='vertical')
		layout_outer.add_widget(layout_inner1)
		layout_outer.add_widget(layout_inner2)
		layout_outer.add_widget(layout_inner3)
		
		self.ids.course_time_section.clear_widgets()
		self.ids.course_time_section.add_widget(layout_outer)
		
	def clear_course_times(self):
		self.ids.course_time_section.clear_widgets()
		
#Description: Dan's sandbox to hook up and test out new server APIs. Will evolve into
# a fully functioning tab eventually, most likely the Get Course Type tab.
#
#@TODO: update for course times once server call is available. Currently this class is 
#a simple copy of the CoursesAvailScreen class as a stub
class DanSandboxScreen(Screen):
		
	def get_courses_available(self):
		#clear widgets from display area
		self.ids.courses_avail_section.clear_widgets()	

		#URL request section
		headers = {'Accept' : 'application/json; indent=4'}		
		req = UrlRequest('http://127.0.0.1:8000/courses_available/', req_headers=headers)
		req.wait()
		res = req.result[0]
		
		print(req.result)
					
		#Add widgets for label display
		#This section currently only displays the following default widgets upon successful resolution  
		#of the UrlRequest /courses_available/
		#
		#@TODO dynamically create and display widgets based on the contents of req.result
		#@TODO alter req.result to size dynamically
		#@TODO update look and feel of this tab to conform to the iOS prototype visuals
		layout_inner1 = BoxLayout(orientation='horizontal')
		layout_inner1.add_widget(Label(text = "Course ID 1"))
		layout_inner1.add_widget(Label(text = "Course Name"))
		layout_inner1.add_widget(Label(text = "Course Time"))
		
		layout_inner2 = BoxLayout(orientation='horizontal')
		layout_inner2.add_widget(Label(text = "Course ID 2"))
		layout_inner2.add_widget(Label(text = "Course Name"))
		layout_inner2.add_widget(Label(text = "Course Time"))
		
		layout_inner3 = BoxLayout(orientation='horizontal')
		layout_inner3.add_widget(Label(text = "Course ID 3"))
		layout_inner3.add_widget(Label(text = "Course Name"))
		layout_inner3.add_widget(Label(text = "Course Time"))
				
		layout_outer = BoxLayout(orientation='vertical')
		layout_outer.add_widget(layout_inner1)
		layout_outer.add_widget(layout_inner2)
		layout_outer.add_widget(layout_inner3)
			
		self.ids.courses_avail_section.clear_widgets()
		self.ids.courses_avail_section.add_widget(layout_outer)
		
	def clear_courses_available(self):
		self.ids.courses_avail_section.clear_widgets()		
#End of Dan's classes. 

class samainapp(App):
    def build(self):
        self.title = 'Student Assistant Application'
        pass

if __name__=='__main__':
	samainapp().run()