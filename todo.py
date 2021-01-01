#!/usr/bin/env python

from todolist import *
import os
import sys


json_folder = os.path.expanduser("~") + "/.todopy/"


class Todo:
	

	def run(self):
		
		try:
			func = getattr(self, sys.argv[1])
	
		except AttributeError:
			print ("The command", sys.argv[1], "doesn't exist")
	
		except IndexError:
			self.help()
		else:
			if callable(func):
				try:
					func()
				except IndexError:
					print ("Missing argument for command '" + sys.argv[1] + "' check help")
				except NoSuchListError:
					print ("That list does not exist. Please try another list," \
						+ " or create the list using create <list>")

	def install(self):
		
		try:
			os.mkdir(json_folder)
		except OSError as e:

			if e.errno == 17:
			
				pass
			else:
			
				raise e

		self.create("todo", False)

		print ("Simple Python Todo Installed")

	def create(self, name=None, print_output=True):
		
		if name is None:
			list_name = sys.argv[2]
		else:
			list_name = name

		try:
			json_file = open(self.getListFilename(list_name), "r")
			json.loads(json_file.read())
			if print_output:
				print (list_name, "already exists.")
		except IOError as e:
			if e.errno == 2:
				json_file = open(self.getListFilename(list_name), "w")
				json_file.write("[]")
				if print_output:
					print ("Created:", list_name)


	def delete(self):
		

		list_name = sys.argv[2]
		os.remove(self.getListFilename(list_name))

		print (list_name, "removed")

	def add(self):
		
		text = ' '.join(sys.argv[2:])
		self.addto("todo", text)

	def addto(self, list_name="", text=""):
		
		if list_name == "":
			list_name = sys.argv[2]
			text = ' '.join(sys.argv[3:])

		todo_list = TodoList(self.getListFilename(list_name))
		todo_list.add(text)
		todo_list.save()

		print ("Added to:", list_name)
		print ("Added:", text)

	def done(self):
		
		item_id = int(sys.argv[2])
		self.donein("todo", item_id)

	def donein(self, list_name="todo", item_id=None):
		
		if item_id is None:
			list_name = sys.argv[2]
			item_id = int(sys.argv[3])


		todo_list = TodoList(self.getListFilename(list_name))
		removed_text = todo_list.remove(item_id)
		todo_list.save()

		print ("Removed from:", list_name)
		print ("Removed:", removed_text)

	def list(self, list_name="todo"):
		
		if len(sys.argv) > 2:
			list_name = sys.argv[2]

		print (TodoList(self.getListFilename(list_name)))

	def getListFilename(self, list_name):
		
		filename = json_folder + list_name.lower() + ".json"
		return filename

	def move(self, item_id=None, lname_from=None, lname_to=None):
		

		item_id = int(sys.argv[2])
		lname_from = sys.argv[3]
		lname_to = sys.argv[4]

		list_from = TodoList(self.getListFilename(lname_from))
		list_to = TodoList(self.getListFilename(lname_to))

		list_to.add(list_from[item_id].text)
		list_from.remove(item_id)

		list_from.save()
		list_to.save()

		print ("Moved to: %s" % lname_to)

	def help(self):
		
		print ()
		print ("Usage:-")
		print ("\t create <list> \t\t\t - Creates a list with the name <list>")
		print ()
		print ("\t addto <list> <message> \t - Adds a message to a certain list")
		print ()
		print ("\t donein <list> <ID> \t\t - Marks a message done in a certain list")
		print ()
		print ("\t list <list> \t\t\t - Prints out a certain list.")
		print ()
		print ("\t delete <list> \t\t\t - Deletes the list with the name <list>")
		print ()

Todo().run()
