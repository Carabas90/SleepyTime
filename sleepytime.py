import matplotlib.pyplot as plt
from tkinter import Tk, Label, Scale, IntVar, Button, Grid, Radiobutton, Entry


def med_dose(rate, hwz, ppb, sizefactor):
    """Takes a influx rate (in mg/h), the halflife of the medication (in minutes), the percentage 
        of substance binding to plasma proteins and a factor which respresents the size of the 
        second kompartment (fatty tissue an musculature) in realtion to blood volume. Returns
        a list which represents the cummulation of the medication up until the point of maximum 
        cummulation, then the breakdown of the medication from this point on"""
    q = 1- ((0.5/hwz)*60) 
    ppf = 1 - (ppb/100) #Factor of substance, which is not bound to Plasma-Proteins
    med = [0]
    komp2 = 0 #Represents the musculature and the fatty tissue in which the substance diffuses
    sconc= rate*q
    if (sconc * ppf) > (komp2 / sizefactor):
        sconc -= (sizefactor*ppf*sconc - komp2)/(sizefactor+1)
        komp2 += (sizefactor*ppf*sconc - komp2)/(sizefactor+1)
    med.append(round(sconc, 3))
    i = 2
    while med[-1] != med[-2]:
        sconc = (sconc + rate)*q
        if (sconc * ppf) > (komp2 / sizefactor):
            sconc -= (sizefactor*ppf*sconc - komp2)/(sizefactor+1)
            komp2 += (sizefactor*ppf*sconc - komp2)/(sizefactor+1)
        med.append(round(sconc, 3))
        i += 1

    sconc = sconc*q
    if (sconc * ppf) < (komp2 / sizefactor):
        sconc += (komp2- sizefactor*ppf*sconc)/(sizefactor+1)
        komp2 -= (komp2- sizefactor*ppf*sconc)/(sizefactor+1)
    med.append(round(sconc, 3))
    while sconc > 0.1:
        sconc = sconc*q
        if (sconc * ppf) < (komp2 / sizefactor):
            sconc += (komp2- sizefactor*ppf*sconc)/(sizefactor+1)
            komp2 -= (komp2- sizefactor*ppf*sconc)/(sizefactor+1)
        med.append(round(sconc, 3))
    return med


def create_x_axis(list):
    """Creates a list which represents the part of the input list in which the numbers are rising with
        with negative numbers an the part in which the numbers are falling with positive numbers. This 
        makes the point of maximum cummulation the 0-point on the x-Axis of the Graph"""
    x_axis = []
    for i in range(len(list)):
        if list[i] != list[i+1]:
            continue
        else:
            l = (-1)*(i+1)
            break
    for _ in range(len(list)):
      x_axis.append(l)
      l += 1  
    return x_axis


def draw_graph(med_list, med_name=None):
    """plots a list of medication doses with the point of maximum cummulation as the 0-point on the 
        x-axis. med_name is an optional argument to create a legend"""
    plt.plot(create_x_axis(med_list), med_list, label= med_name) 


def show_graph():
    plt.xlabel('Zeit in Stunden')
    plt.ylabel('Kummulierte Dosis')
    plt.ylim(bottom=0)
    plt.title('Pharmakokinetik der Analgosedierung')
    plt.legend()
    plt.show()


def open_gui():
    """Creates a small GUI, which serves as an input for drawing graphs"""
    def calc():
        """ Plots and shows the graphs from the users input in the GUI"""
        propdose = (sclprop.get() * int(centryprop.get()) /10)
        midadose = (sclmida.get() * int(centrymida.get()))
        ketadose = (sclketa.get() * int(centryketa.get()) / 10)
        sufentadose = (sclsufenta.get() * int(centrysufenta.get()) / 10)
        propv = propvar.get()
        midav = midavar.get()
        ketav = ketavar.get()
        sufentav = sufentavar.get()

        if propdose != 0:
            draw_graph(med_dose(propdose, propv, 98, 10), med_name='Propofol 1=10mg')
        if midadose != 0:
            draw_graph(med_dose(midadose, midav, 95, 10), med_name='Midazolam 1=1mg')
        if ketadose != 0:
            draw_graph(med_dose((ketadose), ketav, 47, 10), med_name='Ketamin 1=10mg')
        if sufentadose != 0:
            draw_graph(med_dose((sufentadose), sufentav, 92, 10), med_name='Sufenta 1=10 Mikrogramm')
        
        show_graph()
    
    root = Tk()
    root.title('SleepyTime')

    spacer1 = Label(root, text='')
    spacer1.grid(row=0)

    lblprop = Label(root, text='Propofol   ')
    lblprop.grid(row=1 , column=0, sticky='W')

    sclprop = Scale(root, from_=0, to=20, orient='horizontal')
    sclprop.grid(row=1, column=1)

    hwzproplbl = Label(root, text='   HWZ   ')
    hwzproplbl.grid(row=1, column=2)

    propvar = IntVar()
    radioprop1 = Radiobutton(root, text='kurz   ', variable=propvar, value=40, selectcolor='black')
    radioprop1.grid(row=1, column=3)
    radioprop2 = Radiobutton(root, text='mittel', variable=propvar, value=120, selectcolor='black')
    radioprop2.grid(row=1, column=4)
    radioprop3 = Radiobutton(root, text='lang', variable=propvar, value=200, selectcolor='black')
    radioprop3.grid(row=1, column=5)
    radioprop1.select()

    centryprop = Entry(root, width=5)
    centryprop.grid(row=1, column=6)
    centryprop.insert(1, '20')
    centryproplbl = Label(root, text='mg/ml')
    centryproplbl.grid(row=1, column=7)

    lblmida = Label(root, text='Midazolam   ')
    lblmida.grid(row=2, column=0, sticky='W')

    sclmida = Scale(root, from_=0, to=20, orient='horizontal')
    sclmida.grid(row=2, column=1)

    hwzmidalbl = Label(root, text='   HWZ   ')
    hwzmidalbl.grid(row=2, column=2)

    midavar = IntVar()
    radiomida1 = Radiobutton(root, text='kurz   ', variable=midavar, value=90, selectcolor='black')
    radiomida1.grid(row=2, column=3)
    radiomida2 = Radiobutton(root, text='mittel', variable=midavar, value=345, selectcolor='black')
    radiomida2.grid(row=2, column=4)
    radiomida3 = Radiobutton(root, text='lang', variable=midavar, value=600, selectcolor='black')
    radiomida3. grid(row=2, column=5)
    radiomida1.select()

    centrymida = Entry(root, width=5)
    centrymida.grid(row=2, column=6)
    centrymida.insert(1, '2')
    centrymidalbl = Label(root, text='mg/ml')
    centrymidalbl.grid(row=2, column=7)

    lblketa = Label(root, text='Ketamin   ')
    lblketa.grid(row=3, column=0, sticky='W')

    sclketa = Scale(root, from_=0, to=20, orient='horizontal')
    sclketa.grid(row=3, column=1)

    hwzketalbl = Label(root, text='   HWZ   ')
    hwzketalbl.grid(row=3, column=2)

    ketavar = IntVar()
    radioketa1 = Radiobutton(root, text='kurz   ', variable=ketavar, value=120, selectcolor='black')
    radioketa1.grid(row=3, column=3)
    radioketa2 = Radiobutton(root, text='mittel', variable=ketavar, value=200, selectcolor='black')
    radioketa2.grid(row=3, column=4)
    radioketa3 = Radiobutton(root, text='lang', variable=ketavar, value=180, selectcolor='black')
    radioketa3. grid(row=3, column=5)
    radioketa1.select()

    centryketa = Entry(root, width=5)
    centryketa.grid(row=3, column=6)
    centryketa.insert(1, '50')
    centryketalbl = Label(root, text='mg/ml')
    centryketalbl.grid(row=3, column=7)

    lblsufenta = Label(root, text='Sufentanil   ')
    lblsufenta.grid(row=4, column=0, sticky='W')

    sclsufenta = Scale(root, from_=0, to=20, orient='horizontal')
    sclsufenta.grid(row=4, column=1)

    hwzsufentalbl = Label(root, text='   HWZ   ')
    hwzsufentalbl.grid(row=4, column=2)

    sufentavar = IntVar()
    radiosufenta1 = Radiobutton(root, text='kurz   ', variable=sufentavar, value=158, selectcolor='black')
    radiosufenta1.grid(row=4, column=3)
    radiosufenta2 = Radiobutton(root, text='mittel', variable=sufentavar, value=161, selectcolor='black')
    radiosufenta2.grid(row=4, column=4)
    radiosufenta3 = Radiobutton(root, text='lang', variable=sufentavar, value=164, selectcolor='black')
    radiosufenta3.grid(row=4, column=5)
    radiosufenta1.select()

    centrysufenta = Entry(root, width=5)
    centrysufenta.grid(row=4, column=6)
    centrysufenta.insert(1, '15')
    centrysufentalbl = Label(root, text='µg/ml')
    centrysufentalbl.grid(row=4, column=7)

    spacer2 = Label(root, text='')
    spacer2.grid(row=5)

    calcbutton = Button(root, text='  Berechnen  ', command=calc)
    calcbutton.grid(row=6, column=5)

    spacer3 = Label(root, text='')
    spacer3.grid(row=7, column=6)

    root.mainloop()



if __name__ == "__main__":
    open_gui()