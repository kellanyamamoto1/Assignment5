from pathlib import Path
#import user as use
from Profile import Profile, Post
from ds_client import send

server_adress = "168.235.86.101"
server_port = "3021"
administrator = False
temp_path = ''




def user():
    user_type = input("Please input user type (\"admin\", \"user\"):  ")
    temp = 0
    if user_type == 'admin':
        temp = 1
    else:
        temp = 0
    return temp


def administration(a):
    global administrator
    if a == 1:
        administrator = True
    else:
        administrator = False
    return administrator


def comm():
    command = input("please enter command:  ")
    command_type = command[0:1]
    if command == 'admin':
        admin.start()
    else:
        if command_type == "L":
            list_files(command)
        elif command_type == "Q":
            quit()
        elif command_type == "C":
            create_file(command)
            comm()
        elif command_type == "D":
            del_file(command)
        elif command_type == "R":
            read_file(command)
        elif command_type == "H":
            use.comm_list()
            comm()
        elif command_type == "O":
            open_file(command)
            comm()
        elif command_type == 'E':
            edit_file(command)
        elif command_type == "P":
            print_data(command)


def file_sort(a, b):
    temp = [f for f in a if Path(b, f).is_file()]
    return temp


def dir(pathlib_path, path):
    temp = []
    fol = Path(path)
    for item in fol.iterdir():
        if item.is_dir():
            temp.append(item)
    return temp


def list_files(a):
    if administrator:
        paths = a.split(' ')
        if len(paths) > 1:
            path = paths[1]
            recursive = "-r" in paths[2:]
            files_only = "-f" in paths[2:]
            search_file = None
            if "-s" in paths[2:]:
                s_index = paths.index("-s")
                if s_index + 1 < len(paths):
                    search_file = paths[s_index + 1]
            ending = None
            if "-e" in paths[2:]:
                e_index = paths.index("-e")
                if e_index + 1 < len(paths):
                    ending = paths[e_index + 1]
            list_items(path, recursive, files_only, search_file, ending)
        else:
            if administrator:
                print("please enter a valid path")
                comm()
            else:
                use.path_help()
    else:
        path = use.get_path()
        recursive = use.recursive()
        files_only = use.files()
        ending = use.ending()
        search_file = use.search()
        print("OUTPUT:\n")
        list_items(path, recursive, files_only, search_file, ending)


def list_items(path, recursive=False, files_only=False, search_file=None, ending=None):
    try:
        l = Path(path).iterdir()
        
        files = file_sort(l, path)
        dirs = dir(l, path)

        for file in files:
            file_name, file_extension = file.stem, file.suffix
            file_extension = file_extension[1::]
            if search_file is None or search_file == file_name:
                if ending is None or file_extension.lower() == ending.lower():
                    print(file)

        if recursive:
            for directory in dirs:
                if not files_only and directory.is_dir():
                    if ending is not None:
                        list_items(directory, recursive, files_only, search_file, ending)
                    else:
                        print(directory)
                        list_items(directory, recursive, files_only, search_file, ending)
                elif files_only and directory.is_dir():
                    list_items(directory, recursive, files_only, search_file, ending)
        elif not files_only and ending is None:
            for directory in dirs:
                print(directory)
    except FileNotFoundError:
        print(f"the path {path} doesnt exist")
    comm()


def create_file(a):
    global temp_path
    if administrator:
        paths = a.split(' ')
        if len(paths) > 1:
            path = paths[1]
            if '-n' in paths[2:]:
                n_index = paths.index('-n')
                temp = n_index + 1
                file_name = paths[temp]
                file_ext = file_name + '.dsu'
                filepath = Path(path) / file_ext
                username = None
                password = None
                bio = None
                profile = Profile(username = username, password = password, bio = bio)
                with open(filepath,'a') as f:
                    print("")
                f = open(filepath,'a')
                profile.save_profile(path = filepath)
                print(f'{filepath} OPENED')
                temp_path = filepath
        print(f"this is the way  {temp_path}")
        return temp_path
                
    else:
        file_path = use.get_path()
        file_name = use.file_name()
        line = file_path + "\\" + file_name
        username = input("Enter Username:  ")
        password = input("Enter Password:  ")
        bio = input("Enter bio: ")
        profile = Profile(username = username, password = password, bio = bio)
        print(line + "      CREATED")
        with open(line, 'a') as f:
            a = "Username: " + username + '\n'
            f.write(a)
            b = "Password: " + password + '\n'
            f.write(b)
            c = "Bio: " + bio + '\n'
            f.write(c)
        profile.save_profile(path = line)
        f = open(line, 'a')
        temp_path = file_path
    print(f'{file_path} OPENED')
    print(f"this is the way  {file_path}")
    return temp_path


def check_file(a):
    if Path(a).exists():
        return True
    else:
        return False


def del_file(a):
    if administrator:
        paths = a.split(' ')
        path = paths[1]
        if path[-3:] == 'dsu':
            if check_file(path):
                Path(path).unlink()
                print(f"{path} DELETED")
            elif not check_file(path):
                print("no such file exists")
        else:
            print("can only delete dsu files")
    else:
        path = use.get_path()
        if path[-3:] == 'dsu':
            if check_file(path):
                Path(path).unlink()
                print(f"{path} DELETED")
            elif not check_file(path):
                print("no such file exists")
        else:
            print("can only delete dsu files")

    comm()


def read_file(a):
    if administrator:
        paths = a.split(' ')
        path = paths[1]
        if path[-3:] == 'dsu':
            if check_file(path):
                with open(path, 'r') as p:
                    l = p.readlines()
                    if len(l) > 0:
                        for i in l:
                            print(i, end='')
                    else:
                        print("EMPTY")
            elif not check_file(path):
                print("no such file exists")
        print("")
    else:
        path = use.get_path()
        if path[-3:] == 'dsu':
            if check_file(path):
                with open(path, 'r') as p:
                    l = p.readlines()
                    if len(l) > 0:
                        for i in l:
                            print(i, end='')
                    else:
                        print("EMPTY")
            elif not check_file(path):
                print("no such file exists") 
        else:
            print("please enter a file with \".dsu\" extention")
    print("")
    comm()


def open_file(a):
    global temp_path
    if administrator:
        path = a.split(' ')
        temp_path = path[1]
        f = open(temp_path, 'a')
        print(temp_path + " has been opened")
        return temp_path
    else:
        path = use.get_path()
        print("Without the file extention,")
        name = use.file_name()
        temp_path = path + "\\" + name
        f = open(temp_path, 'r+')
        print(temp_path + ' Has been opened')
        for line in f:
            print("hehehehe")
            print(line.strip())
    comm()
    return temp_path
        

def edit_file(a):
    if administrator:
        lis = a.split(' ')
        bio_index = a.find('-bio')
        bio = ''
        if bio_index != -1:
            start_quote = a.find('"', bio_index)
            end_quote = a.find('"', start_quote + 1)
            if start_quote != -1 and end_quote != -1:
                bio = a[start_quote + 1:end_quote]
        
        profile = Profile()
        profile.load_profile(path = temp_path)
        
        if '-usr' in lis:
            usr_index = lis.index('-usr')
            new_usr = ' '.join(lis[usr_index + 1:]).strip('"')
            profile.username = new_usr
            profile.save_profile(temp_path)
        if '-pwd' in lis:
            pwd_index = lis.index('-pwd')
            new_pwd= lis[pwd_index + 1]
            profile.password = new_pwd.strip('"')
            profile.save_profile(temp_path)
        if '-bio' in lis:
            profile.bio = bio.strip('"')
            profile.save_profile(temp_path)
        if '-addpost' in lis:
            post_index = lis.index('-addpost')
            post_content = ' '.join(lis[post_index + 1:])
            new_post = Post(post_content)
            profile.add_post(new_post)
            profile.save_profile(temp_path)
    else:
        profile = Profile()
        print("please enter a dsu file path")
        temp_path = input()
        profile.load_profile(path = temp_path)
        print("what would you like to edit?")
        print("\"-usr\" to update the username")
        print("\"-pwd\" to update password")
        print("\"-bio\" to update bio")
        print("\"-addpost\" to add a post")
        user_in = str(input())
        if "-usr" in user_in:
            new = str(input("enter new username: "))
            profile.username = new
            profile.save_profile(temp_path)
        elif "-pwd" in user_in:
            new = str(input("enter new password: "))
            profile.password = new
            profile.save_profile(temp_path)
        elif "-bio" in user_in:
            new = str(input("enter new bio: "))
            profile.bio = new
            profile.save_profile(temp_path)
        elif "-addpost" in user_in:
            post_content = input("Enter new post: ")
            new_post = Post(post_content)
            profile.add_post(new_post)
            profile.save_profile(temp_path)
            temp = input("would you like to post this on a server?  Y/N:    ")
            if temp == "Y":
                serv = input("please input a server:   ")
                port = 3021
                username = profile.username
                password = profile.password
                message = post_content
                send(serv, port, username, password, message)

    comm()


def print_data(command):
    global temp_path
    
    options = command.split()[1:]

    profile = Profile()
    profile.load_profile(temp_path)

    if '-usr' in options:
        print("Username:", profile.username)
    if '-pwd' in options:
        print("Password:", profile.password)
    if '-bio' in options:
        print("Bio:", profile.bio)
    if '-posts' in options:
        for i, post in enumerate(profile._posts):
            print(f"Post {i}: {post}")
    if '-post' in options:
        post_index = options.index('-post')
        post_id = int(options[post_index + 1])
        if 0 <= post_id < len(profile._posts):
            print(f"Post {post_id}: {profile._posts[post_id]}")
        else:
            print("Invalid post ID")
    if '-all' in options:
        print("Username:", profile.username)
        print("Password:", profile.password)
        print("Bio:", profile.bio)
        print("Posts:")
        for i, post in enumerate(profile._posts):
            print(f"  Post {i}: {post}")
    comm()

if __name__ == "__main__":
    user()

