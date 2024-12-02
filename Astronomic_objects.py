import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.animation import FuncAnimation

### CONSTANTES ###
G = 6.6743015e-11  # Constante gravitationnelle [m3/kg/s2]
YEAR = 365.25 * 24 * 3600  # Une année en secondes

### CLASS BODY ###
class Body:
    """
    Classe représentant un corps céleste.
    """
    def __init__(self, Name, Position, Velocity, Mass, Radius, Temperature, Albedo, Emissivity, Color):
        self.Name = Name  # Nom du corps
        self.Position = Position  # Position initiale [km]
        self.Velocity = Velocity  # Vitesse initiale [km/s]
        self.Mass = Mass  # Masse [kg]
        self.Radius = Radius  # Rayon [km]
        self.Albedo = Albedo  # Albedo du corps
        self.Emissivity = Emissivity  # Émissivité thermique
        self.Temperature = Temperature  # Température initiale [K]
        self.Thermic_Radiation_Resultant = 0  # Radiation thermique résultante
        self.Force_Resultant = 0  # Force résultante due à la gravitation
        self.Color = Color  # Couleur pour l'affichage

### CLASS SYSTEM ###
class System:
    """
    Classe représentant un système de corps célestes et les lois physiques régissant leurs interactions.
    """
    def __init__(self, Elements):
        self.Elements = Elements  # Liste des corps du système
        self.Time = 0  # Temps initialisé à 0
        self.Trajectories = {}  # Dictionnaire pour stocker les trajectoires
        self.Temperatures = {}  # Dictionnaire pour stocker les températures
        self.animations = {}  # Dictionnaire pour stocker les animations
        self.max_size = max([np.log(element.Radius) for element in Elements])
        self.min_size = min([np.log(element.Radius) for element in Elements])

    def Init_Data(self, Time, Nb_step):
        """
        Initialise les données pour la simulation.
        """
        self.Time = np.linspace(0.0, Time/YEAR, Nb_step)
        for element in self.Elements:
            self.Trajectories[element.Name] = np.zeros((3, Nb_step))  # Trajectoires (x, y, z)
            self.Temperatures[element.Name] = np.zeros(Nb_step)  # Températures en fonction du temps

    def Save_Data(self, k):
        """
        Enregistre les données de position et de température à chaque étape.
        """
        for element in self.Elements:
            self.Trajectories[element.Name][:, k] = np.ravel(element.Position)  # Enregistre la position
            self.Temperatures[element.Name][k] = element.Temperature  # Enregistre la température

    def Gravitation_law(self):
        """
        Calcule la force gravitationnelle agissant sur chaque corps.
        """
        for i in self.Elements:
            force_sum = 0
            for j in self.Elements:
                if j != i:
                    dvec = (i.Position - j.Position) * 1e3  # Distance en mètres
                    dnorm = np.linalg.norm(dvec)  # Norme de la distance
                    force_sum += i.Mass * j.Mass * dvec / (dnorm ** 3)  # Loi de gravitation
            i.Force_Resultant = -G * force_sum  # Force résultante sur le corps i

    def Thermic_Radiation_law(self):
        """
        Calcule la radiation thermique agissant sur chaque corps.
        """
        for i in self.Elements:
            if i.Albedo != 1.0:  # Si le corps n'est pas parfaitement réfléchissant
                rad_sum = 0
                for j in self.Elements:
                    if j != i:
                        dvec = (i.Position - j.Position) * 1e3  # Distance en mètres
                        dnorm = np.linalg.norm(dvec)  # Norme de la distance
                        rad_sum += (j.Radius * 1e3 / dnorm) ** 2 * j.Temperature ** 4
                i.Thermic_Radiation_Resultant = (1 - i.Albedo) / (4 * i.Emissivity) * rad_sum
            else:
                i.Thermic_Radiation_Resultant = i.Temperature ** 4

    def Transition(self, Time_step):
        """
        Met à jour la position, la vitesse et la température des corps en fonction des lois physiques.
        """
        for element in self.Elements:
            # Mise à jour de la vitesse en fonction de la force gravitationnelle
            element.Velocity += Time_step * element.Force_Resultant / element.Mass / 1e3  # Vitesse en km/s
            # Mise à jour de la position en fonction de la vitesse
            element.Position += Time_step * element.Velocity
            # Mise à jour de la température en fonction de la radiation thermique
            element.Temperature = element.Thermic_Radiation_Resultant ** (1 / 4)

    def Display_Trajectory(self, step):
        """
        Affiche les trajectoires des corps dans un graphe 3D.
        """
        fig = plt.figure('Trajectories')
        ax = fig.add_subplot(projection="3d")
        plt.title('Trajectories')

        for element in self.Elements:
            # Trace la trajectoire complète
            ax.plot3D(*self.Trajectories[element.Name], linestyle='dashed', color=element.Color)
            # Affiche la position actuelle
            ax.plot3D(self.Trajectories[element.Name][0, step],
                      self.Trajectories[element.Name][1, step],
                      self.Trajectories[element.Name][2, step],
                      marker='o', color=element.Color, label=element.Name)
        ax.legend()

    def Display_Temperature(self, Time, Nb_step):
        """
        Affiche les températures des corps en fonction du temps.
        """
        for element in self.Elements:
            plt.figure(f'Temperature of {element.Name}')
            plt.title(f'Temperature of {element.Name}')
            plt.xlabel('Time [s]')
            plt.ylabel('Temperature [°C]')
            plt.plot(np.linspace(0, Time, Nb_step),
                     self.Temperatures[element.Name] - 273, linestyle='solid', color=element.Color)

    def Simulation(self, Time, Nb_step):
        """
        Lance la simulation du système pour une durée donnée.
        """
        Time_step = Time / Nb_step
        self.Init_Data(Time, Nb_step)

        for k in tqdm(range(Nb_step)):
            self.Gravitation_law()
            self.Thermic_Radiation_law()
            self.Transition(Time_step)
            self.Save_Data(k)

    def set_lim_traj(self, ax):
        """
        Définit les limites des axes pour l'affichage des trajectoires en 3D.
        """
        min_pos, max_pos = np.inf, -np.inf
        for element in self.Elements:
            min_pos = min(min_pos, np.min(self.Trajectories[element.Name]))
            max_pos = max(max_pos, np.max(self.Trajectories[element.Name]))

        ax.set_xlim([min_pos, max_pos])
        ax.set_ylim([min_pos, max_pos])
        ax.set_zlim([min_pos, max_pos])
        ax.set_xlabel('X [km]')
        ax.set_ylabel('Y [km]')
        ax.set_zlabel('Z [km]')

    def center_elements(self, fixed):
        """
        Centre les trajectoires sur un élément spécifique.
        """
        if fixed is None:
            return
        
        print('Setting reference point to '+self.Elements[fixed].Name)
        for element in self.Elements:
            # Déplacer les trajectoires de tous les autres éléments pour centrer le repère
            if element.Name != self.Elements[fixed].Name:
                self.Trajectories[element.Name] -= self.Trajectories[self.Elements[fixed].Name]
        self.Trajectories[self.Elements[fixed].Name] = np.zeros((3, len(self.Time)))

    def Animation(self, Animated_time, trail=1.0, anim_temps=True, fixed=None):
        """
        Crée une animation des trajectoires et des températures des corps sur une période donnée.
        """
        Nb_step = len(self.Time)
        Animated_time = min(Animated_time, Nb_step / 60)
        Nb_frames = int(60 * Animated_time)
        Time_step = 1e3 / 60
        ratio = Nb_step / Nb_frames

        # Centrer les éléments si nécessaire
        self.center_elements(fixed)
        
        ### Animation des trajectoires ###
        fig = plt.figure('Trajectories')
        ax = fig.add_subplot(projection="3d")
        self.set_lim_traj(ax)
        ax.set_title('Trajectories')
        px_max = 10
        px_min = 2
        a = (px_max - px_min) / (self.max_size - self.min_size)
        b = self.max_size - px_max / a

        traj_lines = [ax.plot([], [], [], linestyle='dashed', color=element.Color)[0] for element in self.Elements]
        if self.max_size==self.min_size:
            traj_objects = [ax.plot([], [], [], marker='o', markersize=int((px_min+px_max)/2), color=element.Color, label=element.Name)[0] for element in self.Elements]
        else:
            traj_objects = [ax.plot([], [], [], marker='o', markersize=int(a * (np.log(element.Radius) - b)), color=element.Color, label=element.Name)[0] for element in self.Elements]
        ax.legend()

        def update_trajectories(frame):
            """
            Met à jour les trajectoires pour chaque frame d'animation.
            """
            for line, obj, element in zip(traj_lines, traj_objects, self.Elements):
                idx_start = int(frame * ratio * (1 - trail))
                idx_end = int(frame * ratio)
                line.set_data_3d(self.Trajectories[element.Name][:, idx_start:idx_end])
                obj.set_data_3d(self.Trajectories[element.Name][:, idx_end].reshape(3, 1))
            return traj_lines + traj_objects

        ani_traj = FuncAnimation(fig, update_trajectories, frames=Nb_frames, interval=Time_step, blit=True)

        ### Animation des températures ###
        if anim_temps:
            fig_temps, ax_temps, lines_temps = {}, {}, {}

            for element in self.Elements:
                fig_temps[element.Name] = plt.figure(f'{element.Name} Temperature', figsize=(6, 4))
                ax_temps[element.Name] = fig_temps[element.Name].add_subplot(111)
                ax_temps[element.Name].set_xlim([np.min(self.Time), np.max(self.Time)])
                if element.Albedo != 1.0:  # La température de l'étoile est constante
                    ax_temps[element.Name].set_ylim([np.min(self.Temperatures[element.Name] - 273.0), np.max(self.Temperatures[element.Name] - 273.0)])
                else:
                    ax_temps[element.Name].set_ylim([np.min(self.Temperatures[element.Name] - 323.0), np.max(self.Temperatures[element.Name] - 223.0)])
                ax_temps[element.Name].set_xlabel('Time [Year]')
                ax_temps[element.Name].set_ylabel('Temperature [°C]')
                ax_temps[element.Name].set_title(f'{element.Name} Temperature')
                lines_temps[element.Name], = ax_temps[element.Name].plot([], [], color=element.Color)

            def update_temp(frame):
                """
                Met à jour les données de température pour chaque frame d'animation.
                """
                idx = int(frame * ratio)
                for element in self.Elements:
                    t_data = self.Time[:idx]
                    temp_data = self.Temperatures[element.Name][:idx] - 273
                    lines_temps[element.Name].set_data(t_data, temp_data)
                return list(lines_temps.values())

            ani_temp = FuncAnimation(fig_temps[element.Name], update_temp, frames=Nb_frames, interval=Time_step, blit=True)

        plt.show()
