import argparse
from tkinter import END, Frame, Label,LabelFrame,Entry,Button,StringVar,Tk,OptionMenu, Text,Canvas, WORD, INSERT
from tkinter import messagebox,filedialog,simpledialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageGrab
# import all the local helpers
from helpers.cadaster import *
from helpers.satmap import *
import time

parser = argparse.ArgumentParser(description="Run the Ultima Patagonia interface")
parser.add_argument(
    "os",
    help='The operating system to work in e.g. "Windows" or "LinuxMac"',
)

args = parser.parse_args()
global OS
OS = args.os

# some constants for now
CRSLIST = [
    "Longitude-Latitude",
    "UTM Zone 18S"
]
BOLDFONT: tuple = ("Arial",12,"bold")
VALIDATED_FONT: tuple = ("Arial",11)

# testing that the database can be accessed nicely. missing an update field method for now...

# root frame.


# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         sbf = ScrollbarFrame(self)
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#         sbf.grid(row=0, column=0, sticky='nsew')
#         # sbf.pack(side="top", fill="both", expand=True)

#         # Some data, layout into the sbf.scrolled_frame
#         frame = sbf.scrolled_frame
#         for row in range(50):
#             text = "%s" % row
#             tk.Label(frame, text=text,
#                      width=3, borderwidth="1", relief="solid") \
#                 .grid(row=row, column=0)

#             text = "this is the second column for row %s" % row
#             tk.Label(frame, text=text,
#                      background=sbf.scrolled_frame.cget('bg')) \
#                 .grid(row=row, column=1)


class CaveDatabaseApp(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        global root
        root = Frame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # sbf.pack(side="top", fill="both", expand=True)



        root.pack(side="top", fill="both", expand = True)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)



        self.frames = {}

        for F in (StartPage, AddFrame, FindCaveFrame, ConvertVisualFrame, PlotFrame, Create2DFrame):

            frame = F(root, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Menu Principal", font=BOLDFONT)
        label.grid(pady=10,padx=10,row=0,column=0,columnspan=2)
        
        input_path = StringVar()
        input_path.set('')
  

        def open_database():
            root_filename = filedialog.askopenfilename(
                initialdir="../therion/data", 
                title="Select a file", 
                filetypes=(("CSV files", "*.csv"),("All files", "*.*"))
            )
            input_path.set(root_filename.split('/')[-1])

            global MyCaveCadaster
            MyCaveCadaster = initialise_database(root_filename)

        databasenameLabel = Label(self, textvariable= input_path,width=50)
        databasenameLabel.grid(pady=10,padx=10,row=1,column=0)

        databaseOpenButton = Button(self, text="Selectionner la base de donnees", width=50,command=open_database)
        databaseOpenButton.grid(pady=10,padx=10,row=2,column=0)
        OpenNoteText = """
        Selectionner un tableur au format csv"""
        databaseOpenNote = Label(self, text=OpenNoteText, width=50)
        databaseOpenNote.grid(pady=10,padx=10,row=2,column=1)

        chosen_path = StringVar()
        chosen_path.set('')

        def open_dialog():
            root_filename = filedialog.asksaveasfilename(
                initialdir="../therion/data", 
                title="Selectionner un fichier", 
                filetypes=(("CSV files", "*.csv"),("Tous fichiers", "*.*"))
            )
            chosen_path.set(root_filename)

            if chosen_path.get() != "":
                try:
                    MyCaveCadaster.write_to_file(chosen_path.get())
                except FileNotFoundError:
                    messagebox.showwarning("Erreur de saisie", "Entrez un nom de fichier valide!")
                    pass


        filenameOpenButton = Button(self, text="Sauvegarder", command=open_dialog,width=50)
        filenameOpenButton.grid(row=3,column=0, padx=10,pady=10)
        SaveNoteText = """
        Enregistrer la base de données dans un tableur au format csv"""
        databaseSaveNote = Label(self, text=SaveNoteText, width=50)
        databaseSaveNote.grid(pady=10,padx=10,row=3,column=1)

        button = Button(self, text="Ajouter une cavité",width=50,
                            command=lambda: controller.show_frame(AddFrame))
        button.grid(pady=10,padx=10,row=4,column=0)
        UpdateNoteText = """
        Renseigner les données d'une nouvelle cavité."""
        UpdateNote = Label(self, text=UpdateNoteText, width=50)
        UpdateNote.grid(pady=10,padx=10,row=4,column=1)

        button = Button(self, text="Trouver une cavité",width=50,
                            command=lambda: controller.show_frame(FindCaveFrame))
        button.grid(pady=10,padx=10,row=5,column=0)
        FindNoteText = """
        Trouver l'emplacement d'une cavité existante."""
        FindNote = Label(self, text=FindNoteText, width=50)
        FindNote.grid(pady=10,padx=10,row=5,column=1)

        button = Button(self, text="Convertir un fichier Visual Topo",width=50,
                            command=lambda: controller.show_frame(ConvertVisualFrame))
        
        button.grid(pady=10,padx=10,row=6,column=0)
        ConvertText = """
        Convertir un fichier Visual Topo (.tro) au format Therion (.th) """
        ConvertNote = Label(self, text=ConvertText, width=50)
        ConvertNote.grid(pady=10,padx=10,row=6,column=1)


        button = Button(self, text="Creer un fichier 2D ou 3D",width=50,
                            command=lambda: controller.show_frame(Create2DFrame))
        button.grid(pady=10,padx=10,row=7,column=0)
        To2DText = """

        Construire un modele .3d ainsi que les fichiers croquis 2D .th2"""
        To2DNote = Label(self,width=50,text=To2DText)
        To2DNote.grid(pady=10,padx=10,row=7,column=1)

        QuitButton = Button(self, text= "Quitter", command= lambda : root.master.destroy(),width=50)
        QuitButton.grid(pady=10,padx=10,row=8,column=0)

class Create2DFrame(Frame):
    def __init__(self, parent,controller):
        Frame.__init__(self,parent)    

        def convert_file() -> None:
            #global chosen_file
            chosen_file =  filedialog.askopenfilename(
                initialdir="../therion/data", 
                title="Selectionner un fichier", 
                filetypes=(("Fichiers Therion", "*.th"),("Tous fichiers", "*.*"))
            )

            filename = chosen_file.split("\\")[-1].split("/")[-1][:-3]
            print(chosen_file)
            print(filename)
            command  = f"python {abspath('create_2d.py')} --projection {{}} {abspath(chosen_file)} {str(filename)}"
            print("COMMAND", command)
            check_output(command.format('plan'), shell=True)
            check_output(command.format('extended'), shell=True)
            
            #check_output(f"python {abspath('../therion/scripts/create_2d.py')} --projection extended {abspath(chosen_file)} {str(filename)}", shell=True)

        
        ConvertButton = Button(self,text="Extraire les points topo au format .th2",command= convert_file)
        ConvertButton.grid(row=0,column=0)



        button1 = Button(self, text="retour",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=25,column=1)



class FindCaveFrame(Frame):

    def __init__(self, parent,controller):
        Frame.__init__(self,parent)    

        button1 = Button(self, text="retour",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=25,column=1)
        
        databaseInputFrame = LabelFrame(self, text= "Choix de la base de données", padx=5, pady=5)
  
        folder_path = StringVar()
        folder_path.set("")

        def search(search: str)-> None:
            try: 
                caves = MyCaveCadaster.find_cave(search)
            except CaveNotFoundError:
                messagebox.showwarning("Aucune cavite a ce nom.", "Entrez un nom valide ou un numero cadastral existant")

            # cycle over key values.
            if len(caves) == 1:
                global cave
                cave = caves[0]
            else: 
                names = ""
                for cave in caves:
                    names += f"\n {cave.cadnum} {cave.name}"
                messagebox.showwarning("Plus d'une cavite a ce nom", names)


            cave.add_coordinates(cave.coordinates)
            folder_path.set(cave._folder_path)
            i=0
        
            for key,value in cave.__dict__.items():
                if key[0] != "_":
                    if key != "coordinates":
                        label = Label(self, text = key, font=BOLDFONT)
                        label.grid(row = 4+i,column=0)
                        valueLabel = Text(self, height=3, wrap=WORD)
                        valueLabel.insert(1.0, value)
                        valueLabel.grid(row = 4+i,column=1)
                        i+=1
                    else:
                        for coord,label in zip((cave.coordinates.x,cave.coordinates.y),("X UTM 18S","Y UTM 18S")):
                            label = Label(self, text = label, font=BOLDFONT)
                            label.grid(row = 4+i,column=0)
                            valueLabel = Text(self, height=3, wrap=WORD)
                            valueLabel.insert(1.0, coord)
                            valueLabel.grid(row = 4+i,column=1)
                            i+=1
            # if any update needed

        def open_directory(dirname: str)-> None:
            actual_dirname = abspath(dirname)

            try: 
                if exists(actual_dirname):
                    if OS == "LinuxMac":
                        print("using Linux or Mac")
                        check_output(f"open {actual_dirname}", shell=True) # linux or mac
                    elif OS == "Windows":
                        print("using windows")
                        print(actual_dirname)
                        check_output(f"start {actual_dirname}", shell=True) # on windows

            except CalledProcessError:
                raise
        
        # search
        caveNameSearch = Entry(databaseInputFrame)
        caveNameSearch.grid(row=4,column=1)
        cavenameLabel = Button(databaseInputFrame, text = 'Rechercher une cavité', command = lambda : search(caveNameSearch.get()))
        cavenameLabel.grid(row=4,column=0)
        # open file explorer
        openButton = Button(databaseInputFrame,text="Ouvrir le dossier",  command = lambda : open_directory(folder_path.get().strip("\n")))
        openButton.grid(row=15,column=2)
        #openFilePath = Label(databaseInputFrame,textvariable=folder_path)
        #openFilePath.grid(row=15,column=3)

        databaseInputFrame.grid(row=0,column=0,sticky="nw")





class AddFrame(Frame):

    def __init__(self, parent,controller):
        Frame.__init__(self,parent)

        button1 = Button(self , text="Retour",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=10,column=1)
        
        SectorName = StringVar()
        SectorRoot = StringVar()
        SectorRoot.set('999')


        #### input coordinates frame
        coordInputFrame = LabelFrame(self, text= "Entrée des coordonnées", padx=5, pady=5)

        CRSin = StringVar()
        CRSin.set(CRSLIST[0])
        CRSinMenu = OptionMenu(coordInputFrame,CRSin, *CRSLIST)
        CRSinMenu.grid(row=0,column=1)

        inXEntry = Entry(coordInputFrame, width=20)
        inYEntry = Entry(coordInputFrame, width=20)
        outXEntry = Entry(coordInputFrame, width=20)
        outYEntry = Entry(coordInputFrame, width=20)

        suggested_cadnum = StringVar()
        suggested_cadnum.set('')


        def convert(xvalue: str,yvalue: str):
            outXEntry.delete(0,END)
            outYEntry.delete(0,END)
            global coords

            if CRSin.get() == 'UTM Zone 18S':
                try:
                    coords = coordinatePairUTM(float(inXEntry.get()),float(inYEntry.get()))
                    coords.add_lat_long_from_xy()
                    coords.add_sector()
                except ValueError:
                    messagebox.showwarning("Erreur de saisie", "Entrez des coordonnees valides!")
                    outXEntry.delete(0,END)
                    outYEntry.delete(0,END)
                    pass

            else:
                # if not already in UTM, convert to UTM.
                coords = convert_coords(coordinatePairLatLong(str(yvalue),str(xvalue)))
                coords.add_lat_long_from_xy()
                coords.add_sector()

            SectorName.set(coords.sector_name) # type: ignore
            SectorRoot.set(coords.cadnum_root) # type: ignore

            try: 
                Sector = CadasterSector(parent=MyCaveCadaster, name=SectorName.get(), root_cadnum= int(SectorRoot.get())) # type: ignore
            except ValueError:
                messagebox.showwarning("Erreur de saisie", "Entrez des coordonnees valides!")
                Sector = CadasterSector(parent=MyCaveCadaster, name='', root_cadnum= 999) # type: ignore

                pass

            suggested_cadnum.set(str(Sector.next_cad_num))
            outXEntry.insert(0,f"{coords.x:.0f}") # type: ignore
            outYEntry.insert(0,f"{coords.y:.0f}") # type: ignore


        convertButton = Button(coordInputFrame, text="Convertir", command=lambda : convert(inXEntry.get(),inYEntry.get()))

        convertButton.grid(row=0,column=3)


        inXEntry.grid(row=1,column=1)
        inYEntry.grid(row=1,column=3)
        outXEntry.grid(row=2,column=1)
        outYEntry.grid(row=2,column=3)


        Label(coordInputFrame,text = 'X UTM (18S):', font = BOLDFONT).grid(row=2,column = 0)
        Label(coordInputFrame,text = 'Y UTM (18S):', font = BOLDFONT).grid(row=2,column = 2)


        Label(coordInputFrame, text="Secteur", font= BOLDFONT).grid(row=3,column=0)
        outSector = Label(coordInputFrame,textvariable=SectorName)
        outSectorRoot = Label(coordInputFrame,text = "Numéro Cadastral", font=BOLDFONT)
        outNewCadnum = Label(coordInputFrame, textvariable=suggested_cadnum)
        outSector.grid(row=3,column=1)
        outSectorRoot.grid(row=3,column=2)
        outNewCadnum.grid(row=3,column=3)

        plotButton = Button(coordInputFrame, text="Visualisation rapide",
                            command=lambda: controller.show_frame(PlotFrame))
        plotButton.grid(row=4,column=0,columnspan=4)

        coordInputFrame.grid(row=0, column=1,columnspan=3, padx=10,pady=10)


        mainFrame = LabelFrame(self, text= "Entrée des données", padx=5, pady=5)

        ENTRIES_FR : list = ['nom','expedition','commentaire','altitude (m)','explorateurs','développement','profondeur']

        ENTRIES_HEIGHTS : list[int] = [1,1,7,1,4,1,1]
        variables: list[StringVar] = [StringVar(value="undefined") for text in ENTRIES_FR]

        entriesLabels : list[Label]  = [Label(mainFrame,text=text, width = 20, font = BOLDFONT) for text in ENTRIES_FR]
        entriesList : list[Text] = [Text(mainFrame, width=40,height=height, wrap= WORD) for height in ENTRIES_HEIGHTS]
        entriesOutput : list[Label] = [Label(mainFrame, width=40, textvariable=variable, wraplength=300,  justify='left', font=VALIDATED_FONT,padx=10) for variable in variables]


        def validate() -> None:
            """Cycle over the entry fields and display values in another widget"""
            for entry,variable in zip(entriesList,variables):
                variable.set(entry.get("1.0", END))
            
            global Sector
            Sector =  CadasterSector(parent=MyCaveCadaster, name=SectorName.get(), root_cadnum= int(SectorRoot.get())) # type: ignore


        validateButton = Button(mainFrame, text='Valider', command= validate)



        # cycle over entries for the inputs.
        for i,(label,entry,output) in enumerate(zip(entriesLabels, entriesList,entriesOutput)):
            label.grid(row=i,column=0)
            entry.grid(row=i,column=1)
            output.grid(row=i, column=2)

        validateButton.grid(row=len(entriesLabels)+1,column= 3)



        def suggest_cadnum(sector: CadasterSector) -> int:
            """Reads a coordinate pair and returns new cadastral number"""
            return sector.next_cad_num


        class NameTooShort(Exception):
            pass
        def toCamelCase(string: str) -> str:
            if len(string) < 4:
                raise NameTooShort

            split = [to_strip.strip('_') for to_strip in string.split(" ")]
            caps = [to_cap[0].capitalize() + to_cap[1:] for to_cap in split]
            accentedcamelCase : str = ""
            for cap in caps:
                accentedcamelCase+=cap
            
            camelCase = accentedcamelCase.replace("'","").replace("é","e").replace("è","e").replace("ë","e").replace("ê","e").replace("ç","c")
            
            return camelCase 

        def update() ->None:
            try:
                name = toCamelCase(variables[0].get().strip("\n"))
            except NameTooShort:
                name = ""
                messagebox.showwarning("Nom trop court!")
            newCave = Cave(cadnum=str(suggest_cadnum(Sector)),
            exped=assignExpedition(variables[1].get().strip("\n")),
            name= name,
            complete_name= variables[0].get().strip("\n"),
            comment=variables[2].get().strip("\n"),
            altitude=variables[3].get().strip("\n"), 
            explorers=variables[4].get().strip("\n"),
            length=float(variables[5].get()),
            depth=float(variables[6].get()),
            coordinates=coordinatePairUTM(float(outXEntry.get()),float(outYEntry.get())),
            _index= len(MyCaveCadaster.caves)+1,
            ) # type: ignore
            newCave.add_coordinates(newCave.coordinates)
            newCave.make_entry_in_sector_file()
            folder_path.set(newCave._folder_path)
            suggested_cadnum.set(str(Sector.next_cad_num))
            try:
                MyCaveCadaster.check_existing(newCave)
                MyCaveCadaster.add_entry(newCave)
                Sector.add_entry(newCave)

            except CaveExistsError:
                messagebox.showwarning("Erreur de saisie", "Une grotte existe déja à ces coordonnées!")
            try: 
                newCave.make_folder()
            except CalledProcessError:
                messagebox.showwarning("Erreur de saisie", "Il existe deja un dossier pour cette grotte!")

        mainFrame.grid(row=2,column=0,columnspan=3, padx=10,pady=10)

        updateFrame = LabelFrame(self, text='Mise à jour des coordonnées')

        updateButton = Button(updateFrame, text="Ajouter la cavité", command = update)
        updateButton.grid(row=0,column=0, sticky="nw")

         # open file explorer

        folder_path = StringVar()
        folder_path.set("")
        print(folder_path.get().strip("\n"))

        def open_directory(dirname: str)-> None:
            actual_dirname = abspath(dirname)

            try: 
                if exists(actual_dirname):
                    if OS == "LinuxMac":
                        print("using Linux or Mac")
                        check_output(f"open {actual_dirname}", shell=True) # linux or mac
                    elif OS == "Windows":
                        print("using windows")
                        print(actual_dirname)
                        check_output(f"start {actual_dirname}", shell=True) # on windows

            except CalledProcessError:
                raise
        openButton = Button(updateFrame,text="Ouvrir le dossier",  command = lambda : open_directory(folder_path.get().strip("\n")))
        openButton.grid(row=0,column=2)


        


        updateFrame.grid(row=3,column=0,columnspan=2, padx=10,pady=10)

class PlotFrame(Frame):

    def __init__(self, parent,controller):
        Frame.__init__(self,parent)

        # go back to the add frame window
        button1 = Button(self , text="Retour",
                            command=lambda: controller.show_frame(AddFrame))
        button1.grid(row=1,column=0)

        plotFrame = LabelFrame(self, text= "Visualisation rapide", padx=5, pady=5)
        # plot the cave location. 
       
        def plot4km():
            return plot(0.0279793174)

        def plot50m():
            return plot(0.000349718)

        def plot250m():
            return plot(0.00174859)

        def plot1km():
            return plot(0.006994382)

        def plot(scale):
            cadastre = MyCaveCadaster
            global SatMapPlot
            SatMapPlot = SatelliteMapPlot(600,400,300,scale=scale)
            SatMapPlot.add_points(cadastre)

            SatMapPlot.add_point_to_plot(coords._orig_long,coords._orig_lat)
  
            # the figure that will contain the plot

            fig, ax = SatMapPlot.plot_map()

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            global canvas
            canvas = FigureCanvasTkAgg(fig,
                               master = self)  
            for item in canvas.get_tk_widget().find_all():
                canvas.get_tk_widget().delete(item)

            canvas.draw()

            
  
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().grid(row=2, column= 0 )
        
        plot_button00 = Button(master = plotFrame, 
                     command = plot50m,
                     height = 2, 
                     width = 20,
                     text = "Visualisation 50 m")

        plot_button0 = Button(master = plotFrame, 
                     command = plot250m,
                     height = 2, 
                     width = 20,
                     text = "Visualisation 250 m")

        plot_button1 = Button(master = plotFrame, 
                     command = plot1km,
                     height = 2, 
                     width = 20,
                     text = "Visualisation 1 km")

        plot_button2 = Button(master = plotFrame, 
                     command = plot4km,
                     height = 2, 
                     width = 20,
                     text = "Visualisation 4 km")
  
                # place the button 

        def savefig(widget,fp):

            timenow = time.localtime()
            timestamp = f"{timenow.tm_year}-{timenow.tm_mon}-{timenow.tm_mday}_{timenow.tm_hour}-{timenow.tm_min}-{timenow.tm_sec}"
            scale =  2000 * (np.cos(50*np.pi/180) * 6370*2*np.pi /360 * SatMapPlot.scale)
            plt.savefig(abspath(fp+"/capture-"+timestamp+f"-{scale:.0f}m"+".png"),dpi=300)

        # in main window
        plot_button00.grid(row=0,column=0)
        plot_button0.grid(row=0,column=1)
        plot_button1.grid(row=0,column=2)
        plot_button2.grid(row=0,column=3)
        savepath = StringVar()
        savepath.set("../therion/outputs/")
        saveButton = Button(padx=10,pady=10,master=plotFrame,width=20,text = "Sauvegarder",command= lambda: savefig(canvas.get_tk_widget(),savepath.get()))
        
        saveButton.grid(row=1,column=0)

        plotFrame.grid(row=0,column=0,sticky="nw")

class ConvertVisualFrame(Frame):

     def __init__(self, parent,controller):
        Frame.__init__(self,parent)

        def convert_file() -> None:
            #global chosen_file
            chosen_file =  filedialog.askopenfilename(
                initialdir="./therion/data", 
                title="Selectionner un fichier", 
                filetypes=(("Fichiers VisualTopo", "*.tro"),("Tous fichiers", "*.*"))
            )
            input_file = abspath(chosen_file)
            if (chosen_file != "" and chosen_file != None) and ".tro" in chosen_file:
                answer = simpledialog.askstring("Entrée de données","Entrer le nom cadastral de la cavité", parent=self)
                if answer is not None:
                    check_output(f'python {abspath("visual_therion.py")} "{input_file}" {answer}', shell=True)
                else: 
                    messagebox.showwarning("Erreur de saisie", "Le nom choisi n'est pas valide!")

        ConvertButton = Button(self,text="Convertir",command= convert_file)
        ConvertButton.grid(row=0,column=0)

        ReturnButton = Button(self, text = "retour", command=lambda: controller.show_frame(StartPage))
        ReturnButton.grid(row=1,column=0)


app = CaveDatabaseApp()

app.title("Base de Données Ultima Patagonia")
app.geometry("1000x800")
app.iconbitmap("logo-icon.ico")
app.mainloop()