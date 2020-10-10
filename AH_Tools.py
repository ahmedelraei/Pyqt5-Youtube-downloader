# AH_Tools Module (by ahmed hatem)

# imports
from tkinter import *
from tkinter import ttk
import getpass
import os

# generating form
# ---> form('#dimensions', '#centered or not (True/False)')

def form(geometry='', is_center=True):
	f = Tk()
	f.geometry(geometry)
	if is_center: frmCenter(f)
	return f



# generating TextBox 
#---> txtbx('#FormVariable', '#numeric only or not (True/False)')

def txtbx(form, is_digit=False):
	def is_number(text):
		if str.isdigit(text):
			return True
		elif text is '':
			return True
		else: 
			return False
	reg = form.register(is_number)
	txt = ttk.Entry(form)
	if is_digit:
		txt.config(font=font_all,validate='key', validatecommand=(reg,'%P'))
	return txt


# Function for Centering Forms
# ---> frmCenter(#formVariable)
def frmCenter(form):
	form.update()
	fw = form.winfo_width()
	fh = form.winfo_height()
	sw = form.winfo_screenwidth()
	sh = form.winfo_screenheight()
	x  = (sw - fw) / 2
	y  = (sh - fh) /2
	form.geometry('%dx%d+%d+%d' % (fw,fh,x,y))

# General Background for all parts of form
# ---> general_bg('#formVariable', '#color', ' #coloring include tkinter.Entry or not(True/false)')

def general_bg(form,bg,entry):
	form.update()
	parts = form.winfo_children()
	form.config(bg=bg)
	for p in parts:
		class_info = p.winfo_class()
		if class_info == 'Label' or class_info=='Button':
			p['bg']=bg

		elif class_info == 'Entry':
			if entry == True:
				p['bg']=bg
			else: pass

		if class_info == 'TLabel' or class_info=='TButton':
			style = ttk.Style()
			style.configure('TLabel', background=bg)
			style.configure('TButton', background=bg)

# General Font for all parts of form
# ---> font_all('#formVariable', '#font')

def font_all(form,font):
	form.update()
	parts = form.winfo_children()
	for p in parts:
		class_info = p.winfo_class()
		if class_info == 'Label' or class_info=='Button' or class_info=='Entry' or class_info=='TEntry':
			p['font']=font
		if class_info == 'TLabel' or class_info=='TButton':
			style = ttk.Style()
			style.configure('TLabel', font=font)
			style.configure('TButton', font=font)

# General Font for all parts of form
# ---> fg_all('#formVariable','#forground color', '#Entry included or not (True/False)', '#entry color if not included')

def fg_all(form,fg,entry,e_fg='none'):
	form.update()
	parts = form.winfo_children()
	for p in parts:
		class_info = p.winfo_class()
		if class_info == 'Label' or class_info=='Button':
			p['fg']=fg
		elif class_info == 'Entry':
			if entry == False:
				p['fg']=e_fg
			else: p['fg']=fg
		if class_info == 'TLabel' or class_info=='TButton':
			style = ttk.Style()
			style.configure('TLabel', foreground=fg)
			style.configure('TButton', foreground=fg)
		elif class_info == 'TEntry':
			if entry == False:
				style = ttk.Style()
				style.configure('TEntry', foreground=e_fg)
			else: style.configure('TEntry', foreground=fg)


# py app start on boot | ---> start_on_boot('#leave empty',os.path.join(__file__))
# don't change any thing in 2nd argument

def start_onBoot(file_path="",fileLocation=''):
	user_name = getpass.getuser()
	if file_path == "":
		dir_path = fileLocation
		file_path = dir_path
		bat_path = r'C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup' % user_name
	with open(bat_path + '/' + "keystartup.bat", "w+") as bat_file:
		bat_file.write(r'start %s' % file_path)

		return start_onBoot


start_onBoot()
# generate input box

def  inpbx(text):
	f = Toplevel()
	f.title(text)
	f.geometry('500x200')
	f.resizable(False, False)
	frmCenter(f)
	ttk.Label(f, text=text, font="none 15").pack(pady=10)
	sv = StringVar()
	txt = ttk.Entry(f, font='none 15',width=35,textvariable=sv)
	txt.pack(pady=10)
	txt.bind('<Return>', lambda t: f.destroy())

	ttk.Style().configure('TButton',font='none 15')
	ttk.Button(f,txt="ok",command=lambda:f.destroy()).pack(pady=10)
	f.grab_set()
	txt.focus()
	f.wait_window()
	return sv.get()