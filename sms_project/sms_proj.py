from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import requests
import bs4
import matplotlib.pyplot as plt

def f1():
	add_window.deiconify()
	main_window.withdraw()
def f2():
	main_window.deiconify()
	add_window.withdraw()
def f3():
	vw_st_data.delete(1.0, END)
	view_window.deiconify()
	main_window.withdraw()
	info = ""
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "rno = " + str(d[0]) + "   name = " + str(d[1]) + "   marks = " + str(d[2]) + "\n"
		vw_st_data.insert(INSERT, info)
	
	except Exception as e:
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
def f4():
	main_window.deiconify()
	view_window.withdraw()
def f5():
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "insert into student values('%d', '%s', '%d')"
		rno = int(aw_ent_rno.get())
		name = aw_ent_name.get()
		marks = int(aw_ent_marks.get())
		cursor.execute(sql % (rno, name, marks))
		if rno < 0:
			showerror("Error", 'Only positive integers!')
		elif rno == 0:
			showerror("Error", 'you must enter a rno')
		
		elif (len(name)<2):
			showerror("Error", 'you must enter a name with more than 1 letter')
		elif not name.isalpha():
			showerror("Error", 'Alphabets only!')
		elif marks < 0 or marks > 100:
			showerror("Out of Range", 'Marks must be in the range of 0-100')
		else:
			con.commit()
			showinfo("Success!", 'Record Added')
		aw_ent_rno.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_marks.delete(0, END)
		aw_ent_rno.focus()
	except ValueError:
		showerror("Error", 'Integers only!')
	except Exception as e:
		con.rollback()
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
def f6():
	update_window.deiconify()
	main_window.withdraw()
	
def f7():
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "update student set name = '%s', marks = '%d' where rno = '%d' "
		name = uw_ent_name.get()
		rno = int(uw_ent_rno.get())
		marks = int(uw_ent_marks.get())
		cursor.execute(sql % (name, marks, rno))
		if rno < 0:
			showerror("Error", 'Rno must be positive')
		
		elif rno == 0:
			showerror("Error", 'Enter rno')
		elif (len(name)<2):
			showerror("Error", 'Name must contain atleast two alphabets')
		elif not name.isalpha():
			showerror("Error", 'Name must contain only alphabets')
		elif marks < 0 or marks > 100:
			showerror("Error", 'Marks should be in range 0-100')
		elif cursor.rowcount == 1:
			con.commit()
			showinfo("Success!", 'Record Updated')
			
		else:
			showerror("Failure!", 'Record not Updated')
		uw_ent_name.delete(0, END)
		uw_ent_rno.delete(0, END)
		uw_ent_marks.delete(0, END)
		uw_ent_rno.focus()
	except ValueError:
		showerror("Error", 'Integers only!')
	except Exception as e:
		showerror("Issue", e)
		con.rollback()
		
	finally:
		if con is not None:
			con.close()
def f8():
	main_window.deiconify()
	update_window.withdraw()
def f9():
	delete_window.deiconify()
	main_window.withdraw()
def f10():
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "delete from student where rno = '%d'"
		rno = int(dw_ent_rno.get())
		cursor.execute(sql % (rno))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Success!", 'Record Deleted')	
			dw_ent_rno.delete(0, END)
		
		else:
			showerror("Failure","record does not exist")
			dw_ent_rno.delete(0, END)
	except ValueError:
		showerror("Error", 'Integers only!')	
	except Exception as e:
		showerror("Issue ", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
def f11():
	main_window.deiconify()
	delete_window.withdraw()

try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)
	data = res.json()
	city_name = data['city']
	state_name = data['region']	
except Exception as e:
	showerror("issue ", e)


try:
	city =city_name
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city
	a3 = "&appid=" + "29bcd924eb41cd2ecd07fbfa267e2f6f"
	wa = a1 + a2 + a3
	res = requests.get(wa)
	data = res.json()
	temp = data['main']['temp']
except Exception as e:
	showerror("Issue", e)

try:
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	data = bs4.BeautifulSoup(res.text, "html.parser")
	info = data.find("img",{"class":"p-qotd"})
	msg = info['alt']
except Exception as e:
	showerror("Issue", e)	


def charts():
	con = connect("sms.db")
	cursor = con.cursor()
	cursor.execute("select name,marks from student")
	name = []
	marks = []
	for row in cursor.fetchall():
		name.append(row[0])
		marks.append(row[1])	
	
	plt.bar(name, [int(x) for x in marks], color=['pink', 'skyblue', 'lavender'])
	plt.xlabel("Names")
	plt.ylabel("Marks")
	plt.title("Batch Information")
	plt.show()


f = ("Calibri", 21, "bold")
main_window = Tk()
main_window['bg'] = 'DarkSeaGreen2'
main_window.geometry("700x600+400+100")
main_window.title(" S.M.S ")

mw_btn_add = Button(main_window, text="Add", width=10, font=f, fg="black", bg="white",command=f1)
mw_btn_view = Button(main_window, text="View", width=10, font=f,fg="black", bg="white",command=f3)

mw_btn_update = Button(main_window, text="Update", width=10, font=f,fg="black", bg="white",command=f6)
mw_btn_delete = Button(main_window, text="Delete", width=10, font=f,fg="black", bg="white",command=f9)
mw_btn_charts = Button(main_window, text="Charts", width=10, font=f,fg="black", bg="white", command=charts)
mw_btn_add.pack(pady=8)
mw_btn_view.pack(pady=8)
mw_btn_update.pack(pady=8)
mw_btn_delete.pack(pady=8)
mw_btn_charts.pack(pady=8)




add_window = Toplevel(main_window)
add_window['bg'] = 'thistle1'
add_window.geometry("600x600+400+100")
add_window.title("Add Student")

aw_lbl_rno = Label(add_window, text ="Enter rno: ", font=f, fg="white", bg="thistle4")
aw_lbl_rno.pack()
aw_ent_rno = Entry(add_window, bd=8, font=f)
aw_ent_rno.pack()
aw_lbl_name = Label(add_window, text="Enter Name:", font=f, fg="white", bg="thistle4")
aw_lbl_name.pack()
aw_ent_name = Entry(add_window, bd=8, font=f)
aw_ent_name.pack()
aw_lbl_marks = Label(add_window, text="Enter Marks:", font=f, fg="white", bg="thistle4")
aw_lbl_marks.pack()
aw_ent_marks = Entry(add_window, bd=8, font=f)
aw_ent_marks.pack()

aw_btn_save = Button(add_window, text="Save", font=f, command=f5, fg="white", bg="thistle4")
aw_btn_back = Button(add_window, text="Back", font=f, command=f2, fg="white", bg="thistle4")
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)
add_window.withdraw()


view_window = Toplevel(main_window)
view_window['bg'] = 'wheat1'
view_window.geometry("600x600+400+100")
view_window.title("View Student")


vw_st_data = ScrolledText(view_window, width=30, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font=f, command=f4, fg="black", bg="white")
vw_st_data.pack()
vw_btn_back.pack(pady=21)
view_window.withdraw()


update_window = Toplevel(main_window)
update_window['bg'] = 'azure2'
update_window.geometry("600x600+400+100")
update_window.title("Update Student")

uw_lbl_rno = Label(update_window, text ="Enter rno: ", font=f, fg="black", bg="pink")
uw_lbl_rno.pack()
uw_ent_rno = Entry(update_window, bd=8, font=f)
uw_ent_rno.pack()
uw_lbl_name = Label(update_window, text="Enter Name:", font=f, fg="black", bg="pink")
uw_lbl_name.pack()
uw_ent_name = Entry(update_window, bd=8, font=f)
uw_ent_name.pack()
uw_lbl_marks = Label(update_window, text="Enter Marks:", font=f, fg="Black", bg="pink")
uw_lbl_marks.pack()
uw_ent_marks = Entry(update_window, bd=8, font=f)
uw_ent_marks.pack()

uw_btn_save = Button(update_window, text="Save", font=f, command=f7, fg="black", bg="pink")
uw_btn_back = Button(update_window, text="Back", font=f, command=f8, fg="black", bg="pink")
uw_btn_save.pack(pady=10)
uw_btn_back.pack(pady=10)
update_window.withdraw()

delete_window = Toplevel(main_window)
delete_window['bg'] = 'seashell2'
delete_window.geometry("600x600+400+100")
delete_window.title("Delete Student")

dw_lbl_rno = Label(delete_window, text ="Enter rno: ", font=f, fg="black", bg="white")
dw_lbl_rno.pack()
dw_ent_rno = Entry(delete_window, bd=8, font=f)
dw_ent_rno.pack()

dw_btn_save = Button(delete_window, text="Save", font=f, command=f10, fg="black", bg="white")
dw_btn_back = Button(delete_window, text="Back", font=f, command=f11, fg="black", bg="white")
dw_btn_save.pack(pady=10)
dw_btn_back.pack(pady=10)
delete_window.withdraw()


lbl_loc = Label(main_window, text="Location:", width=9, font=f, height = 1, fg="black", bg="white").place(x=4, y=420)
lbl_loc2 = Label(main_window, text=city_name, 
width=9, font=f, height =1, fg="black", bg="white").place(x=134, y=420)

lbl_temp = Label(main_window, text="Temperature:", width=11, height=1, font=f, fg="black", bg="white").place(x=444, y=420)
lbl_temp2 = Label(main_window, text=temp, width=5, height=1, font=f, fg="black", bg="white").place(x=615, y=420)


lbl_qotd = Label(main_window, text="QOTD:", width=9, height=0, font=("Calibri", 19, "bold italic"), fg="black", bg="white").place(x = 5, y=500)
lbl_qotd2 = Label(main_window, text=msg, width=60, font=("Calibri",19,"bold italic"),fg="black",bg="white").place(x=104,y=550)




main_window.mainloop()