
#не очень интересный редактор слишком ограничено

# https://pythonru.com/uroki/obuchenie-python-gui-uroki-po-tkinter

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

window = Tk()
window.geometry('840x420')


window.title("Добро пожаловать в приложение Python")

#***************************
lbl = Label(window, text="Привет", font=("Arial Bold", 20))
lbl.grid(column=0, row=0)

#***************************
input_entry = Entry(window,width=10)  
input_entry.grid(column=1, row=0)  
input_entry.focus()

#***************************
def clicked():
    lbl.configure(text="Я же просил...")
    # res = "Привет {}".format(txt.get())  
    lbl.configure(text=res)  

btn = Button(window, text="Не нажимать!", bg="black", fg="green", command=clicked)
btn.grid(column=2, row=0)

#***************************
# Combobox

lbl2 = Label(window, text=" ")
lbl2.grid(column=0, row=2, pady = 25)


def clicked_combo():
    clicked_element = combo.get()
    lbl2.configure(text=clicked_element)


combo = Combobox(window)  
combo['values'] = (1, 2, 3, 4, 5, "Текст" )  
combo.current(1)  # установите вариант по умолчанию  
combo.grid(column=1, row=2)


btn2 = Button(window, text="Не нажимать!", bg="white", fg="black", command=clicked_combo)
btn2.grid(column=2, row=2)
#***************************
# чекбокс
chk = Checkbutton(window, text='Выбрать')

chk_state = BooleanVar()  
# если надо задать через int 
chk_state = IntVar()
chk_state.set(0) # False
chk_state.set(1) # True




chk_state.set(True)  # задайте проверку состояния чекбокса 
chk = Checkbutton(window, text='Выбрать', var=chk_state)  
chk.grid(column=0, row=4)  


#***************************
#Radio Button 

def selected_radio_button():  
    lbl.configure(text=selected.get())

def selected_1_radio():
    lbl.configure(text=selected.get())

selected = IntVar()  
rad1 = Radiobutton(window,text='Первый', value=1, variable=selected, command=selected_1_radio)  
rad2 = Radiobutton(window,text='Второй', value=2, variable=selected)  
rad3 = Radiobutton(window,text='Третий', value=3, variable=selected)  
btn2 = Button(window, text="выбранный вариант", command=selected_radio_button)  
lbl3 = Label(window)  
rad1.grid(column=0, row=4)  
rad2.grid(column=1, row=4)  
rad3.grid(column=2, row=4)  
btn2.grid(column=3, row=4)  
lbl3.grid(column=0, row=5)  

#***************************
# текстовая область Tkinter

txt_field = ScrolledText(window,width=40,height=10)
txt_field.grid(column=0, row=6)  

txt_field.insert(INSERT, 'Текстовое поле')

txt_field.delete(1.0, END)  # мы передали координаты очистки


window.mainloop()













