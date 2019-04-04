from Tkinter import *
from SimpleCV import *
import winsound
import smtplib
i=0
j=0
x = True
after_id=None
per=0
#cam =None

def simplecvo():
    global after_id     
    global i
    global j
    #cam = JpegStreamCamera('http://192.168.43.1:8080/videofeed') ########### to use ip camera
    #global cam
    cam = Camera() ###################WEBCAM################################
    peakHue=w.get()
    th=w1.get()
    bsize=w2.get()
    blen=w3.get()
    synt=w4.get()
    idx = 0
    
    if x:
     
            idx+=1
            img=cam.getImage().scale(320,240)
            
            imgdist=img.hueDistance(peakHue)
            imagedistbin=imgdist.invert().threshold(th)
            blobs=imagedistbin.findBlobs(minsize=bsize)
            result=img.sideBySide(imgdist,side='bottom',scale=False)
            result=result.sideBySide(imagedistbin,side='right')
            result.show()

            if blobs is not None:
                le = len(blobs)

                if le!= blen:
                        winsound.Beep(1000,100)
                        #print "ok"
                        i=i+1
                        #timeLabel.config(text="Pass")
                else:
                        j=j+1
                        #print "fail"
    
    after_id=root.after(synt,simplecvo)

def start():
        global x
        x==True
        simplecvo()
    
def des(root):
        root.destroy()

def stop():
         global after_id
         if after_id:
                  root.after_cancel(after_id)
                  after_id=None
                  if i==0:
                     Label(root,text="No BListers Found",font = ("Verdana 10 bold",20)).grid(row=10,column=1,sticky=W+E+N+S)
                  else:
                      k=i+j
                      cal=float(i * 100)/k
                      global per
                      per=format(cal, '.2f')
                      Label(root,text="Correct  Packets :"+str(i),font = ("Verdana 10 bold",20)).grid(row=10,column=1,sticky=W+E+N+S)
                      Label(root,text="Defected Packets :"+str(j),font= ("Verdana 10 bold",20)).grid(row=11,column=1,sticky=W+E+N+S)
                      Label(root,text="Accuracy Rate   :"+str(per)+"%",font = ("Verdana 10 bold",20)).grid(row=12,column=1,sticky=W+E+N+S)
                      #del cam

def About():
    window = Toplevel(root)

def mail():
    if i!=0:
         fromaddr = ''    #UPDATE SENDER ADRRESS
         toaddrs  = ''    #UPDATE RECEIVER ADDRESS
         sub = 'Subject:Testing \n'
         msg = 'Correct  Packets ' +str(i) +'\n'+'Defected Packets '+str(j) + '\n'+'Accuracy rate' + str(per) +'%'
         result=sub+msg


         # Credentials (if needed)
         username = '' #SENDER EMAIL
         password = ''  # SENDER PASSWORD

         # The actual mail send
         server = smtplib.SMTP('smtp.gmail.com',587)
         server.ehlo()
         server.starttls()
         server.login(username,password)
         server.sendmail(fromaddr,toaddrs,result)
         server.quit()
    else:
        Label(root,text="Scanner has no data",font = ("Verdana 10 bold",20)).grid(row=10,column=1,sticky=W+E+N+S)
        
         
                  #######################GUI CODING ############################
root = Tk()
root.geometry("850x500")
root.title('Quality Checker')
#root.state('zoomed')
                                   
button_1=Button(root,text="Start",width=10,command=start,fg = "Black").grid(row=6,column=1,sticky=N)

button = Button(root, text='Stop', width=10, command=stop).grid(row=7,column=1,sticky=S)

button_2 = Button(root, text='Quit', width=10, command=lambda root=root:des(root)).grid(row=8,column=1,sticky=S)

button_3= Button(root, text='Mail', width=10, command=mail).grid(row=9,column=1,sticky=S)
#timeLabel = Label(root, fg='green',font=('Helvetica',150)).grid(row=9,column=1)

Label(root,text="Packaging Quality Checker Of Medicines",fg = "Red",bg = "Black",font = ("Verdana 10 bold",10)).grid(row=0)

Label(root, text='Change Hue',font = ("Verdana 10 bold",10)).grid(row=2,sticky=S+W)
w = Scale(root, from_=0, to=200,length=500, orient=HORIZONTAL,font = ("Verdana 10 bold",10))
w.grid(row=2,column=1)
w.set(15.0)

Label(root, text='Change Threshold',font = ("Verdana 10 bold",10),activebackground="Red").grid(row=4,sticky=S+W)
w1 = Scale(root, from_=0, to=200, length=500, orient=HORIZONTAL,font = ("Verdana 10 bold",10))
w1.grid(row=4,column=1)
w1.set(180)


Label(root, text='Blob Size',font = ("Verdana 10 bold",10)).grid(row=1,sticky=S+W)
w2 = Scale(root, from_=0, to=2000,length=500, orient=HORIZONTAL,font = ("Verdana 10 bold",10))
w2.grid(row=1,column=1)
w2.set(1000)

Label(root, text='No. Of Blisters',font = ("Verdana 10 bold",10)).grid(row=3,sticky=S+W)
w3 = Scale(root, from_=0, to=20,length=500, orient=HORIZONTAL,font = ("Verdana 10 bold",10))
w3.grid(row=3,column=1)
w3.set(8)

Label(root, text='Time to take one shot(miliseconds)',font = ("Verdana 10 bold",10)).grid(row=5,sticky=S+W)
w4 = Scale(root, from_=0, to=10000,length=500, orient=HORIZONTAL,font = ("Verdana 10 bold",10))
w4.grid(row=5,column=1)
w4.set(1000)

menu = Menu(root)
root.config(menu=menu)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)



root.mainloop()
