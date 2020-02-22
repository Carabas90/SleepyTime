import matplotlib.pyplot as plt
from tkinter import Tk, Label, Scale, IntVar, Button, Grid, Radiobutton


def serum_conc_calculator(t, q , influx):
    """Takes a timeframe (t, usually hours), a quotient (0<q>1), and the influx of a medication 
        in mg/h and returns the serum concentration at the end of t"""
    serum_conc = 0
    for _ in range(t):
        serum_conc = (serum_conc + influx)*q
    return serum_conc 


def breakdown(start_dose, q , t):
    """ Takes the starting dose of a medication, a quotient (0<q>1), and a timeframe (t), and returns 
        the remaining dose after t"""
    remaining = start_dose *(q**t)
    return remaining


def med_dose(rate, hwz):
    """Takes a influx rate (in mg/h) and the halflife of the medication (in minutes), and returns
        a list which represents the cummulation of the medication up until the point of maximum 
        cummulation, then the breakdown of the medication from this point on"""
    q = 1- ((0.5/hwz)*60) 
    med = [0]
    med.append(round(serum_conc_calculator(1, q, rate), 2))
    i = 2
    while med[-1] != med[-2]:
        med.append(round(serum_conc_calculator(i, q, rate), 2))
        i += 1

    med.append(round(breakdown(med[-1], q, 1), 2))
    while med[-1] != med[-2]:
        med.append(round(breakdown(med[-1], q, 1), 2))
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
    plt.legend()
    plt.show()


def open_gui():
    """Creates a small GUI, which serves as an input for drawing graphs"""
    def calc():
        propdose = sclprop.get()
        midadose = sclmida.get()
        ketadose = sclketa.get()
        sufentadose = sclsufenta.get()
        propv = propvar.get()
        midav = midavar.get()
        ketav = ketavar.get()
        sufentav = sufentavar.get()

        if propdose != 0:
            draw_graph(med_dose((propdose*20), propv), med_name='Propofol 1=1mg')
        if midadose != 0:
            draw_graph(med_dose((midadose*2), midav), med_name='Midazolam 1=1mg')
        if ketadose != 0:
            draw_graph(med_dose((ketadose*5), ketav), med_name='Ketamin 1=10mg')
        if sufentadose != 0:
            draw_graph(med_dose((sufentadose*1.5), sufentav), med_name='Sufenta 1=10 Mikrogramm')
        
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
    radioprop3. grid(row=1, column=5)
    radioprop1.select()

    lblmida = Label(root, text='Midazolam   ')
    lblmida.grid(row=2, column=0, sticky='W')

    sclmida = Scale(root, from_=0, to=20, orient='horizontal')
    sclmida.grid(row=2, column=1)

    hwzmidalbl = Label(root, text='   HWZ   ')
    hwzmidalbl.grid(row=2, column=2)

    midavar = IntVar()
    radiomida1 = Radiobutton(root, text='kurz   ', variable=midavar, value=90, selectcolor='black')
    radiomida1.grid(row=2, column=3)
    radiomida2 = Radiobutton(root, text='mittel', variable=midavar, value=360, selectcolor='black')
    radiomida2.grid(row=2, column=4)
    radiomida3 = Radiobutton(root, text='lang', variable=midavar, value=630, selectcolor='black')
    radiomida3. grid(row=2, column=5)
    radiomida1.select()

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

    spacer2 = Label(root, text='')
    spacer2.grid(row=5)

    calcbutton = Button(root, text='  Berechnen  ', command=calc)
    calcbutton.grid(row=6, column=5)

    spacer3 = Label(root, text='')
    spacer3.grid(row=7, column=6)

    root.mainloop()



if __name__ == "__main__":
    open_gui()