#---Imported modules----------
import tkinter as gui
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from collections import namedtuple
import language_eng as eng
import language_rus as rus
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#---Custom classes------------

params = namedtuple('params',['N', 'I', 'beta', 'gamma', 'time'])

class cMathModel(object):
    def __init__(self, parameters):
        self.N=parameters.N
        self.I0=parameters.I # infected individuals
        self.S0=self.get_S0() # susceptible individuals
        self.beta=parameters.beta #effective contact rate of the disease
        self.gamma=parameters.gamma #recovery rate of the disease
        self.time = parameters.time
        self.sus = []
        self.inf = []

    def infection(self):
        S=self.S0
        I=self.I0
        N=self.N
        time=self.time
        beta=self.beta
        gamma=self.gamma
        self.sus.append(self.S0)
        self.inf.append(self.I0)
        for t in range (1, time):
            S, I = S - (beta*S*I/N) + gamma * I, I + (beta*S*I/N) - gamma * I

            self.sus.append(S)
            self.inf.append(I)

    def get_S0(self):
        return self.N-self.I0

    @staticmethod
    def get_case_1_params():
        return params(
            N=100,
            I=80,
            beta=0.4,
            gamma=0.3,
            time=100
        )

    @staticmethod
    def get_case_2_params():
        return params(
            N=100,
            I=80,
            beta=0.2,
            gamma=0.3,
            time=100
        )

    @staticmethod
    def get_case_3_params():
        return params(
            N=100,
            I=80,
            beta=0.2,
            gamma=0,
            time=100
        )

class cApp(gui.Tk):
    def __init__(self, *args, **kwargs):
        self.model=cMathModel(params(1000, 500, 0.2, 0.2, 100))
        self.lang='eng'

        #---GUI Elements--------------     
    
        gui.Tk.__init__(self, *args, **kwargs)
        self.main_menu=gui.Menu(self)
        self.language_menu=gui.Menu(self.main_menu, tearoff=0)
        self.example_menu=gui.Menu(self.main_menu, tearoff=0)
        self.model_plot_frame=gui.Frame(self, bg='#f6dddd')
        self.model_description_frame=gui.Frame(self, bg='#f6dddd')
        self.model_description=gui.Label(self.model_description_frame, bg='white', font=14, height=3)
        self.model_parameters_frame=gui.Frame(self, bg='#f6dddd')
        self.model_parameters_N_label=gui.Label(self.model_parameters_frame, bg='#f6dddd', font=14)
        self.model_parameters_N_scale=gui.Scale(self.model_parameters_frame, orient='hor', from_=2, to=10000, resolution=1, length=400, command=self.callback_N, font=14)
        self.model_parameters_I_label=gui.Label(self.model_parameters_frame, bg='#f6dddd', font=14)
        self.model_parameters_I_scale=gui.Scale(self.model_parameters_frame, orient='hor', from_=1, to=10000, resolution=1, length=400, command=self.callback_I, font=14)
        self.model_parameters_beta_label=gui.Label(self.model_parameters_frame, bg='#f6dddd', font=14)
        self.model_parameters_beta_scale=gui.Scale(self.model_parameters_frame, orient='hor', to=2, resolution=0.01, length=400, command=self.callback_beta, font=14)
        self.model_parameters_gamma_label=gui.Label(self.model_parameters_frame, bg='#f6dddd', font=14)
        self.model_parameters_gamma_scale=gui.Scale(self.model_parameters_frame, orient='hor', to=1.0, resolution=0.01, length=400, command=self.callback_gamma, font=14)
        self.model_parameters_time_label=gui.Label(self.model_parameters_frame, bg='#f6dddd', font=14)
        self.model_parameters_time_scale=gui.Scale(self.model_parameters_frame, orient='hor', from_=0, to=1000, resolution=1, length=400, command=self.callback_time, font=14)
        
        
        self.model.infection()

        self.figure = Figure(figsize=(5,5), dpi=100)
        self.sus_graph = self.figure.add_subplot(111)
        self.sus_graph.plot(self.model.sus)
        self.inf_graph =self.figure.add_subplot(111)
        self.inf_graph.plot(self.model.inf)
        self.sus_line = matplotlib.lines.Line2D([], [], color='steelblue')
        self.inf_line = matplotlib.lines.Line2D([], [], color='orange')
        self.figure.legend(handles=[self.sus_line,self.inf_line])
        self.canvas = FigureCanvasTkAgg(self.figure, self.model_plot_frame)
        self.canvas.draw()
        


        #---GUI Configuration---------

        self.minsize(1200, 680)
        self.configure(menu=self.main_menu)
        self.title('Epidemic Model SIS')
        self.main_menu.add_cascade(menu=self.language_menu)
        self.language_menu.add_command(command=self.rus_lang)
        self.language_menu.add_command(command=self.eng_lang)
        self.main_menu.add_command(command=self.about_message)
        self.main_menu.add_cascade(menu=self.example_menu)
        self.example_menu.add_command(command=self.example1)
        self.example_menu.add_command(command=self.example2)
        self.example_menu.add_command(command=self.example3)

        self.eng_lang()
        self.model_parameters_N_scale.set(self.model.N)
        self.model_parameters_I_scale.set(self.model.I0)
        self.model_parameters_beta_scale.set(self.model.beta)
        self.model_parameters_gamma_scale.set(self.model.gamma)
        self.model_parameters_time_scale.set(self.model.time)
        


        #---GUI Packing-----------
        self.model_description_frame.pack(side='bottom', anchor='s', ipadx=10, ipady=10, fill='both')
        self.model_description.pack(anchor='center', padx=10, pady=10, fill='both')
        self.model_plot_frame.pack(side='left', anchor='w', ipadx=100, ipady=100, fill='both', expand=True)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)
        self.model_parameters_frame.pack(side='right', anchor='e', ipadx=20, ipady=100, fill='both')
        self.model_parameters_N_label.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_N_scale.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_I_label.pack(side='top', anchor='w', padx=10, pady=10)
        self.model_parameters_I_scale.pack(side='top', anchor='w', padx=10, pady=10)
        self.model_parameters_beta_label.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_beta_scale.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_gamma_label.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_gamma_scale.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_time_label.pack(side='top', anchor='nw', padx=10, pady=10)
        self.model_parameters_time_scale.pack(side='top', anchor='nw', padx=10, pady=10)


    #---GUI functions-------------

    def about_message(self):
        if self.lang=='eng':
            about_message=eng.about_message
            about_message_title=eng.about_message_title
        else:
            about_message=rus.about_message
            about_message_title=rus.about_message_title
        msgbox.showinfo(about_message_title, about_message)

    def rus_lang(self):
        self.lang='rus'
        N_label=rus.N_label
        I_label=rus.I_label
        beta_label=rus.beta_label
        gamma_label=rus.gamma_label
        time_label=rus.time_label
        language_menu_label=rus.language_menu_label
        language_rus_label=rus.language_rus_label
        language_eng_label=rus.language_eng_label
        about_menu_label=rus.about_menu_label
        description_text=rus.description_text
        examples_menu_label=rus.examples_menu_label
        examples_example1_label=rus.examples_example1_label
        examples_example2_label=rus.examples_example2_label
        examples_example3_label=rus.examples_example3_label
        sus_line_label=rus.sus_line_label
        inf_line_label=rus.inf_line_label
        self.translate(
            N_label, 
            I_label,
            beta_label,
            gamma_label, 
            time_label,
            language_menu_label,
            language_rus_label,
            language_eng_label,
            about_menu_label,
            description_text,
            examples_menu_label,
            examples_example1_label,
            examples_example2_label,
            examples_example3_label,
            sus_line_label,
            inf_line_label
        )
        
    def eng_lang(self):
        self.lang='eng'
        N_label=eng.N_label
        I_label=eng.I_label
        beta_label=eng.beta_label
        gamma_label=eng.gamma_label
        time_label=eng.time_label
        language_menu_label=eng.language_menu_label
        language_rus_label=eng.language_rus_label
        language_eng_label=eng.language_eng_label
        about_menu_label=eng.about_menu_label
        description_text=eng.description_text
        examples_menu_label=eng.examples_menu_label
        examples_example1_label=eng.examples_example1_label
        examples_example2_label=eng.examples_example2_label
        examples_example3_label=eng.examples_example3_label
        sus_line_label=eng.sus_line_label
        inf_line_label=eng.inf_line_label
        self.translate(
            N_label, 
            I_label,
            beta_label,
            gamma_label, 
            time_label,
            language_menu_label,
            language_rus_label,
            language_eng_label,
            about_menu_label,
            description_text,
            examples_menu_label,
            examples_example1_label,
            examples_example2_label,
            examples_example3_label,
            sus_line_label,
            inf_line_label
        )

    def translate(self, 
        N_label, I_label, beta_label, gamma_label, time_label, 
        language_menu_label, language_rus_label, language_eng_label, 
        about_menu_label, description_text,
        examples_menu_label, examples_example1_label, examples_example2_label, examples_example3_label,
        sus_line_label, inf_line_label):
        self.model_parameters_N_label.config(text=N_label)
        self.model_parameters_I_label.config(text=I_label)
        self.model_parameters_beta_label.config(text=beta_label)
        self.model_parameters_gamma_label.config(text=gamma_label)
        self.model_parameters_time_label.config(text=time_label)
        self.model_description.config(text=description_text)
        self.main_menu.entryconfigure(1, label=language_menu_label)
        self.language_menu.entryconfigure(0, label=language_rus_label)
        self.language_menu.entryconfigure(1, label=language_eng_label)
        self.main_menu.entryconfigure(2, label=about_menu_label)
        self.main_menu.entryconfigure(3, label=examples_menu_label)
        self.example_menu.entryconfigure(0, label=examples_example1_label)
        self.example_menu.entryconfigure(1, label=examples_example2_label)
        self.example_menu.entryconfigure(2, label=examples_example3_label)
        self.sus_line.set_label(sus_line_label)
        self.inf_line.set_label(inf_line_label)
        self.redraw_plot()

    def example1(self):
        
        self.model=cMathModel(cMathModel.get_case_1_params())
        self.model.infection()
        self.model_parameters_N_scale.set(self.model.N)
        self.model_parameters_I_scale.set(self.model.I0)
        self.model_parameters_beta_scale.set(self.model.beta)
        self.model_parameters_gamma_scale.set(self.model.gamma)
        self.model_parameters_time_scale.set(self.model.time)
        self.redraw_plot()
        if self.lang=='eng':
            example1_message=eng.example1_message
            example1_message_title=eng.example1_message_title
        else:
            example1_message=rus.example1_message
            example1_message_title=rus.example1_message_title
        msgbox.showinfo(example1_message_title, example1_message)

    def example2(self):

        self.model=cMathModel(cMathModel.get_case_2_params())
        self.model.infection()
        self.model_parameters_N_scale.set(self.model.N)
        self.model_parameters_I_scale.set(self.model.I0)
        self.model_parameters_beta_scale.set(self.model.beta)
        self.model_parameters_gamma_scale.set(self.model.gamma)
        self.model_parameters_time_scale.set(self.model.time)
        self.redraw_plot()
        if self.lang=='eng':
            example2_message=eng.example2_message
            example2_message_title=rus.example2_message_title
        else:
            example2_message=rus.example2_message
            example2_message_title=rus.example2_message_title
        msgbox.showinfo(example2_message_title, example2_message)

    def example3(self):
        
        self.model=cMathModel(cMathModel.get_case_3_params())
        self.model.infection()
        self.model_parameters_N_scale.set(self.model.N)
        self.model_parameters_I_scale.set(self.model.I0)
        self.model_parameters_beta_scale.set(self.model.beta)
        self.model_parameters_gamma_scale.set(self.model.gamma)
        self.model_parameters_time_scale.set(self.model.time)
        self.redraw_plot()
        if self.lang=='eng':
            example3_message=eng.example3_message
            example3_message_title=eng.example3_message_title
        else:
            example3_message=rus.example3_message
            example3_message_title=rus.example3_message_title
        msgbox.showinfo(example3_message_title, example3_message)

    def callback_N(self, event):
        self.model.N=self.model_parameters_N_scale.get()
        if self.model.I0>self.model.N:
            self.model.I0=self.model.N
            self.model_parameters_I_scale.set(self.model.I0)
        self.model.S0=self.model.get_S0()
        self.redraw_plot()
    
    def callback_I(self, event):
        self.model.I0=self.model_parameters_I_scale.get()
        if self.model.I0>self.model.N:
            self.model.N=self.model.I0
            self.model_parameters_N_scale.set(self.model.N)
        self.model.S0=self.model.get_S0()
        self.redraw_plot()

    def callback_beta(self, event):
        self.model.beta=self.model_parameters_beta_scale.get()
        self.redraw_plot()

    def callback_gamma(self, event):
        self.model.gamma=self.model_parameters_gamma_scale.get()
        self.redraw_plot()

    def callback_time(self, event):
        self.model.time=self.model_parameters_time_scale.get()
        self.redraw_plot()

    def redraw_plot(self):
        self.model.sus.clear()
        self.model.inf.clear()
        self.model.infection()
        self.figure.clear()
        self.sus_graph = self.figure.add_subplot(111)
        self.sus_graph.plot(self.model.sus)
        self.inf_graph=self.figure.add_subplot(111)
        self.inf_graph.plot(self.model.inf)
        self.figure.legend(handles=[self.sus_line, self.inf_line])
        self.canvas.draw()
    
if __name__=='__main__':
    root=cApp()
    root.mainloop()
