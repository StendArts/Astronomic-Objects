from Astronomic_objects import *

### DEFINITION DES CORPS ###

Soleil = Body(Name = 'Sun',
              Position = np.array([[0.0],[0.0],[0.0]]),
              Velocity = np.array([[0.0],[0.0],[0.0]]),
              Mass = 1.98892e30,
              Radius = 696340,
              Temperature = 5772,
              Albedo = 1,
              Emissivity = 0.95,
              Color = 'gold')

Terre = Body(Name = 'Earth',
             Position = np.array([[147e6],[0.0],[0.0]]),
             Velocity = np.array([[0.0],[30],[0.0]]),
             Mass = 5.972e24,
             Radius = 6371,
             Temperature = 286.7,
             Albedo = 0.01054,
             Emissivity = 0.95,
             Color = 'b')

Lune = Body(Name = 'Moon',
            Position = np.array([[147361141],[32485],[0.0]]),
            Velocity = np.array([[0.0],[30.965],[0.0]]),
            Mass = 7.36e22,
            Radius = 1737.4,
            Temperature = 250,
            Albedo = 0.1054,
            Emissivity = 0.95,
            Color = 'gray')

### SIMULATION DU SYSTEME ###

Helios = System([Soleil,Terre,Lune])

Helios.Simulation(Time = 365*24*3600, Nb_step = 365)
Helios.Animation(Animated_time = 2,trail=0.5,anim_temps = False, fixed = 1)