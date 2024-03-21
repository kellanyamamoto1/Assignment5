import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
from ds_messenger import *
import socket
import json
import Profile as prof
import pathlib
import time
timestamp = str(time.time())



class Body(tk.Frame):
    '''
    Body Class that Holds the Main Draw
    '''
    def __init__(self, root, recipient_selected_callback=None):
        '''
        Initilizes self
        '''
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        '''
         Select Node
        '''
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        '''
        Instert Function
        '''
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        '''
        Instert Contact Tree
        '''
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        '''
        Function to Insert User Message
        '''
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        '''
        Function to Insert Contact Message
        '''
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        '''
        Function to Get Text Entry
        '''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        '''
        Function to Set Text Entry
        '''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        '''
        Draw Function that Sets the Gui Variables
        '''
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, check_new_callback=None):
        '''
        Initilizes self
        '''
        tk.Frame.__init__(self, root)
        '''
        Initilizes self
        '''
        self.root = root
        self._send_callback = send_callback
        self._check_new_callback = check_new_callback
        self._draw()

    def send_click(self):
        '''
        Defines click button action
        '''
        if self._send_callback is not None:
            self._send_callback()

    def check_new_click(self):
        '''
        Defines New Check Action
        '''
        if self._check_new_callback is not None:
            self._check_new_callback()

    def enable_check_new_button(self):
        '''
        Enables new check
        '''
        self.check_new_button['state'] = tk.NORMAL

    def disable_check_new_button(self):
        '''
        Disables Check New
        '''
        self.check_new_button['state'] = tk.DISABLED

    def _draw(self):
        '''
        makes Function that Sets the Gui Variables
        '''
        save_button = tk.Button(master=self, text="Send",
                                width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.check_new_button = tk.Button(master=self, text="Check New",
                                          width=20,
                                          command=self.check_new_click)
        self.check_new_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        '''
        Initilizes self
        '''
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        '''
        Holds Main Variable assignments
        '''
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.pack()

        if self.server:
            self.server_entry.insert(tk.END, self.server)
        if self.user:
            self.username_entry.insert(tk.END, self.user)
        if self.pwd:
            self.password_entry.insert(tk.END, self.pwd)

    def apply(self):
        '''
        Function to Apply
        '''
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        '''
        Initilizes 
        '''
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.direct_messenger = None
        self._draw()
        self.body.insert_contact("test student")

    def send_message(self):
        '''
        Send Messages with Others
        '''
        message_txt = self.body.get_text_entry()
        if self.recipient and message_txt and self.direct_messenger:
            print("i got here")
            send_bool = self.direct_messenger.send(message=message_txt,
                                                   recipient=self.recipient)
            print("grapes")
            if send_bool:
                self.publish(f"You: {message_txt}")
            else:
                print("Could not send message.")
            self.body.set_text_entry('')

    def add_contact(self):
        '''
        Add Contact person
        '''
        temp1 = "Add Contact"
        temp2 = "Enter the name of the new contact:"
        contact_name = tk.simpledialog.askstring(temp1, temp2)
        if contact_name:
            self.body.insert_contact(contact_name)

    def recipient_selected(self, recipient):
        '''
        Select Recipient
        '''
        self.recipient = recipient

    def configure_server(self):
        '''
        Configure Server
        '''
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        if ud.user and ud.pwd and ud.server:
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server
            # You must implement this!
            # You must configure and instantiate your
            # DirectMessenger instance after this line.
            self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                    username=self.username,
                                                    password=self.password)
            print("igothere")

    def publish(self, message: str):
        '''
        Publish Message to GUI
        '''
        if "You:" in message:
            self.body.insert_user_message(message)
        else:
            self.body.insert_contact_message(message)

    def check_new(self):
        '''
        Check New messages
        '''
        if self.direct_messenger:
            new_messages = self.direct_messenger.retrieve_new()
            print(new_messages)
            for msg in new_messages:
                print(msg.recipient)
                print(msg.message)
                self.body.insert_contact_message(
                    f'{msg.recipient}: {msg.message}'
                    )
        self.after(2000, self.check_new)

    def _draw(self):
        '''
        Draw Function for Gui Variable Sets
        '''
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root,
                             send_callback=self.send_message,
                             check_new_callback=self.check_new)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def begin():
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("Bruh")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
