import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import el_gamal
HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#485460'
MEDIUM_GREY = '#1e272e'
OCEAN_BLUE = '#60a3bc'
q= []
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


# tạo môt đối tượng socket sử dụng ipv4 và giao thức truyền tin TCP

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# hàm sau thực hiện thêm tin nhắn vào trong box chat. và các in nhắn thêm vào sẽ được xuống dòng
def add_message(message):
    message_box.config(state=tk.NORMAL)#cho phep click nhập
    message_box.insert(tk.END, message + '\n')#them vao cuoi tin nhan vai xuong dong 
    message_box.config(state=tk.DISABLED)#vo hieu hóa (ẩn) thẻ  

def connect():

    # try except block
    try:
        # Connect to the server
        client.connect((HOST, PORT))#client kêt noi cong và port

        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")#hien thi trên giai dien
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")
        #thong bao lỗi ra giao diên
    username = username_textbox.get()#bien lây tên user từ giao diên
    if username != '':
        client.sendall(username.encode())#mã hóa user name
        print("SEND : ", username.encode() )
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    #tk
    username_textbox.config(state=tk.DISABLED)#vo hiêu hoa sau khi nhap
    username_button.config(state=tk.DISABLED)
    username_button.pack_forget()
    username_textbox.pack_forget()#ẩn nút và ô
    username_label['text']= "Welcome " + username + " to our secure room"
    username_label.pack(side=tk.LEFT)#dẩy về vê bên trái màn hình

####here
def send_message():
    message = message_textbox.get()#lây tin nhăn từ giao diện
    if message != '':
        message_textbox.delete(0, len(message))#xoa noi message_box

        #encryption
        print("elgammel encryption")
        global messageCopy
        message = el_gamal.incrypt_gamal(int(elgamalkey[0]), int(elgamalkey[1]), int(elgamalkey[2]),message)
        #bien lấy mã hóa tin nhắn ở message_box
        messageCopy = message
            #cipher after encryption in var message
        # gui ban ma cho server
        client.sendall(message.encode("utf-8"))
        #gưi đên server 
        #print("SEND : ", message.encode() )
        
        print("Tin nhan da duoc chuyen di")
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


####here
def listen_for_messages_from_server(client):
    
    while 1:
        #nhận lại bản mã và khóa từ server
        message = client.recv(2048).decode('utf-8')
        print("RECV : ", message)
        #####
        if message != '':
            message = message.split("~")
            global key,elgamalkey

             
            username = message[0]
            content = message[1]#tin nhan
            key = message[2]#khoa phien
            elgamalkey = message[3]#khoa cong khai 
            elgamalkey = elgamalkey.split(",")

            #decrypt
            if username != "SERVER":

                print("elgamal decryption")
                print("content copy message=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==- ",content)
                content=el_gamal.decrept_gamal(content,int(elgamalkey[3]))#giải mã với message và khóa công khai elgamal
            else:
                print() 

            add_message(f"[{username} {key}] {content}") # thêm  message vào giao diên
                      
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")
    

          
root = tk.Tk()#tao cửa sổ
root.geometry("600x600")#Kich thước 
root.title("Messenger Client") #tiêu đề của cửa sổ
root.resizable(False, False)#không cho kéo dãn khung
#dinh dạng vị trị
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)#định dạng vị trị

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)
#tao the label (giong the h1,h2) 
username_label = tk.Label(top_frame, text="nhập tên sử dụng:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)# các khung 10px
#tao ô nhâp
username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)
#tao nut 
username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)
#tao o nhap textbox
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)
#tao nut 
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)
#hiêu thi tin nhan(dang con lan chuot)
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


# main function
def main():
    #print("CODE :", server.getMethod())
    root.mainloop()#xu ly su kien lien qua dên tk 
    
if __name__ == '__main__':
    main()