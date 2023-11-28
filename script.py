import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fpdf import FPDF


# -------------------------
# Shows menu
# -------------------------

def show_menu():

    # if teachers or class or subjects are being edited ask to save changes or not
    global is_editing_classes,is_editing_teachers,is_editing_subjects,is_creating_general

    if is_editing_classes:
        print("new",ec.new_class_list)
        print(class_list)
        if ec.new_class_list!=class_list:
            opt=messagebox.askyesno(title="",message="Save changes?")
            if opt:
                ec.edit_classes_done()
            is_editing_classes=False

    if is_editing_teachers:
        print("new",et.new_teacher_list)
        print(teacher_list)
        if et.new_teacher_list!=teacher_list:
            opt=messagebox.askyesno(title="",message="Save changes?")
            if opt:
                et.edit_teachers_done()
            is_editing_teachers=False

    if is_editing_subjects:
        print("new",es.new_subject_list)
        print(subject_list)
        if es.new_subject_list!=subject_list:
            opt=messagebox.askyesno(title="",message="Save changes?")
            if opt:
                et.edit_teachers_done()
            is_editing_subjects=False

    # if general is being edited
    is_edited=False
    if is_creating_general:
        for obj in tt_frame_objs:
            for i in range(len(obj.period_subjects)):
                for j in range(len(obj.period_subjects[i])):
                    if obj.period_subjects[i][j].get()!=obj.s[i][j] or obj.period_teachers[i][j].get()!=obj.t[i][j]:
                        is_edited=True
                        break
                if is_edited:
                    break
            if is_edited:
                break
    if is_edited:
        opt=messagebox.askyesno(title="",message="Save changes?")
        if opt:
            save_general(tt_frame_objs,title_name)

    # visual changes
    edit_teachers_frame.destroy()
    edit_classes_frame.destroy()
    edit_subjects_frame.destroy()
    selection_frame.destroy()
    regular_tt_frame.destroy()
    tt_creation_frame.destroy()
    menubutton.pack_forget()
    menu_frame.pack()


# ---------- Create Button clicked ----------

def create_tt():

    global selection_frame
    selection_frame=tk.Frame(root)
    selection_page=selection_frame_creator(selection_frame)
    selection_page.create()

class selection_frame_creator():

    def __init__(self,container):

        # container
        self.container=container

        # day selection
        self.day_selection_frame=tk.Frame(container,bd=2,background='black')
        self.select_day_label=ttk.Label(self.day_selection_frame,text="Select Day:")
        self.selected_day=tk.StringVar()

        # teacher selection
        self.teachers_selection_frame=tk.Frame(container,bd=2,background='black')
        # tsf - teacher selection frame
        self.tsf_canvas=tk.Canvas(self.teachers_selection_frame)
        self.tsf_scrollbar=ttk.Scrollbar(self.teachers_selection_frame,orient="vertical",command=self.tsf_canvas.yview)
        self.tsf_list=tk.Frame(self.tsf_canvas)
        self.teachers_attendance=[]

        # class selection
        self.class_selection_frame=tk.Frame(container,bd=2,background='black')
        # csf - class selection frame
        self.csf_canvas=tk.Canvas(self.class_selection_frame)
        self.csf_scrollbar=ttk.Scrollbar(self.class_selection_frame,orient="vertical",command=self.csf_canvas.yview)
        self.csf_list=tk.Frame(self.csf_canvas)
        self.classes_attendance=[]

    def create(self):

        menu_frame.pack_forget()
        self.container.pack()

        # day selection frame
        self.day_selection_frame.grid(column=0,row=3,sticky=tk.EW,pady=5,padx=5,ipadx=3)
        self.select_day_label.pack(expand=True,fill='x')
        for d in days:
            ttk.Radiobutton(self.day_selection_frame,text=d,value=d,variable=self.selected_day).pack(side='left',fill='both',expand=True,ipadx=3)

        # teacher selection frame ( Scrollable )
        self.tsf_list.bind(
            "<Configure>",
            lambda e: self.tsf_canvas.config(scrollregion=self.tsf_canvas.bbox("all"))
        )
        self.tsf_canvas.create_window((0,0),window=self.tsf_list,anchor="nw")
        self.tsf_canvas.config(yscrollcommand=self.tsf_scrollbar.set)
        self.teachers_selection_frame.grid(column=0,row=1,sticky=tk.EW,pady=5,padx=5)
        tk.Label(self.teachers_selection_frame,text="Select Teachers:").pack(anchor=tk.W,fill='x')
        self.tsf_canvas.pack(side='left',fill='both',expand=True)
        self.tsf_scrollbar.pack(side='right',fill='y')
        for i in range(len(teacher_list)):
            self.teachers_attendance.append(tk.StringVar())
            t=tk.Checkbutton(self.tsf_list,text=teacher_list[i],variable=self.teachers_attendance[i],onvalue="Present",offvalue="Absent")
            t.pack(anchor=tk.W)
            t.select()

        # class selection frame ( Scrollable )
        self.csf_list.bind(
            "<Configure>",
            lambda e: self.csf_canvas.config(scrollregion=self.csf_canvas.bbox("all"))
        )
        self.csf_canvas.create_window((0,0),window=self.csf_list,anchor="nw")
        self.csf_canvas.config(yscrollcommand=self.csf_scrollbar.set)
        self.class_selection_frame.grid(column=1,row=1,sticky=tk.EW,pady=5,padx=5)
        tk.Label(self.class_selection_frame,text="Select Classes:").pack(anchor=tk.W,fill='x')
        self.csf_canvas.pack(side='left',fill='both',expand=True)
        self.csf_scrollbar.pack(side='right',fill='y')
        for i in range(len(class_list)):
            self.classes_attendance.append(tk.StringVar())
            t=tk.Checkbutton(self.csf_list,text=class_list[i],variable=self.classes_attendance[i],onvalue="Present",offvalue="Absent")
            t.pack(anchor=tk.W)
            t.select()

        # continue button
        ttk.Button(self.container,text="Continue",command=lambda con=self:continue_creation(con)).grid(column=1,row=3,pady=5,padx=5,sticky=tk.SE)
        root.bind('<Return>',lambda event,self=self:continue_creation(self))
        menubutton.pack()


# -- Continue button clicked -> Creation

def continue_creation(sfc): 

    # sfc - selection frame creator
    if sfc.selected_day.get()=="":
        messagebox.showinfo(title="Attention",message="Please select a day!")
        return

    # unbinding keyboard enter action from previous page button
    root.unbind('<Return>')
    selection_frame.destroy()
    selection_frame.pack_forget()
    menubutton.pack_forget()
    
    # new page
    global tt_creation_frame
    tt_creation_frame=tk.Frame(root)

    # decalaration of variables needed
    global present_teachers,present_classes,absent_teachers,absent_classes
    present_teachers=[]
    present_classes=[]
    absent_teachers=[]
    absent_classes=[]

    # collect absent teachers
    for i in range(len(sfc.teachers_attendance)):
        if sfc.teachers_attendance[i].get()=="Absent":
            absent_teachers.append(teacher_list[i])

    # collect absent classes
    for i in range(len(sfc.classes_attendance)):
        if sfc.classes_attendance[i].get()=="Absent":
            absent_classes.append(class_list[i])

    # collect present teachers
    for i in range(len(sfc.teachers_attendance)):
        if sfc.teachers_attendance[i].get()=="Present":
            present_teachers.append(teacher_list[i])

    # collect present classes
    for i in range(len(sfc.classes_attendance)):
        if sfc.classes_attendance[i].get()=="Present":
            present_classes.append(class_list[i])
    
    # creating frame
    title_frame=tk.Frame(tt_creation_frame)
    title_frame.pack()
    ttk.Label(title_frame,text="Title:").pack(side="left")
    title_name=tk.StringVar()
    title_name_entry=tk.Entry(title_frame,textvariable=title_name)
    title_name_entry.pack()

    try:
        f=open("files//values.txt","r")
        title_name_filler=f.readline().lstrip("title:").rstrip("\n")
        title_name_entry.insert(0,title_name_filler)
        f.close()
    except:
        pass

    tt_creation_frame.pack(fill='both')
    tt_frame_page=tt_frame_creator(tt_creation_frame,tt_type="today",selected_day=sfc.selected_day.get())
    tt_frame_page.time_table_struct()


# ---------- Create Time Table Frame (Used in both regular and current time tables)

class tt_frame_creator():

    def __init__(self,container,tt_type,selected_day=None):

        # fetching parameters
        self.container=container
        self.tt_type=tt_type
        self.selected_day=selected_day

        self.edit_tt_frame=tk.Frame(container)
        # ettf - edit time table frame
        self.ettf_canvas=tk.Canvas(self.edit_tt_frame,highlightthickness=0)
        self.ettf_xscrollbar=ttk.Scrollbar(self.edit_tt_frame,orient='horizontal',command=self.ettf_canvas.xview)
        self.ettf_yscrollbar=ttk.Scrollbar(self.edit_tt_frame,orient='vertical',command=self.ettf_canvas.yview)
        self.tt_editing_grid=tk.Frame(self.ettf_canvas,bg='black',bd=2)
        if self.tt_type=="today":
            self.save_button=ttk.Button(container,text="Save",command=save_time_table)
            self.combobox_state='normal'
        if tt_type=="regular":
            self.combobox_state='readonly'
        self.default_class_periods=[]
        self.subject_menubuttons=[]
        self.teacher_menubuttons=[]
        self.period_subjects=[]
        self.period_teachers=[]
        # st - student teacher
        self.st_frames=[]
        self.absent_blocks=[]

    def time_table_struct(self):

        global n_periods
        # -- preparing default fillers
        f=open(f".\\regular\\{self.selected_day}.csv","r",newline="")
        fo=csv.reader(f)
        self.s=[] # contain sequenced subject list for periods
        self.t=[] # contain sequenced teacher list for periods
        self.c=[] # contain class names

        # odd positions for subjects and even for teachers
        pos=1
        for i in fo:
            if pos%2!=0:
                self.c.append(i[0])
                self.s.append(i[1:len(i)])
            else:
                self.t.append(i[1:len(i)])
            pos+=1

        # -- collecting present classes and teachers

        global present_classes
        # select all classes if editing regular
        if self.tt_type=='regular':
            present_classes=class_list

        global present_teachers
        # select all teachers if editing regular
        if self.tt_type=='regular':
            present_teachers=list(teacher_list)

        # finally preparing list
        for i in present_classes:
            self.default_class_periods.append([i])
            indexval=self.c.index(i)
            for j in range(len(self.s[0])):
                self.default_class_periods[-1].append([self.s[indexval][j],self.t[indexval][j]])
        f.close()


        # -- Creating Time table grid
        
        self.tt_editing_grid.bind(
            "<Configure>",
            lambda e: self.ettf_canvas.config(
                scrollregion=self.ettf_canvas.bbox('all')
            )
        )
        self.ettf_canvas.create_window((0,0),window=self.tt_editing_grid,anchor='nw')
        self.ettf_canvas.config(xscrollcommand=self.ettf_xscrollbar.set)
        self.ettf_canvas.config(yscrollcommand=self.ettf_yscrollbar.set)

        self.edit_tt_frame.pack(fill="both",expand=True)
        self.ettf_xscrollbar.pack(side='top',fill='x')
        self.ettf_canvas.pack(side='left',fill='both',expand=True)
        self.ettf_yscrollbar.pack(side='left',fill='y')

        # preparing columns
        for i in range(0,n_periods+1):
            self.tt_editing_grid.columnconfigure(i,weight=1)
        self.tt_editing_grid.columnconfigure(0,minsize=70)
        for i in range(1,n_periods+1):
            self.tt_editing_grid.columnconfigure(i,minsize=140)
        
        # period labels (I,II,III ....)
        for i in range(1,n_periods+1):
            period_label=ttk.Label(self.tt_editing_grid,text=str(i))
            period_label.grid(column=i,row=0,sticky=tk.NSEW)

        for i in range(1,len(present_classes)+1):

            # class labels
            class_label=tk.Label(self.tt_editing_grid,text=present_classes[i-1])
            class_label.grid(column=0,row=i,sticky=tk.NSEW)

            # contain string values
            class_period_subject=[]
            class_period_teachers=[]

            class_period_menubuttons=[]
            teacher_period_menubuttons=[]
            st_frames=[]

            for j in range(1,n_periods+1):
                subject=tk.StringVar()
                teacher=tk.StringVar()
                class_period_subject.append(subject)
                class_period_teachers.append(teacher)

                st_frame=tk.Frame(self.tt_editing_grid,bd=1,bg='black')
                subject_menubutton=ttk.Combobox(st_frame,textvariable=subject,values=subject_list,state=self.combobox_state)
                teacher_menubutton=ttk.Combobox(st_frame,textvariable=teacher,values=present_teachers,state=self.combobox_state)
                subject_menubutton.bind('<<ComboboxSelected>>',subject_menu_button_clicked)
                teacher_menubutton.bind('<<ComboboxSelected>>',lambda e: teacher_menu_button_clicked(e,self))

                # -- Setting default filled subject and teachers

                global absent_teachers
                if self.tt_type=='regular':
                    absent_teachers=[]
                subject.set(self.default_class_periods[i-1][j][0])
                if self.default_class_periods[i-1][j][1] not in teacher_list:
                    teacher.set("")
                    st_frame.config(bg='red',border=2)
                elif self.default_class_periods[i-1][j][1] not in absent_teachers:
                    teacher.set(self.default_class_periods[i-1][j][1])
                else:
                    teacher.set("Absent")
                    st_frame.config(bg='yellow',border=2)
                    self.absent_blocks.append((i-1,j-1))
                
                st_frames.append(st_frame)
                class_period_menubuttons.append(subject_menubutton)
                teacher_period_menubuttons.append(teacher_menubutton)

                st_frame.grid(column=j,row=i,sticky=tk.NSEW)
                subject_menubutton.pack(fill='x')
                teacher_menubutton.pack(fill='x')

            self.st_frames.append(st_frames)
            self.period_subjects.append(class_period_subject)
            self.period_teachers.append(class_period_teachers)
            self.subject_menubuttons.append(class_period_menubuttons)
            self.teacher_menubuttons.append(teacher_period_menubuttons)

        # -- configuring save button for today's time table creation
        if self.tt_type=='today':
            self.save_button.config(command=lambda: save_time_table(self))
            self.save_button.pack()
            root.bind('<Return>',lambda event:save_time_table(self))
        
        # let the conditions and indicators work instantly
        subject_menu_button_clicked(None)
        teacher_menu_button_clicked(None,self)

        menubutton.pack()

        return self.edit_tt_frame


# ---------- Applying Conditions and indicators in Time Table Frame

def teacher_menu_button_clicked(event,frameid):

    # Check if teacher got two classes in same period
    for i in range(0,n_periods):
        for k in range(len(present_classes)):
            for j in range(len(present_classes)):
                if j==k:
                    continue
                if frameid.period_teachers[k][i].get()==frameid.period_teachers[j][i].get()!="Absent" and frameid.period_teachers[k][i].get()!="":
                    frameid.st_frames[k][i].config(bg='blue')
                    frameid.st_frames[j][i].config(bg='blue')

    # re assigning black border if corrected
    for i in range(0,n_periods):
        for k in range(len(present_classes)):
            for j in range(len(present_classes)):
                if j==k:
                    continue
                if frameid.period_teachers[k][i].get()==frameid.period_teachers[j][i].get() or frameid.period_teachers[k][i].get() in ["Absent",""]:
                    break
            else:
                frameid.st_frames[k][i].config(bg='black')

def subject_menu_button_clicked(event):
    pass
    # Change teacher menu according to subject
    # for i in range(len(classes)):
    #     for j in range(0,n_periods):
    #         try:
    #             subject_teacher=subject_teachers[class_periods[i][j].get()]
    #         except:
    #             subject_teacher=["No teacher found"]
    #         classes_teachers_menubuttons[i][j].configure(values=subject_teacher)


# ---------- Saving Time Table ----------

def save_time_table(frameid):

    # Save (condition:check if all absentees and empty are filled)
    absentee_found=False
    for i in range(len(present_classes)):
        for j in range(0,n_periods):
            if frameid.period_teachers[i][j].get() in ["Absent","No teacher found",""]:
                absentee_found=True
    if absentee_found:
        messagebox.showinfo(title="Attention",message='All not filled!')
        return


    # -- Creating PDF

    f=filedialog.asksaveasfilename(title='Save Table',initialdir='C:',defaultextension='.pdf',initialfile='Time Table',filetypes=[("PDF File",'.pdf')])
    if not f=="":
        pdf=FPDF()
        pdf.add_page()
        pdf.set_margins(3,3,3)

        # title
        pdf.set_font("Times",size=15,style='U')
        f2=open("files//values.txt","r")
        title=f2.readline().lstrip("title:").rstrip("\n")
        f2.close()
        pos_xy=[0,0]
        pdf.set_xy(0,0)
        pdf.multi_cell(w=210,h=15,txt=title,align="C")
        pos_xy=[3,pos_xy[1]+15+1]

        # values
        cell_height=5
        class_gap=1
        period_cell_w=(192/n_periods)
        class_cell_w=13

        # period numbering
        pdf.set_font("Times",size=11)
        pdf.cell(class_cell_w-1,5,border="LTBR")
        pdf.cell(1,5,border="TBR")
        for i in range(1,n_periods+1):
            pdf.cell(period_cell_w,5,txt=roman_count[i],border="TBR",align="C")
        pos_xy[1]+=5

        # time table
        pdf.set_xy(pos_xy[0],pos_xy[1])
        pdf.set_font("Times",size=11)

        for i in range(0,len(present_classes)):

            pdf.cell(class_cell_w-1,cell_height,border="LTR")
            pdf.cell(1,cell_height,border="TR")
            pos_xy[0]+=class_cell_w

            # subjects
            for j in frameid.period_subjects[i]:
                pdf.multi_cell(period_cell_w,cell_height,txt=j.get(),border="TR")
                pos_xy[0]+=period_cell_w
                pdf.set_xy(pos_xy[0],pos_xy[1])
            pdf.ln(cell_height)
            pos_xy=[3,pos_xy[1]+cell_height]

            # -- classes
            pdf.multi_cell(class_cell_w-1,cell_height,txt=present_classes[i],border="LR",align="C")
            pos_xy[0]+=class_cell_w-1
            pdf.set_xy(pos_xy[0],pos_xy[1])
            pdf.cell(1,cell_height,border='R')
            pos_xy[0]+=1

            # extra line for subject name
            for j in range(n_periods):
                pdf.cell(period_cell_w,cell_height,border="BR")
            pdf.ln(cell_height)
            pos_xy=[3,pos_xy[1]+cell_height]

            # extra line for class name
            pdf.cell(class_cell_w-1,cell_height,border="LR")
            pdf.cell(1,cell_height,border='R')
            pos_xy[0]+=class_cell_w

            # -- teachers
            for j in frameid.period_teachers[i]:
                pdf.multi_cell(period_cell_w,cell_height,txt=j.get(),border="R")
                pos_xy[0]+=period_cell_w
                pdf.set_xy(pos_xy[0],pos_xy[1])
            pdf.ln(cell_height)
            pos_xy=[3,pos_xy[1]+cell_height]

            # extra line for teacher name
            pdf.cell(class_cell_w-1,cell_height,border="LBR")
            pdf.cell(1,cell_height,border="BR")
            for j in range(n_periods):
                pdf.cell(period_cell_w,cell_height,border="BR")

            pdf.ln(cell_height+class_gap)
            pos_xy=[3,pos_xy[1]+cell_height+class_gap]
            pdf.set_xy(pos_xy[0],pos_xy[1])

        pdf.output(dest="F",name=f)


# ---------- Creating Presets ----------

def create_general():

    # if no class found
    if class_list==[]:
        messagebox.showinfo(title="Info",message="No class found! Seems you need to add some :)")
        return


    global is_creating_general
    is_creating_general=True

    global regular_tt_frame
    regular_tt_frame=tk.Frame(root)

    # settings
    settings_button=ttk.Button(regular_tt_frame,text='Settings',command=open_settings)
    settings_button.pack()

    # -- title name entry block

    title_frame=tk.Frame(regular_tt_frame)
    title_frame.pack()
    ttk.Label(title_frame,text="Title:").pack(side="left")
    global title_name
    title_name=tk.StringVar()
    title_entry=ttk.Entry(title_frame,textvariable=title_name)
    title_entry.pack()
    try:
        f=open("files//values.txt","r")
        title_name_filler=f.readline().lstrip("title:").rstrip("\n")
        title_entry.insert(0,title_name_filler)
        f.close()
    except:
        pass

    # -- Time table grids for regular preset

    global daytabmenu,tt_frame_objs
    regular_tt_frame.pack(fill='both')
    daytabmenu=ttk.Notebook(regular_tt_frame)
    daytabmenu.pack(fill="both")
    tt_frame_objs=[]
    for i in days:
        obj=tt_frame_creator(daytabmenu,tt_type="regular",selected_day=i)
        tab=obj.time_table_struct()
        daytabmenu.add(tab,text=i)
        tt_frame_objs.append(obj)

    # Save button
    save_button=ttk.Button(regular_tt_frame,text="Save",command=lambda:save_general(tt_frame_objs,title_name))
    save_button.pack()

    # Main Menu button
    menu_frame.pack_forget()
    menubutton.pack_forget()
    menubutton.pack()

# --settings for time table

def open_settings():

    # settings window
    settings_win=tk.Tk()
    settings_win.title("Settings")
    sw_center_x=int(screen_w/2-400/2)
    sw_center_y=int(screen_h/2-100/2)
    settings_win.geometry(f"{400}x{100}+{sw_center_x}+{sw_center_y}")
    settings_win.focus_force()
    root.attributes('-disable',True)
    settings_win.protocol('WM_DELETE_WINDOW',lambda a=settings_win: enable_main_window(a))
    
    ttk.Label(settings_win,text="Periods:").grid(column=0,row=1)
    period_entry=ttk.Spinbox(settings_win,values=(6,8))
    period_entry.grid(column=1,row=1)
    period_entry.insert(0,n_periods)

    # saving changes into files
    def save_settings():

        global n_periods
        f=open("files//values.txt","r")
        title_value=f.readline()
        period_value=f.readline()
        f.close()
        n_periods=int(period_entry.get())
        if period_value[8]!=str(n_periods):
            opt=messagebox.askokcancel(title="Info",message="Changing number of periods will reset time table. Continue?")
            if not opt:
                return

        f=open("files//values.txt","w")
        f.write(title_value)
        f.write(f"periods:{period_entry.get()}\n")
        f.close()
        enable_main_window(settings_win)

        for i in days:
            f=open(f".\\regular\\{i}.csv","w",newline="")
            fo=csv.writer(f)
            for j in class_list:
                fo.writerow([j]+[""]*n_periods)
                fo.writerow([""]*(n_periods+1))
            f.close()
        regular_tt_frame.destroy()
        create_general()

    save_settings_button=ttk.Button(settings_win,text="Save",command=save_settings)
    save_settings_button.grid(column=0,row=2)


# ---------- Saving preset ----------

def save_general(objs,title_name):

    # check if any block is empty
    emptyfound=False
    for obj in objs:
        for i in range(len(class_list)):
            for j in range(0,n_periods):
                if obj.period_subjects[i][j].get() == "":
                    emptyfound=True
                if obj.period_teachers[i][j].get() == "":
                    emptyfound=True
    
    if emptyfound:
        opt=messagebox.askyesno(title="Attention",message='Some values are not filled! Still save?')
        if not opt:
            return


    # -- Write values to backend

    # time table
    for i in range(len(objs)):
        f=open(f".\\regular\\{days[i]}.csv","w",newline="")
        fo=csv.writer(f)
        for j in range(0,len(class_list)):
            r1=[class_list[j]]
            r2=[None]
            for k in objs[i].period_subjects[j]:
                r1.append(k.get())
            for k in objs[i].period_teachers[j]:
                r2.append(k.get())
            fo.writerows([r1,r2])
        f.close()

    # title
    f=open('files//values.txt')
    title_value=f.readline()
    period_value=f.readline()
    f.close()
    f=open("files//values.txt","w")
    f.write(f"title:{title_name.get()}\n")
    f.write(period_value)
    f.close()

    # message
    messagebox.showinfo(title="info",message="Saved!")

    global is_creating_general
    is_creating_general=False
    show_menu()


# ---------- Edit Classes ---------

def edit_classes():

    global is_editing_classes
    is_editing_classes=True

    global edit_classes_frame
    menu_frame.pack_forget()
    edit_classes_frame=tk.Frame(root)
    edit_classes_frame.pack()
    global ec
    ec=editclasses()
    ec.edit_classes()

class editclasses:

    def __init__(self):

        self.new_class_list=list(class_list)
        global edit_classes_frame
        self.class_list_frame=tk.Frame(edit_classes_frame)
        self.class_list_scrollbar=ttk.Scrollbar(self.class_list_frame)
        self.class_listbox=tk.Listbox(self.class_list_frame,yscrollcommand=self.class_list_scrollbar.set)

        self.edit_options_frame=tk.Frame(edit_classes_frame)
        self.add_button=ttk.Button(self.edit_options_frame,text="Add",command=self.add_class1)
        self.edit_button=ttk.Button(self.edit_options_frame,text="Edit",command=self.edit_class1)
        self.delete_button=ttk.Button(self.edit_options_frame,text="Delete",command=self.delete_class)

        self.edit_classes_done_button=ttk.Button(self.edit_options_frame,text="Done",command=self.edit_classes_done)

    def edit_classes(self):

        edit_classes_frame.pack()
        self.class_list_frame.grid(column=0,row=0)
        for i in range(len(self.new_class_list)):
            self.class_listbox.insert(tk.END,self.new_class_list[i])
        self.class_listbox.select_set(0)
        self.class_listbox.pack(side='left')
        self.class_list_scrollbar.pack(side='right',fill='y')
        self.edit_options_frame.grid(column=1,row=0)
        self.add_button.pack()
        self.edit_button.pack()
        self.delete_button.pack()
        self.edit_classes_done_button.pack()

        menubutton.pack()

    def add_class1(self):

        # preparing window
        self.add_window=tk.Tk()
        self.add_window.attributes('-topmost',True)
        self.add_window.protocol("WM_DELETE_WINDOW",lambda a=self.add_window: enable_main_window(a))
        root.attributes('-disable',True)

        # content
        tk.Label(self.add_window,text="Name:").pack(side='left')
        class_name=ttk.Entry(self.add_window)
        class_name.pack(side='left')
        add_class_done=ttk.Button(self.add_window,text="Save",command=lambda a=class_name:self.add_class2(a))
        add_class_done.pack(side='right')

        # centralize window
        self.add_win_w=300
        self.add_win_h=100
        self.center_x=int(screen_w/2-self.add_win_w/2)
        self.center_y=int(screen_h/2-self.add_win_h/2)
        self.add_window.geometry(f"{self.add_win_w}x{self.add_win_h}+{self.center_x}+{self.center_y}")

        # focus and run window
        class_name.focus_force()
        self.add_window.mainloop()

    def add_class2(self,class_name):

        # conditions
        if class_name.get()=="":
            messagebox.showerror(title="Error",message="Can't be empty!",parent=self.add_window)
        elif class_name.get() in self.new_class_list:
            messagebox.showerror(title="Error",message="Already used!",parent=self.add_window)
        else:
            self.class_listbox.insert(0,class_name.get())
            self.new_class_list.insert(0,class_name.get())
            self.class_listbox.selection_clear(0,tk.END)
            self.class_listbox.select_set(0)
            enable_main_window(self.add_window)
        # print("new-",self.new_class_list)
        # print(class_list)

    def edit_class1(self):

        # preparing window
        self.edit_window=tk.Tk()
        self.edit_window.attributes('-topmost',True)
        self.edit_window.protocol("WM_DELETE_WINDOW",lambda a=self.edit_window: enable_main_window(a))
        root.attributes('-disable',True)

        # content
        tk.Label(self.edit_window,text="Name:").pack(side='left')
        class_name=ttk.Entry(self.edit_window)
        class_name.pack(side='left')
        class_index=self.class_listbox.curselection()[0]
        old_class_name=self.class_listbox.get(class_index)
        class_name.insert(0,old_class_name)
        edit_class_done=ttk.Button(self.edit_window,text="Save",command=lambda a=class_name,b=class_index,c=old_class_name:self.edit_class2(a,b,c))
        edit_class_done.pack(side='right')

        # centralize window
        self.edit_win_w=300
        self.edit_win_h=100
        self.center_x=int(screen_w/2-self.edit_win_w/2)
        self.center_y=int(screen_h/2-self.edit_win_h/2)
        self.edit_window.geometry(f"{self.edit_win_w}x{self.edit_win_h}+{self.center_x}+{self.center_y}")

        # focus and run window
        class_name.focus_force()
        self.edit_window.mainloop()

    def edit_class2(self,class_name,class_index,old_class_name):

        class_name=class_name.get()

        # conditions
        if class_name=="":
            messagebox.showerror(title="Error",message="Can't be empty!",parent=self.edit_window)
        elif class_name in self.new_class_list and class_name!=old_class_name:
            messagebox.showerror(title="Error",message="Already used!",parent=self.edit_window)
        else:
            self.class_listbox.delete(class_index)
            self.class_listbox.insert(class_index,class_name)
            self.new_class_list[class_index]=class_name
            self.class_listbox.selection_clear(0,tk.END)
            self.class_listbox.select_set(class_index)
            enable_main_window(self.edit_window)

    def delete_class(self):

        class_index=self.class_listbox.curselection()[0]
        opt=messagebox.askokcancel(title="",message="Delete? All data associated with it will be erased!")
        if opt:
            self.class_listbox.delete(class_index)
            self.new_class_list.pop(class_index)
        # print("new",self.new_class_list)
        # print(class_list)

    def edit_classes_done(self):

        global class_list

        # backend
        for i in self.new_class_list:
            if i not in class_list:
                for j in days:
                    f=open(f"regular//{j}.csv","r",newline="")
                    data=f.readlines()
                    f.close()
                    f=open(f"regular//{j}.csv","w",newline="")
                    f.write(f"{i},,,,,,,,\n")
                    f.write(",,,,,,,,\n")
                    f.writelines(data)
                    f.close()
        for i in class_list:
            if i not in self.new_class_list:
                for j in days:
                    f=open(f"regular//{j}.csv","r",newline="")
                    data=f.readlines()
                    f.close()
                    for k in data:
                        if k.startswith(i+","):
                            indexval=data.index(k)
                            data.pop(indexval+1)
                            data.pop(indexval)
                    f=open(f"regular//{j}.csv","w",newline="")
                    f.writelines(data)
                    f.close()

        # saving changes into files

        class_list=list(self.new_class_list)
        f=open("files//classes.csv","w",newline="")
        fo=csv.writer(f)
        for i in class_list:
            fo.writerow([i])
        f.close()
        edit_classes_frame.destroy()
        global is_editing_classes
        is_editing_classes=False
        show_menu()


# ---------- Editing Teachers ----------

def edit_teachers():

    global is_editing_teachers
    is_editing_teachers=True

    global edit_teachers_frame
    menu_frame.pack_forget()
    edit_teachers_frame=tk.Frame(root)
    edit_teachers_frame.pack()
    global et
    et=editteachers()
    et.edit_teachers()

class editteachers:

    def __init__(self):

        self.new_teacher_list=list(teacher_list)
        global edit_teachers_frame
        self.teacher_list_frame=tk.Frame(edit_teachers_frame)
        self.teacher_list_scrollbar=ttk.Scrollbar(self.teacher_list_frame)
        self.teacher_listbox=tk.Listbox(self.teacher_list_frame,yscrollcommand=self.teacher_list_scrollbar.set)

        self.edit_options_frame=tk.Frame(edit_teachers_frame)
        self.add_button=ttk.Button(self.edit_options_frame,text="Add",command=self.add_teacher1)
        self.edit_button=ttk.Button(self.edit_options_frame,text="Edit",command=self.edit_teacher1)
        self.delete_button=ttk.Button(self.edit_options_frame,text="Delete",command=self.delete_teacher)

        self.edit_teachers_done_button=ttk.Button(self.edit_options_frame,text="Done",command=self.edit_teachers_done)

    def edit_teachers(self):

        edit_teachers_frame.pack()
        self.teacher_list_frame.grid(column=0,row=0)
        for i in range(len(self.new_teacher_list)):
            self.teacher_listbox.insert(tk.END,self.new_teacher_list[i])
        self.teacher_listbox.select_set(0)
        self.teacher_listbox.pack(side='left')
        self.teacher_list_scrollbar.pack(side='right',fill='y')
        self.edit_options_frame.grid(column=1,row=0)
        self.add_button.pack()
        self.edit_button.pack()
        self.delete_button.pack()
        self.edit_teachers_done_button.pack()

        menubutton.pack()

    def add_teacher1(self):

        # preparing window
        self.add_window=tk.Tk()
        self.add_window.attributes('-topmost',True)
        self.add_window.protocol("WM_DELETE_WINDOW",lambda a=self.add_window: enable_main_window(a))
        root.attributes('-disable',True)

        # content
        tk.Label(self.add_window,text="Name:").pack(side='left')
        teacher_name=ttk.Entry(self.add_window)
        teacher_name.pack(side='left')
        add_teacher_done=ttk.Button(self.add_window,text="Save",command=lambda a=teacher_name:self.add_teacher2(a))
        add_teacher_done.pack(side='right')

        # centralize window
        self.add_win_w=300
        self.add_win_h=100
        self.center_x=int(screen_w/2-self.add_win_w/2)
        self.center_y=int(screen_h/2-self.add_win_h/2)
        self.add_window.geometry(f"{self.add_win_w}x{self.add_win_h}+{self.center_x}+{self.center_y}")

        # focus and run window
        teacher_name.focus_force()
        self.add_window.mainloop()

    def add_teacher2(self,teacher_name):

        # conditions
        if teacher_name.get()=="":
            messagebox.showerror(title="Error",message="Can't be empty!",parent=self.add_window)
        elif teacher_name.get() in self.new_teacher_list:
            messagebox.showerror(title="Error",message="Already used!",parent=self.add_window)
        else:
            self.teacher_listbox.insert(0,teacher_name.get())
            self.new_teacher_list.insert(0,teacher_name.get())
            self.teacher_listbox.selection_clear(0,tk.END)
            self.teacher_listbox.select_set(0)
            enable_main_window(self.add_window)
        print("new",self.new_teacher_list)
        print(teacher_list)

    def edit_teacher1(self):

        # preparing window
        self.edit_window=tk.Tk()
        self.edit_window.attributes('-topmost',True)
        self.edit_window.protocol("WM_DELETE_WINDOW",lambda a=self.edit_window: enable_main_window(a))
        root.attributes('-disable',True)

        # content
        tk.Label(self.edit_window,text="Name:").pack(side='left')
        teacher_name=ttk.Entry(self.edit_window)
        teacher_name.pack(side='left')
        teacher_index=self.teacher_listbox.curselection()[0]
        old_teacher_name=self.teacher_listbox.get(teacher_index)
        teacher_name.insert(0,old_teacher_name)
        edit_teacher_done=ttk.Button(self.edit_window,text="Save",command=lambda a=teacher_name,b=teacher_index,c=old_teacher_name:self.edit_teacher2(a,b,c))
        edit_teacher_done.pack(side='right')

        # centralize window
        self.edit_win_w=300
        self.edit_win_h=100
        self.center_x=int(screen_w/2-self.edit_win_w/2)
        self.center_y=int(screen_h/2-self.edit_win_h/2)
        self.edit_window.geometry(f"{self.edit_win_w}x{self.edit_win_h}+{self.center_x}+{self.center_y}")

        # focus and run window
        teacher_name.focus_force()
        self.edit_window.mainloop()

    def edit_teacher2(self,teacher_name,teacher_index,old_teacher_name):

        teacher_name=teacher_name.get()

        # conditions
        if teacher_name=="":
            messagebox.showerror(title="Error",message="Can't be empty!",parent=self.edit_window)
        elif teacher_name in self.new_teacher_list and teacher_name!=old_teacher_name:
            messagebox.showerror(title="Error",message="Already used!",parent=self.edit_window)
        else:
            self.teacher_listbox.delete(teacher_index)
            self.teacher_listbox.insert(teacher_index,teacher_name)
            self.new_teacher_list[teacher_index]=teacher_name
            self.teacher_listbox.selection_clear(0,tk.END)
            self.teacher_listbox.select_set(teacher_index)
            enable_main_window(self.edit_window)

    def delete_teacher(self):

        teacher_index=self.teacher_listbox.curselection()[0]
        opt=messagebox.askokcancel(title="",message="Delete? All data associated with it will be erased!")
        if opt:
            self.teacher_listbox.delete(teacher_index)
            self.new_teacher_list.pop(teacher_index)

    def edit_teachers_done(self):
        
        teacher_list=list(self.new_teacher_list)
        f=open("files//teachers.csv","w",newline="")
        fo=csv.writer(f)
        for i in teacher_list:
            fo.writerow([i])
        f.close()
        edit_teachers_frame.destroy()
        global is_editing_teachers
        is_editing_teachers=False
        show_menu()


# ---------- Edit subjects ----------

def edit_subjects():

    global is_editing_subjects
    is_editing_subjects=True

    global edit_subjects_frame
    menu_frame.pack_forget()
    edit_subjects_frame=tk.Frame(root)
    edit_subjects_frame.pack()
    global es
    es=editsubjects()
    es.edit_subjects()

class editsubjects:

    def __init__(self):

        self.new_subject_list=list(subject_list)
        global edit_subjects_frame
        self.subject_list_frame=tk.Frame(edit_subjects_frame)
        self.subject_list_scrollbar=ttk.Scrollbar(self.subject_list_frame)
        self.subject_listbox=tk.Listbox(self.subject_list_frame,yscrollcommand=self.subject_list_scrollbar.set)

        self.edit_options_frame=tk.Frame(edit_subjects_frame)
        self.add_button=ttk.Button(self.edit_options_frame,text="Add",command=self.add_subject1)
        self.edit_button=ttk.Button(self.edit_options_frame,text="Edit",command=self.edit_subject1)
        self.delete_button=ttk.Button(self.edit_options_frame,text="Delete",command=self.delete_subject)

        self.edit_subjects_done_button=ttk.Button(self.edit_options_frame,text="Done",command=self.edit_subjects_done)

    def edit_subjects(self):

        edit_subjects_frame.pack()
        self.subject_list_frame.grid(column=0,row=0)
        for i in range(len(self.new_subject_list)):
            self.subject_listbox.insert(tk.END,self.new_subject_list[i])
        self.subject_listbox.select_set(0)
        self.subject_listbox.pack(side='left')
        self.subject_list_scrollbar.pack(side='right',fill='y')
        self.edit_options_frame.grid(column=1,row=0)
        self.add_button.pack()
        self.edit_button.pack()
        self.delete_button.pack()
        self.edit_subjects_done_button.pack()

        menubutton.pack()

    def add_subject1(self):

        # preparing window
        self.add_window=tk.Tk()
        self.add_window.attributes('-topmost',True)
        self.add_window.protocol("WM_DELETE_WINDOW",lambda a=self.add_window: enable_main_window(a))
        root.attributes('-disable',True)

        # content
        tk.Label(self.add_window,text="Name:").pack(side='left')
        subject_name=ttk.Entry(self.add_window)
        subject_name.pack(side='left')
        add_subject_done=ttk.Button(self.add_window,text="Save",command=lambda a=subject_name:self.add_subject2(a))
        add_subject_done.pack(side='right')

        # centralize window
        self.add_win_w=300
        self.add_win_h=100
        self.center_x=int(screen_w/2-self.add_win_w/2)
        self.center_y=int(screen_h/2-self.add_win_h/2)
        self.add_window.geometry(f"{self.add_win_w}x{self.add_win_h}+{self.center_x}+{self.center_y}")

        # focus and run window
        subject_name.focus_force()
        self.add_window.mainloop()

    def add_subject2(self,subject_name):

        # conditions
        if subject_name.get()=="":
            messagebox.showerror(title="Error",message="Can't be empty!",parent=self.add_window)
        elif subject_name.get() in self.new_subject_list:
            messagebox.showerror(title="Error",message="Already used!",parent=self.add_window)
        else:
            self.subject_listbox.insert(0,subject_name.get())
            self.new_subject_list.insert(0,subject_name.get())
            self.subject_listbox.selection_clear(0,tk.END)
            self.subject_listbox.select_set(0)
            enable_main_window(self.add_window)

    def edit_subject1(self):

        # preparing window
        self.edit_window=tk.Tk()
        self.edit_window.attributes('-topmost',True)
        self.edit_window.protocol("WM_DELETE_WINDOW",lambda a=self.edit_window: enable_main_window(a))
        root.attributes('-disable',True)

        # content
        tk.Label(self.edit_window,text="Name:").pack(side='left')
        subject_name=ttk.Entry(self.edit_window)
        subject_name.pack(side='left')
        subject_index=self.subject_listbox.curselection()[0]
        old_subject_name=self.subject_listbox.get(subject_index)
        subject_name.insert(0,old_subject_name)
        edit_subject_done=ttk.Button(self.edit_window,text="Save",command=lambda a=subject_name,b=subject_index,c=old_subject_name:self.edit_subject2(a,b,c))
        edit_subject_done.pack(side='right')

        # centralize window
        self.edit_win_w=300
        self.edit_win_h=100
        self.center_x=int(screen_w/2-self.edit_win_w/2)
        self.center_y=int(screen_h/2-self.edit_win_h/2)
        self.edit_window.geometry(f"{self.edit_win_w}x{self.edit_win_h}+{self.center_x}+{self.center_y}")

        # focus and run window
        subject_name.focus_force()
        self.edit_window.mainloop()

    def edit_subject2(self,subject_name,subject_index,old_subject_name):

        subject_name=subject_name.get()

        # conditions
        if subject_name=="":
            messagebox.showerror(title="Error",message="Can't be empty!",parent=self.edit_window)
        elif subject_name in self.new_subject_list and subject_name!=old_subject_name:
            messagebox.showerror(title="Error",message="Already used!",parent=self.edit_window)
        else:
            self.subject_listbox.delete(subject_index)
            self.subject_listbox.insert(subject_index,subject_name)
            self.new_subject_list[subject_index]=subject_name
            self.subject_listbox.selection_clear(0,tk.END)
            self.subject_listbox.select_set(subject_index)
            enable_main_window(self.edit_window)

    def delete_subject(self):

        subject_index=self.subject_listbox.curselection()[0]
        opt=messagebox.askokcancel(title="",message="Delete? All data associated with it will be erased!")
        if opt:
            self.subject_listbox.delete(subject_index)
            self.new_subject_list.pop(subject_index)

    def edit_subjects_done(self):

        subject_list=list(self.new_subject_list)
        f=open("files//subjects.csv","w",newline="")
        fo=csv.writer(f)
        for i in subject_list:
            fo.writerow([i])
        f.close()
        edit_subjects_frame.destroy()
        global is_editing_subjects
        is_editing_subjects=False
        show_menu()


# for extra windows being created
def enable_main_window(win):

    root.attributes('-disable',False)
    win.destroy()


# ---------- Window ----------

root=tk.Tk()
style=ttk.Style()
root.title("Time Table Management")
# root.iconbitmap(default="Software icon.ico")

# centering the window
win_w=1215
win_h=500
screen_w=root.winfo_screenwidth()
screen_h=root.winfo_screenheight()
center_x=int(screen_w/2-win_w/2)
center_y=int(screen_h/2-win_h/2)
root.geometry(f'{win_w}x{win_h}+{center_x}+{center_y}')
root.minsize(win_w,win_h)


# ---------- Variables ----------

days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
roman_count=('0','I','II','III','IV','V','VI','VII','VIII','IX','X')
subject_teachers={
    "S1":["T2","T3","T4"],
    "S2":["T3","T8","T4"],
    "S3":["T5","T3","T4"],
    "S4":["T8","T3","T4"],
    "S5":["T2","T3","T4"],
    "S6":["T8","T3","T4"],
    "S7":["T8","T3","T4"],
    "S8":["T4","T3","T4"],
}


# ---------- Auto Setup ----------
    
# preparing classes list
class_list=[]
try:
    f=open("files//classes.csv","r",newline="")
    fo=csv.reader(f)
    for i in fo:
        class_list.append(i[0])
except:
    f=open("files//classes.csv","w",newline="")
f.close()

# preparing teachers list
teacher_list=[]
try:
    f=open("files//teachers.csv","r",newline="")
    fo=csv.reader(f)
    for i in fo:
        teacher_list.append(i[0])
except:
    f=open("files//teachers.csv","w",newline="")
f.close()

# preparing subject list
subject_list=[]
try:
    f=open("files//subjects.csv","r",newline="")
    fo=csv.reader(f)
    for i in fo:
        subject_list.append(i[0])
except:
    f=open("files//subjects.csv","w",newline="")
f.close()

# number of periods
try:
    f=open("files//values.txt","r")
    title_name=f.readline()[6:]
    n_periods=int(f.readline()[8])
except:
    f=open("files//values.txt","w")
    f.write("title:\nperiods:8\n")
    n_periods=8
f.close()

# preparing presets
if "regular" not in os.listdir():
    path=os.path.join(os.getcwd(),"regular")
    os.mkdir(path)
for i in days:
    try:
        f=open(f".\\regular\\{i}.csv","r",newline="")
    except:
        f=open(f".\\regular\\{i}.csv","w",newline="")
        fo=csv.writer(f)
        for j in class_list:
            fo.writerow([j]+[""]*n_periods)
            fo.writerow([""]*(n_periods+1))
    f.close()


# ---------- Main Menu ----------

menu_frame=tk.Frame(root)
menu_frame.pack()

# buttons/options
createbutton=ttk.Button(menu_frame,text="Create",command=create_tt)
createbutton.grid(column=1,row=1,pady=20)
edit_teachers_button=ttk.Button(menu_frame,text="Teachers",command=edit_teachers)
edit_teachers_button.grid(column=0,row=2)
edit_classes_button=ttk.Button(menu_frame,text="Classes",command=edit_classes)
edit_classes_button.grid(column=1,row=2)
edit_subjects_button=ttk.Button(menu_frame,text="Subjects",command=edit_subjects)
edit_subjects_button.grid(column=2,row=2)
create_general_button=ttk.Button(menu_frame,text="Regular",command=create_general)
create_general_button.grid(column=1,row=3)

# menubutton
menubutton=ttk.Button(root,text="Menu",command=show_menu)

# ----- All frames/pages
selection_frame=tk.Frame(root)
tt_creation_frame=tk.Frame(root)
regular_tt_frame=tk.Frame(root)
edit_classes_frame=tk.Frame(root)
edit_teachers_frame=tk.Frame(root)
edit_subjects_frame=tk.Frame(root)

# to solve undefined error switching to main menu
is_editing_classes=False
is_editing_teachers=False
is_editing_subjects=False
is_creating_general=False
is_creating_tt=False

# starting the window
root.mainloop()