from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest


class HomeScreen(Screen):
	pass

class BuildingsScreen(Screen):
	pass

class TeachersScreen(Screen):
	pass

class CourseDescriptionScreen(Screen):
	
	def get_course_description(self):
		headers = {'Accept': 'application/json; indent=4'}
		#This is how you grab the text to perform the search and retrievel
	 	#searched = self.ids.course_id.text
		req = UrlRequest('http://127.0.0.1:8000/course_description/', req_headers=headers)
		req.wait()
		res = req.result[0]
		print req.result
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

class SampleMenuApp(App):
	pass

if __name__=='__main__':
	SampleMenuApp().run()
