from flask import *
from multiprocessing import Process
from tkinter import Button,Label,Entry,Tk
import os, requests,shutil
from datetime import datetime

app = Flask(__name__)

win_list=[]

if "Manufacturers_cache_pending" not in os.listdir():
	os.mkdir("Manufacturers_cache_pending")
if "Manufacturers_cache_history" not in os.listdir():
	os.mkdir("Manufacturers_cache_history")
def rndm():
	return str(datetime.now()).replace(":","").replace(".","").replace("-","").replace(" ","")

@app.route("/", methods=["POST"])
def a():
	c=rndm()
	os.mkdir(f"Manufacturers_cache_pending/{c}")
	w = [request.json["volume_of_product"],request.json["number_of_sold"],request.json["address"],request.json["cost_of_order"]]
	open(f"Manufacturers_cache_pending/{c}/data.txt","a").write(f"{w[0]}\n{w[1]}\n{w[2]}\n{w[3]}")
	return "ok"

def mark_as_delivered(path,n,directory):
	if "pending" in path:
		shutil.copytree(f"{path}/{directory}",f"Manufacturers_cache_history/{directory}")
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
			if "pending" in path:
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
			if "pending" in path:
				Button(text="Mark as delivered", background="green", foreground="white", command=lambda:mark_as_delivered(path,n,p[o-1])).place(x=10,y=p_y+80)
			data_t = open(f"{path}/{p[o]}/data.txt","r").read().split("\n")
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
	win.title("Manufacturers - history")
	win.geometry("400x500+20+20")
	if (n == 1):
		back_state = "disabled"
	else:
		back_state= "active"
	if (n*4 > len(os.listdir("Manufacturers_cache_history")) or n*4 == len(os.listdir("Manufacturers_cache_history"))):
		forward_state="disabled"
	else:
		forward_state = "active"
	Button(win, text="Home", background="green", relief="raised", foreground="white", command=main).place(x=0,y=0)
	Button(win, text="back", background="green", relief="raised", foreground="white", state=back_state, command=lambda:order_history(n-1)).place(x=100,y=0)
	Button(win, text="forward", background="green", relief="raised", foreground="white", state=forward_state, command=lambda:order_history(n+1)).place(x=150,y=0)
	show_list("Manufacturers_cache_history",n)

def order_pending(n):
	win_list[0].destroy()
	win_list.remove(win_list[0])
	win = Tk()
	win_list.append(win)
	win.title("Manufacturers - pending")
	win.geometry("400x500+20+20")
	if (n == 1):
		back_state = "disabled"
	else:
		back_state= "active"
	if (n*4 > len(os.listdir("Manufacturers_cache_pending")) or n*4 == len(os.listdir("Manufacturers_cache_pending"))):
		forward_state="disabled"
	else:
		forward_state = "active"
	Button(win, text="Home", background="green", relief="raised", foreground="white", command=main).place(x=0,y=0)
	Button(win, text="back", background="green", relief="raised", foreground="white", state=back_state, command=lambda:order_pending(n-1)).place(x=100,y=0)
	Button(win, text="forward", background="green", relief="raised", foreground="white", state=forward_state, command=lambda:order_pending(n+1)).place(x=150,y=0)
	show_list("Manufacturers_cache_pending",n)

def main():
	if (len(win_list) != 0):
		win_list[0].destroy()
		win_list.remove(win_list[0])
	window=Tk()
	win_list.append(window)
	window.title("Company - Manufacturers")
	window.geometry("300x100+20+20")
	Button(window, text="Order history", background="green", relief="raised", foreground="white", command=lambda:order_history(1)).place(x=10,y=10)
	Button(window, text="Order pending", background="green", relief="raised", foreground="white", command=lambda:order_pending(1)).place(x=10,y=50)
	window.mainloop()

def server():
	app.run(host="localhost", port="9080")

if __name__ == '__main__':
	t = [Process(target=server), Process(target=main)]
	t[0].start()
	t[1].start()
	t[1].join()