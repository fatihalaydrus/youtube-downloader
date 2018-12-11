from pytube import YouTube
from tkinter import *
from tkinter.font import Font
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo
from os.path import exists

class YouTubeDownloader(YouTube):
    def __init__(self, master):
        self.master = master
        master.minsize(300,300)
        master.title('YouTube Downloader by Fatih IA')

        self.__widget()
        self.__pack()

    def __widget(self):
        self.master.bind('<Return>', self.check)
        self.font = Font(family='Helvetica',size=12, weight='bold')

        self.link_lable = Label(self.master,text='Input your YouTube link:',font=self.font)
        self.out_lable = Label(self.master,text='Filename:',font=self.font)
        self.link = StringVar()
        self.link_field = Entry(self.master,textvariable=self.link,width=25)

    def __pack(self):
        self.link_lable.pack()
        self.link_field.pack()

    def check(self, event):
        link = self.link.get()
        if not ('https://youtu.be' in link or 'https://www.youtube.com' in link):
            showerror('Link Error', "Please input a valid YouTube link!\neg. 'https://www.youtube.com/watch?v= ...'")
        else:
            if 'youtu.be' in link:
                link = 'https://www.youtube.com/watch?v=' + link[-11:]

            super().__init__(link)
            vidtitle = self.title
            self.outfile = StringVar(value = vidtitle)
            self.out_lable.pack()
            self.outfile_field = Entry(self.master,textvariable=self.outfile,width=25)
            self.outfile_field.pack()
            self.master.bind('<Return>', self.check2)

    def check2(self,event):
        outfile = self.outfile.get()
        if any(x in '''\/:*?"<>|''' for x  in outfile):
            showerror('Filename Error', '''A file name can't contain any of the following
            \/:*?"<>|''')
        else:
            self.vid_list()

    def vid_list(self):
        prompt = Message(self.master, text='Available file format:')
        prompt.pack_forget()
        prompt.pack()

        vid_list = self.streams.filter(type='video').order_by('resolution').all()

        self.chosen_num = IntVar()
        self.streamed = {}
        for num, vids in enumerate(vid_list):
            resolution = vids.resolution
            fps = vids.fps
            streamtype = vids.mime_type
            Radiobutton(self.master,text = f'{resolution} {fps}FPS {streamtype}',
            variable=self.chosen_num, value=num).pack()
            self.streamed[num] = vids
        self.download_init()

    def download_init(self):
        self.download_button = Button(self.master,text='Download!',command=self.download_video)
        self.download_button.pack()

    def download_video(self):
        path = self.askdir()
        filename = self.outfile_field.get()
        chosen_type = self.streamed[self.chosen_num.get()]
        if exists(path+filename+'.'+chosen_type.subtype):
            showinfo('File Exist','The file you want to download already exist.')
            self.master.destroy()
            exit()
        showinfo('Download Prompt', 'Your file will now be downloaded')
        chosen_type.download(path, filename)

    def askdir(self):
        path = askdirectory()
        path = path.replace('/', '\\') + '\\'
        return path

def main():
    root = Tk()
    YTD = YouTubeDownloader(root)
    root.mainloop()

if __name__ == '__main__':
    main()
