__author__ = 'Dario Benšić'

from tkinter import *

import sqlite3

class Application(Frame):
    """GUI aplikacija"""

    def __init__(self, master):
        """Initialize the Frame"""
        Frame.__init__(self,master, bd=0, relief=SUNKEN)
        self.g_name = ""
        self.g_lastname = ""
        self.g_address = ""
        self.g_city = ""
        self.g_email = ""
        self.g_phone = ""
        self.g_mobile = ""
        self.g_text = ""
        self.g_label_success = ""
        self.g_label_error = ""
        self.content = ""
        self.g_list_label = ""
        self.g_list_container_label = ""
        self.index = 0
        self.grid(row=0, column=0, padx=10, pady=10)
        self.create_widgets()

        self.conn = sqlite3.connect('address_book.db')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

        self.tableCreate()

        self.readData()

    def create_widgets(self, index=-1):
        if index >= 0:
            data = self.readItemData(index)
            #print(data[1])
            self.g_name = data[1]
            self.g_lastname = data[2]
            self.g_address = data[3]
            self.g_city = data[4]
            self.g_email = data[5]
            self.g_phone = data[6]
            self.g_mobile = data[7]
            self.g_text = data[8]
        else :
            data = ""
            self.g_name = ""
            self.g_lastname = ""
            self.g_address = ""
            self.g_city = ""
            self.g_email = ""
            self.g_phone = ""
            self.g_mobile = ""
            self.g_text = ""

        name_value = StringVar()
        lastname_value = StringVar()
        address_value = StringVar()
        city_value = StringVar()
        email_value = StringVar()
        phone_value = StringVar()
        mobile_value = StringVar()
        #text_value = StringVar()

        name_value.set(self.g_name)
        lastname_value.set(self.g_lastname)
        address_value.set(self.g_address)
        city_value.set(self.g_city)
        email_value.set(self.g_email)
        phone_value.set(self.g_phone)
        mobile_value.set(self.g_mobile)
        #text_value.set(self.g_text)

        """Create button, text, and entry widgets"""
        self.name_label = Label(self, text="Ime *")
        self.name_label.grid(row=0, column=0, columnspan=2, sticky=W)

        self.name = Entry(self, textvariable=name_value)
        self.name.grid(row=0, column=1, sticky = W)

        self.lastname_label = Label(self, text="Prezime *")
        self.lastname_label.grid(row=2, column=0, columnspan=2, sticky=W)

        self.lastname = Entry(self, textvariable=lastname_value)
        self.lastname.grid(row=2, column=1, sticky = W)

        self.address_label = Label(self, text="Adresa")
        self.address_label.grid(row=4, column=0, columnspan=2, sticky=W)

        self.address = Entry(self, textvariable=address_value)
        self.address.grid(row=4, column=1, sticky = W)

        self.city_label = Label(self, text="Mjesto")
        self.city_label.grid(row=6, column=0, columnspan=2, sticky=W)

        self.city = Entry(self, textvariable=city_value)
        self.city.grid(row=6, column=1, sticky = W)

        self.email_label = Label(self, text="E-mail")
        self.email_label.grid(row=8, column=0, columnspan=2, sticky=W)

        self.email = Entry(self, textvariable=email_value)
        self.email.grid(row=8, column=1, sticky = W)

        self.phone_label = Label(self, text="Telefon")
        self.phone_label.grid(row=10, column=0, columnspan=2, sticky=W)

        self.phone = Entry(self, textvariable=phone_value)
        self.phone.grid(row=10, column=1, sticky = W)

        self.mobile_label = Label(self, text="Mobitel *")
        self.mobile_label.grid(row=12, column=0, columnspan=2, sticky=W)

        self.mobile = Entry(self, textvariable=mobile_value)
        self.mobile.grid(row=12, column=1, sticky = W)

        self.text = Text(self, width=25, height=5, wrap=WORD)
        self.text.grid(row=15, column=0, columnspan=2, sticky=W)

        self.text_label = Label(self, text="Dodatno")
        self.text_label.grid(row=14, column=0, columnspan=2, sticky=W)

        self.submit_button = Button(self, text = "Spremi", command=self.save)
        self.submit_button.grid(row=16, column=0, sticky=W)

        self.result_label = Label(self, text="")
        self.result_label.grid(row=18, column=0, columnspan=2, sticky=W)

        self.g_list_container_label = Label(self, text="")
        self.g_list_container_label.grid(row=2, column=600, columnspan=2, sticky=W)

        self.text.insert(END, self.g_text)

        if index >= 0:
            self.edit_button = Button(self, text = "Uredi")
            self.edit_button.grid(row=16, column=1, sticky=N+W)

            self.delete_button = Button(self, text = "Izbriši")
            self.delete_button.grid(row=16, column=1, sticky=E)

            self.edit_button.bind('<Button>', self.update_item)
            self.delete_button.bind('<Button>', self.delete_item)


    def showEditForm(self, index):
        self.create_widgets(index)

    def on_select(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        #print(index)
        self.index = index
        self.result_label.config(text="")
        self.showEditForm(index)

    def tableCreate(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS phone_book("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), "
                  "lastname VARCHAR(50), "
                  "address VARCHAR(100), city VARCHAR(60), "
                  "email VARCHAR(60), phone VARCHAR(50), "
                  "mobile VARCHAR(50), text TEXT, "
                  "created DATETIME DEFAULT CURRENT_TIMESTAMP)")

    def readItemData(self, index):
        self.content = ""
        #self.index = index
        edit_id = self.getId(self.index)

        sql = "SELECT * FROM phone_book where id = ? order by id desc"
        self.c.execute(sql,(edit_id,))

        r = self.c.fetchone()
        return r

    def readData(self):
        self.content = ""
        sql = "SELECT * FROM phone_book order by id desc"

        self.g_list_label = Label(root, text="Adresar: ")
        self.g_list_label.grid(row=0, column=1,
           sticky=N+W, padx=10, pady=10)

        self.Lb1 = Listbox(root, width=30, height=17)
        self.Lb1.grid(row=0, column=1, rowspan=2,
           sticky=S, padx=10, pady=10)
        scrl = Scrollbar(root, command=self.Lb1.yview)
        self.Lb1.config(yscrollcommand=scrl.set)
        scrl.grid(row=0, column=2, rowspan=2,
           sticky='ns', padx=0, pady=10)

        self.mobile_label = Label(root, text="Copyright © Dario Benšić\ndario.bensic@gmail.com")
        self.mobile_label.grid(row=2, column=0,
            sticky=W, padx=10, pady=10)

        for row in self.c.execute(sql) :
            #self.content += row['name']+" [Izbriši]\n"
            self.Lb1.insert(0, row['name']+" "+row['lastname'])

        self.Lb1.bind('<<ListboxSelect>>', self.on_select)

    def getId(self, index):
        self.content = ""

        #print("SELECT id FROM phone_book order by id asc limit "+str(index)+",1 ")
        sql = "SELECT id FROM phone_book order by id asc limit ?,1 "

        self.c.execute(sql,(str(index),))
        edit_id = self.c.fetchone()

        return edit_id['id']

    def save(self):
        self.g_label_success = "Podaci su uspješno spremljeni!"
        self.g_label_error = "Podaci NISU uspješno spremljeni!"

        g_name = self.name.get()
        g_lastname = self.lastname.get()
        g_address = self.address.get()
        g_city = self.city.get()
        g_email = self.email.get()
        g_phone = self.phone.get()
        g_mobile = self.mobile.get()
        g_text = self.text.get(1.0, END)

        if((g_name != "") and (g_lastname != "") and (g_mobile != "")):
            sql = "INSERT INTO phone_book (name,lastname,address,city,email," \
                  "phone,mobile,text) VALUES (?,?,?,?,?,?,?,?)"
            self.c.execute(sql,(g_name,g_lastname,g_address,g_city,
                                g_email,g_phone,g_mobile,g_text))

            self.conn.commit()

            self.readData()

            self.name.delete(0, END)
            self.name.insert(0, "")
            self.lastname.delete(0, END)
            self.lastname.insert(0, "")
            self.address.delete(0, END)
            self.address.insert(0, "")
            self.city.delete(0, END)
            self.city.insert(0, "")
            self.email.delete(0, END)
            self.email.insert(0, "")
            self.phone.delete(0, END)
            self.phone.insert(0, "")
            self.mobile.delete(0, END)
            self.mobile.insert(0, "")
            self.text.delete(0.0, END)
            self.text.insert(0.0, "")
            self.result_label.config(text=self.g_label_success,fg="blue")
        else :
            self.result_label.config(text=self.g_label_error,fg="red")

        self.index = -1

    def update_item(self, event):
        self.g_label_success = "Podaci su uspješno izmijenjeni!"
        self.g_label_error = "Podaci NISU uspješno izmijenjeni!"

        g_name = self.name.get()
        g_lastname = self.lastname.get()
        g_address = self.address.get()
        g_city = self.city.get()
        g_email = self.email.get()
        g_phone = self.phone.get()
        g_mobile = self.mobile.get()
        g_text = self.text.get(1.0, END)

        if((self.index >= 0) and (g_name != "") and (g_lastname != "") and (g_mobile != "")):
            id = self.getId(self.index)
            sql = "UPDATE phone_book SET name=?,lastname=?,address=?," \
                  "city=?,email=?,phone=?,mobile=?,text=? WHERE id=?"
            self.c.execute(sql,(g_name,g_lastname,g_address,g_city,
                                g_email,g_phone,g_mobile,g_text,id))
            self.conn.commit()

            self.readData()

            self.name.delete(0, END)
            self.name.insert(0, "")
            self.lastname.delete(0, END)
            self.lastname.insert(0, "")
            self.address.delete(0, END)
            self.address.insert(0, "")
            self.city.delete(0, END)
            self.city.insert(0, "")
            self.email.delete(0, END)
            self.email.insert(0, "")
            self.phone.delete(0, END)
            self.phone.insert(0, "")
            self.mobile.delete(0, END)
            self.mobile.insert(0, "")
            self.text.delete(0.0, END)
            self.text.insert(0.0, "")
            self.result_label.config(text=self.g_label_success,fg="blue",justify=LEFT)
        else :
            self.result_label.config(text=self.g_label_error,fg="red")

        self.index = -1

    def delete_item(self, event):
        #print("clicked ", event.x, event.y)
        self.g_label_success = "Podaci su uspješno izbrisani!"
        self.g_label_error = "Podaci NISU uspješno izbrisani!"

        if self.index >= 0:
            id = self.getId(self.index)
            #print("DELETE from phone_book where id = "+str(id)+"")
            sql = "DELETE from phone_book where id = ?"
            self.c.execute(sql,(id,))
            self.conn.commit()

            self.readData()

            self.name.delete(0, END)
            self.name.insert(0, "")
            self.lastname.delete(0, END)
            self.lastname.insert(0, "")
            self.address.delete(0, END)
            self.address.insert(0, "")
            self.city.delete(0, END)
            self.city.insert(0, "")
            self.email.delete(0, END)
            self.email.insert(0, "")
            self.phone.delete(0, END)
            self.phone.insert(0, "")
            self.mobile.delete(0, END)
            self.mobile.insert(0, "")
            self.text.delete(0.0, END)
            self.text.insert(0.0, "")
            self.result_label.config(text=self.g_label_success,fg="blue")
        else :
            self.result_label.config(text=self.g_label_error,fg="red")

        self.index = -1

root = Tk()
root.title("Adresar kontakata")
root.geometry("800x600")
app = Application(root)

root.mainloop()