from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import pymysql
from pymysql import cursors


class Dorm:
    def __init__(self,root):
        self.root=root
        self.root.title("Dormatory Management System")
        self.root.geometry("1366x768+0+0")

        #Upper Frame for Title
        title=Label(self.root,text="Dormatory Management System",bd=10,relief=GROOVE,
        font=("times new roman",40,"bold"),bg="grey",fg="white")
        title.pack(side=TOP,fill=X)

        #Variables
        self.name_var = StringVar()
        self.roll_var = StringVar()
        self.room_var = StringVar()
        self.email_var = StringVar()
        self.contact_var = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()

        #Manage Frame Left Side
        Manage_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="grey")
        Manage_Frame.place(x=5,y=85,width=550,height=650)

        m_title=Label(Manage_Frame,text="Manage Students",
        font=("times new roman",30,"bold"),bg="black",fg="white")
        m_title.grid(row=0,columnspan=2,pady=20,sticky="w")
        #NAME
        lbl_name=Label(Manage_Frame,text="Student Name",
        font=("times new roman",20,"bold"),bg="grey")
        lbl_name.grid(row=1,column=0,pady=10,padx=20,sticky="w")

        txt_name=Entry(Manage_Frame,textvariable=self.name_var,
        font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        txt_name.grid(row=1,column=1,pady=10,padx=20,sticky="w")
        #ID
        lbl_roll=Label(Manage_Frame,text="Student ID",
        font=("times new roman",20,"bold"),bg="grey")
        lbl_roll.grid(row=2,column=0,pady=10,padx=20,sticky="w")

        txt_roll=Entry(Manage_Frame,textvariable=self.roll_var,
        font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        txt_roll.grid(row=2,column=1,pady=10,padx=20,sticky="w")
        #Room
        lbl_room=Label(Manage_Frame,text="Room No",
        font=("times new roman",20,"bold"),bg="grey")
        lbl_room.grid(row=3,column=0,pady=10,padx=20,sticky="w")

        txt_room=Entry(Manage_Frame,textvariable=self.room_var,
        font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        txt_room.grid(row=3,column=1,pady=10,padx=20,sticky="w")
        #Mail
        lbl_email=Label(Manage_Frame,text="Email",
        font=("times new roman",20,"bold"),bg="grey")
        lbl_email.grid(row=4,column=0,pady=10,padx=20,sticky="w")

        txt_email=Entry(Manage_Frame,textvariable=self.email_var,
        font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        txt_email.grid(row=4,column=1,pady=10,padx=20,sticky="w")

        #Contact
        lbl_contact=Label(Manage_Frame,text="Contact No",
        font=("times new roman",20,"bold"),bg="grey")
        lbl_contact.grid(row=5,column=0,pady=10,padx=20,sticky="w")

        txt_contact=Entry(Manage_Frame,textvariable=self.contact_var,
        font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        txt_contact.grid(row=5,column=1,pady=10,padx=20,sticky="w")
        #Address
        lbl_address=Label(Manage_Frame,text="Address",
        font=("times new roman",20,"bold"),bg="grey")
        lbl_address.grid(row=6,column=0,pady=10,padx=20,sticky="w")

        self.txt_address=Text(Manage_Frame,width=36,height=5)
        #font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        self.txt_address.grid(row=6,column=1,pady=10,padx=20,sticky="w")

        #Button Frame--------------------------------------------
        Btn_Frame=Frame(Manage_Frame,bg='grey')
        Btn_Frame.place(x=55,y=520,width=475)
        
        Btn_add=Button(Btn_Frame,text="Add",font=("times new roman",12),width=10,command=self.add_student)
        Btn_add.grid(row=0,column=0,padx=10,pady=10)

        Btn_update=Button(Btn_Frame,text="Update",font=("times new roman",12),width=10,command=self.update_data)
        Btn_update.grid(row=0,column=1,padx=10,pady=10)

        Btn_delete=Button(Btn_Frame,text="Delete",font=("times new roman",12),width=10,command=self.delete_data)
        Btn_delete.grid(row=0,column=2,padx=10,pady=10)

        Btn_clear=Button(Btn_Frame,text="Clear",font=("times new roman",12),width=10,command=self.clear)
        Btn_clear.grid(row=0,column=3,padx=10,pady=10)
        
        
        #Detail Frame Right Side------------------------------------------
        Detail_Frame=Frame(self.root,bd=4,relief=RIDGE)
        Detail_Frame.place(x=560,y=85,width=800,height=650)

        lbl_search = Label(Detail_Frame,text="Search By",font=("times new roman",15,"bold"))
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        combo_search = ttk.Combobox(Detail_Frame,textvariable=self.search_by,font=("times new roman",15),state="readonly",width=10)
        combo_search['values'] = ['Name','ID','Room','Contact']
        combo_search.grid(row=0,column=1,padx=5,pady=5)

        txt_search = Entry(Detail_Frame,textvariable=self.search_txt,font=("times new roman",15),bd=5,relief=GROOVE)
        txt_search.grid(row=0,column=2,padx=5,pady=5)

        btn_search = Button(Detail_Frame,text="Search",font=("times new roman",12),width=10,command=self.search_data)
        btn_search.grid(row=0,column=3,padx=5,pady=5)

        btn_showall = Button(Detail_Frame,text="Show All",font=("times new roman",12),width=10,command=self.fetch_data)
        btn_showall.grid(row=0,column=4,padx=5,pady=5)


        #Table Frame
        Table_Frame = Frame(Detail_Frame,bd=4,relief=RIDGE)
        Table_Frame.place(x=10,y=70,width=780,height=550)

        #Room,ID,Name,Contact,Mail,Address
        scroll_x = Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame,orient=VERTICAL)
        self.Student_table = ttk.Treeview(Table_Frame,columns=("room","roll","name","contact","mail","address"),
        xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)
        self.Student_table.heading("room",text="Room")
        self.Student_table.heading("roll",text="ID")
        self.Student_table.heading("name",text="Name")
        self.Student_table.heading("contact",text="Mobile")
        self.Student_table.heading("mail",text="Mail")
        self.Student_table.heading("address",text="Address")
        self.Student_table['show'] = 'headings'

        self.Student_table.column("room",width=50)
        self.Student_table.column("roll",width=80)
        self.Student_table.column("name",width=150)
        self.Student_table.column("contact",width=150)
        self.Student_table.column("mail",width=150)
        self.Student_table.column("address",width=250)
        
        self.Student_table.pack(fill=BOTH,expand=1)
        self.Student_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    
    def add_student(self):
        if(self.roll_var.get()=="" or self.name_var.get()==""):
            messagebox.showerror("Error","Name & ID Fields are required")
            return
            
        con = pymysql.connect(host="localhost",user="root",password="7426",database="Dorm")
        cur = con.cursor()
        cur.execute("insert into residence values(%s,%s,%s,%s,%s,%s)",
        (self.name_var.get(),self.roll_var.get(),self.room_var.get(),self.email_var.get(),self.contact_var.get(),self.txt_address.get('1.0',END)))
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()
        messagebox.showinfo("Success","Record Added")
    
    def fetch_data(self):
        con = pymysql.connect(host="localhost",user="root",password="7426",database="Dorm")
        cur = con.cursor()
        cur.execute("select room,id,name,contact,mail,address from residence")
        rows = cur.fetchall()
        if(len(rows))!=0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('',END,values=row)
        con.commit()
        con.close()
    
    def clear(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.room_var.set("")
        self.email_var.set("")
        self.contact_var.set("")
        self.txt_address.delete("1.0",END)
    
    def get_cursor(self,ev):
        cursor_row = self.Student_table.focus()
        contents = self.Student_table.item(cursor_row)
        row = contents['values']
        self.txt_address.delete("1.0",END)
        self.roll_var.set(row[1])
        self.name_var.set(row[2])
        self.room_var.set(row[0])
        self.email_var.set(row[4])
        self.contact_var.set(row[3])
        self.txt_address.insert(END,row[5])
    def update_data(self):
        con = pymysql.connect(host="localhost",user="root",password="7426",database="Dorm")
        cur = con.cursor()
        cur.execute("update residence set name=%s, room=%s, mail=%s, contact=%s, address=%s where id=%s",(
            self.name_var.get(),
            self.room_var.get(),
            self.email_var.get(),
            self.contact_var.get(),
            self.txt_address.get('1.0',END),
            self.roll_var.get()
        ))
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()
    def delete_data(self):
        con = pymysql.connect(host="localhost",user="root",password="7426",database="Dorm")
        cur = con.cursor()
        cur.execute("delete from residence where id=%s",self.roll_var.get())
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()
    
    def search_data(self):
        con = pymysql.connect(host="localhost",user="root",password="7426",database="Dorm")
        cur = con.cursor()
        cur.execute("select room,id,name,contact,mail,address from residence where "+str(self.search_by.get())+" LIKE '%"+str(self.search_txt.get())+"%'")
        rows = cur.fetchall()
        if(len(rows))!=0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('',END,values=row)
        con.commit()
        con.close()
        



        





root = Tk()
ob = Dorm(root)
root.mainloop()
