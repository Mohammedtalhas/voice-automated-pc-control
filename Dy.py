import os
import shutil
import subprocess as s
import icon  
from win10toast import ToastNotifier
from Adafruit_IO import Client, Data
aio = Client('2463b53e4a774cd9a3195257819e5826')

import re, urllib, sys
toaster = ToastNotifier()

version = sys.version_info[0]

if version == 2:
    user_input = raw_input
    import urllib2
    urlopen = urllib2.urlopen
    encode = urllib.urlencode
    retrieve = urllib.urlretrieve
    cleanup = urllib.urlcleanup()

else:
    user_input = input
    import urllib.request
    import urllib.parse
    urlopen = urllib.request.urlopen
    encode = urllib.parse.urlencode
    retrieve = urllib.request.urlretrieve
    cleanup = urllib.request.urlcleanup()


def ming(st):
    path = st
    list_ = os.listdir(path)
    for file_ in list_:
        name,ext = os.path.splitext(file_)
        ext = ext[1:]
        if ext == '':
            continue
        if os.path.exists(path+'/'+ext):
            try:
                shutil.move(path+'/'+file_,path+'/'+ext+'/'+file_)
            except:
                continue
        else:
            try:
                os.makedirs(path+'/'+ext)
                shutil.move(path+'/'+file_,path+'/'+ext+'/'+file_)
            except:
                continue

def exit(code):
    print('\nExiting....')
    print('\nHave a good day.')
    sys.exit(code)

def video_title(url):
    try:
        webpage = urlopen(url).read()
        title = str(webpage).split('<title>')[1].split('</title>')[0]
    except:
        title = 'Youtube Song'

    return title


def single_download(song=None):
    if not(song):
        song = user_input('Enter the song name or youtube link: ')

    if "youtube.com/" not in song:
        try:
            query_string = encode({"search_query" : song})
            html_content = urlopen("http://www.youtube.com/results?" + query_string)

            if version == 3:
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            else:
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read())
        except:
            print('Network Error')
            return None

        command = 'youtube-dl --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" ' + search_results[0]

    else:
        command = 'youtube-dl --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" ' + song[song.find("=")+1:]
        song=video_title(song)

    try:
        print('Downloading %s' % song)
        os.system(command)
    except:
        print('Error downloading %s' % song)
        return None




while(1):

    rec = aio.receive('Control')
    data=rec.value



    if data == '0':
        continue

    if data == '1':

        toaster.show_toast('Shell & Bash\n',"SHUTTING DOWN YOUR PC......",icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        os.system("SHUTDOWN -s ")
        continue

    if data == '2':
        toaster.show_toast('Shell & Bash\n',"RESTARTING YOUR PC.....",icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        os.system("SHUTDOWN -r")
        continue

    if(data[:6]=="a new "):
        st = str(data[6:])
        toaster.show_toast('Shell & Bash\n','Creating a New '+ st +' Folder',icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        newpath = r'Desktop/' + st + '/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        else:
            continue
        continue

    if(data[:4]=="the "):
        st = str(data[4:])
        toaster.show_toast('Shell & Bash\n','Deleting the '+ st +' Folder',icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        x = 1
        newpath = 'Desktop/' +st+ '/'
        if os.path.exists(newpath):
            shutil.rmtree(newpath)
        else:
            continue
        continue

    if 'of' in data[:5]:
        no = int(data[0])
        if(data[1] is not ' '):
            no = (no*10)+int(data[1])
        st = str(data[6:])
        toaster.show_toast('Shell & Bash\n','Downloading '+str(no)+ ' images of ' + st,icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        command = 'googleimagesdownload --keywords ' + st + ' --limit '+ str(no)
        os.system(command)
        continue


    if data == '5':
        st = r'Desktop/'
        toaster.show_toast('Shell & Bash','Organizing your Desktop Folder',icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        ming(st)
        continue

    if data == '6':
        toaster.show_toast('Shell & Bash','Suspending your PC....',icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        os.system("systemctl suspend")
        continue
    
    if data == '8':
        st = 'Downloads/'
        toaster.show_toast('Shell & Bash','Organizing your Downloads Folder',icon_path="SB.ico")
        data = Data(value='0')
        aio.create_data('Control', data)
        ming(st)
        continue
        

    if(str(data)):
        st = str(data)
        toaster.show_toast('Shell & Bash\n','Downloading  '+ st +' Song',icon_path="SB.ico")
        try:
            single_download(str(st))
        except NameError:
            exit(1)
        data = Data(value='0')
        aio.create_data('Control', data)
        print('Completed Download')
        continue


    
