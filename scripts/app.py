""" Tkinter GUI for Lyrics Analyzer """

# import libraries
import tkinter as tk
from lyrics_tool import LyricsTool


class app:
    
    def __init__(self):
        
        self.label4=None
    
    def main(self):
        
        # set up Tkinter
        root = tk.Tk()
        root.title("Explicit Lyrics Detector")
        canvas1 = tk.Canvas(root, width = 500, height = 250)
        canvas1.pack()

        # main title
        label1 = tk.Label(root, text='Explicit Lyrics Detector')
        label1.config(font=('helvetica', 24))
        canvas1.create_window(250, 25, window=label1)

        # start note text entry field
        label2 = tk.Label(root, text='Song Title')
        label2.config(font=('helvetica', 10))
        canvas1.create_window(150, 100, window=label2)

        entry1 = tk.Entry (root) 
        canvas1.create_window(150, 75, window=entry1)


        # start note text entry field
        label3 = tk.Label(root, text='Artist')
        label3.config(font=('helvetica', 10))
        canvas1.create_window(350, 100, window=label3)

        entry2 = tk.Entry (root) 
        canvas1.create_window(350, 75, window=entry2)


        # transpose button
        def VetLyricsButton():  
            
            if self.label4 == None:
                pass
            else:
                self.label4.destroy()

            # get data
            song_title = entry1.get()
            artist = entry2.get()

            # transpose note
            v = LyricsTool()
            clean = v.vet(song_title, artist)

            if clean==True:
                state='Clean Lyrics'
            else:
                state='Explicit lyrics detected!'

            # display transposed note to user

            self.label4 = tk.Label(root, text= state)
            self.label4.config(font=('helvetica', 14))
            canvas1.create_window(250, 200, window=self.label4)

            
        # primary button for transposing notes
        button1 = tk.Button(text='Submit', command=VetLyricsButton)
        canvas1.create_window(250, 150, window=button1)


        # main loop
        root.mainloop()
        
a = app()

a.main()
