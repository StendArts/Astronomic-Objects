from Astronomic_objects import *

### DEFINITION DES CONSTANTES ###

UA = 147e6
MS = 1.98892e30
MT = 5.972e24
AN = 365*24*3600

### DEFINITION DES CORPS ###

CentoriA = Body(Name = 'Centori A',
              Position = np.array([[0.0],[0.0],[0.0]]),
              Velocity = np.array([[0.0],[0.0],[0.0]]),
              Mass = 1.1*MS,
              Radius = 696340*1.227,
              Temperature = 5800,
              Albedo = 1,
              Emissivity = 0.95,
              Color = 'gold')

r12 = 25 * UA
v12 = np.sqrt(G * (CentoriA.Mass) / r12)

CentoriB= Body(Name = 'Centori B',
              Position = np.array([[r12],[0.0],[0.0]])*UA,
              Velocity = np.array([[0.0],[v12],[0.0]]),
              Mass = 0.907*MS,
              Radius = 696340*0.865,
              Temperature = 5260,
              Albedo = 1,
              Emissivity = 0.95,
              Color = 'goldenrod')

r13 = 60 * UA
v13 = np.sqrt(G * (CentoriA.Mass + CentoriB.Mass) / r13)

CentoriC = Body(Name = 'Centori C',
              Position = np.array([[r13],[0.0],[0.0]])*UA,
              Velocity = np.array([[0.0],[v13],[0.0]]),
              Mass = 0.1221*MS,
              Radius = 696340*0.1542,
              Temperature = 3042,
              Albedo = 1,
              Emissivity = 0.95,
              Color = 'darkred')

r_planet = 1 * UA
v_planet = np.sqrt(G * CentoriA.Mass / r_planet)

Proxima = Body(Name = 'Proxima b',
            Position = np.array([[r_planet],[0.0],[0.0]])*UA,
            Velocity = np.array([[0.0],[v_planet],[0.0]]),
            Mass = 1.17*MT,
            Radius = 1737.4,
            Temperature = 250,
            Albedo = 0.1054,
            Emissivity = 0.95,
            Color = 'blue')

### SIMULATION DU SYSTEME ###

Trisolaris = System([CentoriA,CentoriB,CentoriC,Proxima])
Trisolaris.Simulation(Time = 100*AN, Nb_step = 1000)
Trisolaris.Animation(Animated_time = 5)