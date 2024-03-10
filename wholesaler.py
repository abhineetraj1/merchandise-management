from flask import *
from multiprocessing import Process
from tkinter import Button,Label,Entry,Tk, messagebox
import os,requests
from datetime import datetime
import shutil

app = Flask(__name__)

win_list=[]

if "wholesaler_cache_pending" not in os.listdir():
	os.mkdir("wholesaler_cache_pending")
if "wholesaler_cache_history" not in os.listdir():
	os.mkdir("wholesaler_cache_history")
def rndm():
	return str(datetime.now()).replace(":","").replace(".","").replace("-","").replace(" ","")

@app.route("/", methods=["POST"])
def a():
	w = [request.json["volume_of_product"],request.json["number_of_sold"],request.json["address"],request.json["cost_of_order"]]
	fg_name=rndm()
	os.mkdir(f"wholesaler_cache_pending/{fg_name}")
	open(f"wholesaler_cache_pending/{fg_name}/data.txt","a").write(f"{w[0]}\n{w[1]}\n{w[2]}\n{w[3]}")
	return "ok"

def mark_as_delivered(path,n,directory):
	if "pending" in path:
		shutil.rmtree(f"{path}/{directory}")
		order_pending(n)
	else:
		order_history(n)

def show_list(path, n):
	p = os.listdir(path)
	if (n*4 < len(os.listdir(path))):
		o=(n*4 - 4)
		p_y=70
		while o != n*4:
			Label(text="Volume of product required: ").place(x=10,y=p_y)
			Label(text="Number of product sold: ").place(x=10,y=p_y+20)
			Label(text="Delivery address: ").place(x=10,y=p_y+40)
			Label(text="Cost of order: ").place(x=10,y=p_y+60)
			data_t = open(f"{path}/{p[o]}/data.txt","r").read().split("\n")
			if "wholesaler_cache_pending" == path:
				Button(text="Mark as delivered", background="green", foreground="white", command=lambda:mark_as_delivered(path,n,p[o-1])).place(x=10,y=p_y+80)
			Label(text=data_t[0]).place(x=160,y=p_y)
			Label(text=data_t[1]).place(x=160,y=p_y+20)
			Label(text=data_t[2]).place(x=160,y=p_y+40)
			Label(text=data_t[3]).place(x=160,y=p_y+60)
			p_y=p_y+110
			o=o+1
	else:
		o, lt=(n*4 - 4),[]
		p_y=70
		while o != len(os.listdir(path)):
			Label(text="Volume of product required: ").place(x=10,y=p_y)
			Label(text="Number of product sold: ").place(x=10,y=p_y+20)
			Label(text="Delivery address: ").place(x=10,y=p_y+40)
			Label(text="Cost of order: ").place(x=10,y=p_y+60)
			data_t = open(f"{path}/{p[o]}/data.txt","r").read().split("\n")
			if "wholesaler_cache_pending" == path:
				Button(text="Mark as delivered", background="green", foreground="white", command=lambda:mark_as_delivered(path,n,p[o-1])).place(x=10,y=p_y+80)
			Label(text=data_t[0]).place(x=160,y=p_y)
			Label(text=data_t[1]).place(x=160,y=p_y+20)
			Label(text=data_t[2]).place(x=160,y=p_y+40)
			Label(text=data_t[3]).place(x=160,y=p_y+60)
			p_y=p_y+100
			o=o+1
def order_history(n):
	win_list[0].destroy()
	win_list.remove(win_list[0])
	win = Tk()
	win_list.append(win)
	win.title("Wholesaler - history")
	win.geometry("400x500+20+20")
	if (n == 1):
		back_state = "disabled"
	else:
		back_state= "active"
	if (n*4 > len(os.listdir("wholesaler_cache_history")) or n*4 == len(os.listdir("wholesaler_cache_history"))):
		forward_state="disabled"
	else:
		forward_state = "active"
	Button(win, text="Home", background="green", relief="raised", foreground="white", command=main).place(x=0,y=0)
	Button(win, text="back", background="green", relief="raised", foreground="white", state=back_state, command=lambda:order_history(n-1)).place(x=100,y=0)
	Button(win, text="forward", background="green", relief="raised", foreground="white", state=forward_state, command=lambda:order_history(n+1)).place(x=150,y=0)
	show_list("wholesaler_cache_history",n)

def order_pending(n):
	win_list[0].destroy()
	win_list.remove(win_list[0])
	win = Tk()
	win_list.append(win)
	win.title("Wholesaler - pending")
	win.geometry("400x500+20+20")
	if (n == 1):
		back_state = "disabled"
	else:
		back_state= "active"
	if (n*4 > len(os.listdir("wholesaler_cache_pending")) or n*4 == len(os.listdir("wholesaler_cache_pending"))):
		forward_state="disabled"
	else:
		forward_state = "active"
	Button(win, text="Home", background="green", relief="raised", foreground="white", command=main).place(x=0,y=0)
	Button(win, text="back", background="green", relief="raised", foreground="white", state=back_state, command=lambda:order_pending(n-1)).place(x=100,y=0)
	Button(win, text="forward", background="green", relief="raised", foreground="white", state=forward_state, command=lambda:order_pending(n+1)).place(x=150,y=0)
	show_list("wholesaler_cache_pending",n)

def main():
	if (len(win_list) != 0):
		win_list[0].destroy()
		win_list.remove(win_list[0])
	def order_now():
		json = {"volume_of_product":t[0].get(),"number_of_sold":t[1].get(),"address":t[2].get(),"cost_of_order":t[3].get()}
		sent_request=requests.post("http://localhost:9080/", json=json, headers={"Content-Type": "application/json"})
		if sent_request.content.decode("utf-8") == "ok":
			fg_name=rndm()
			os.mkdir(f"wholesaler_cache_history/{fg_name}")
			open(f"wholesaler_cache_history/{fg_name}/data.txt","a").write(f"{t[0].get()}\n{t[1].get()}\n{t[2].get()}\n{t[3].get()}")
			messagebox.showinfo("Success","Order sent!")
		else:
			messagebox.showerror("Error","Failed to send order")
	window=Tk()
	win_list.append(window)
	window.title("Company - Wholesaler")
	window.geometry("300x300+20+20")
	t = [Entry(window, bd=5),Entry(window, bd=5),Entry(window, bd=5),Entry(window, bd=5)]
	t[0].place(x=150,y=0)
	t[1].place(x=150,y=50)
	t[2].place(x=150,y=100)
	t[3].place(x=150,y=150)
	Label(window, text="Enter volume of product").place(x=0,y=0)
	Label(window, text="Number of sold product").place(x=0,y=50)
	Label(window, text="Delivery address").place(x=0,y=100)
	Label(window, text="Total cost of order").place(x=0,y=150)
	Button(window, text="Order now", background="green", relief="raised", foreground="white", command=order_now).place(x=0,y=200)
	Button(window, text="Order history", background="green", relief="raised", foreground="white", command=lambda:order_history(1)).place(x=70,y=200)
	Button(window, text="Order pending", background="green", relief="raised", foreground="white", command=lambda:order_pending(1)).place(x=150,y=200)
	window.mainloop()

def server():
	app.run(host="localhost", port="8080")

if __name__ == '__main__':
	t = [Process(target=server), Process(target=main)]
	t[0].start()
	t[1].start()
	t[1].join()