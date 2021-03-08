import tkinter as tk
from client import Client
from tkinter import scrolledtext


class ClientApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Conversation):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Connexion : " , fg="#145A32").grid(row=0, column=0)
        self.controller = controller
        
        tk.Label(self, text="username:", fg="#145A32").grid(row=1, column=0)
        tk.Label(self, text="server:" , fg="#145A32").grid(row=2, column=0)
        tk.Label(self, text="port:", fg="#145A32").grid(row=3, column=0)

        self.entryUsername = tk.Entry(self,width=30, font=1, fg="#145A32")
        self.entryUsername.grid(row=1, column=1, pady=10)
        self.entryServer = tk.Entry(self,width=30, font=1, fg="#145A32")
        self.entryServer.grid(row=2, column=1, pady=10)
        self.entryPort = tk.Entry(self,width=30, font=1, fg="#145A32")
        self.entryPort.grid(row=3, column=1, pady=10)
        button = tk.Button(self, text="valider",width=20,bg="#145A32", fg="white", command=lambda: self.validateConfig({
            'username': self.entryUsername.get(),
            'server': self.entryServer.get(),
            'port': int(self.entryPort.get())
        }))
        button.grid(row=4, column=0, columnspan=2, pady=50)

    def validateConfig(self, data):
        self.controller.frames['Conversation'].receive_data(data)
        self.controller.show_frame("Conversation")


class Conversation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Conversation", fg="#145A32", width=40, pady=10, font=20).grid(row=0, column=0)
        self.controller = controller
        self.messages = scrolledtext.ScrolledText(self, width=50)
        self.messages.grid(row=1, column=0, padx=10, pady=10)

        self.entryMessage = tk.Entry(self, width=30, font=1,fg="#145A32")
        self.entryMessage.insert(0, "Message")
        self.entryMessage.grid(row=2, column=0, padx=10, pady=30)

        def send_message():
            clientMessage = self.entryMessage.get()
            self.client.send(clientMessage)

        btnSendMessage = tk.Button(self, text="Envoyer", width=20,bg="#145A32", fg="white", command=send_message)
        btnSendMessage.grid(row=3, column=0, padx=10, pady=30)

    def receive_data(self, data):
        self.client = Client(data['username'], data['server'], data['port'])
        self.client.listen(self.handle)

    def handle(self, data):
        self.messages.insert(tk.END, data + '\n', 'message')

if __name__ == '__main__':
    ClientApp().mainloop()
