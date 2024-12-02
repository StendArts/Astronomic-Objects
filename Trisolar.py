import numpy as np
from Astronomic_objects import Body, System

### CONSTANTES ###
G = 6.67430e-11  # Constante gravitationnelle (m^3/kg/s^2)
MS = 1.98892e30  # Masse du Soleil (kg)
AU = 1.496e8    # 1 Unité Astronomique en kilomètres (km)
YEAR = 365.25 * 24 * 3600  # Une année en secondes

### POSITIONS ET VITESSES INITIALES ADAPTEES ###
# Les valeurs ici sont choisies pour la solution en huit
# Utilisées pour maintenir la stabilité de la solution

# Ces valeurs sont basées sur des études numériquement précises de la solution en "8" du problème à trois corps
scale_factor = 3.35  # Pour ajuster l'échelle globale de la simulation

# Initial positions (en unités de AU pour une meilleure lisibilité)
positions = scale_factor * np.array([[0.97000436, -0.24308753, 0.0],
                                     [-0.97000436, 0.24308753, 0.0],
                                     [0.0, 0.0, 0.0]]) * AU

# Initial velocities (en unités de AU par an pour correspondre à la position)
velocities = scale_factor * np.array([[0.466203685, 0.43236573, 0.0],
                                      [0.466203685, -0.43236573, 0.0],
                                      [-0.93240737, -0.86473146, 0.0]]) * (AU / YEAR)

### CREATION DES CORPS ###
# Les trois étoiles ont la même masse
mass_star = MS  # Masse du Soleil

# Création des corps avec les nouvelles conditions initiales
Star1 = Body(Name='Star1',
             Position=positions[0].reshape(3, 1),  # Position initiale de l'étoile 1
             Velocity=velocities[0].reshape(3, 1),  # Vitesse initiale de l'étoile 1
             Mass=mass_star,
             Radius=696340,  # Rayon en km
             Temperature=5772,  # Température en Kelvin
             Albedo=1,
             Emissivity=0.95,
             Color='r')

Star2 = Body(Name='Star2',
             Position=positions[1].reshape(3, 1),  # Position initiale de l'étoile 2
             Velocity=velocities[1].reshape(3, 1),  # Vitesse initiale de l'étoile 2
             Mass=mass_star,
             Radius=696340,
             Temperature=5772,
             Albedo=1,
             Emissivity=0.95,
             Color='g')

Star3 = Body(Name='Star3',
             Position=positions[2].reshape(3, 1),  # Position initiale de l'étoile 3 (au centre)
             Velocity=velocities[2].reshape(3, 1),  # Vitesse initiale de l'étoile 3
             Mass=mass_star,
             Radius=696340,
             Temperature=5772,
             Albedo=1,
             Emissivity=0.95,
             Color='b')

### SIMULATION DU SYSTEME ###

# Créer le système avec les trois étoiles
Trisolaire = System([Star1, Star2, Star3])

# Simulation du système sur 10 ans avec 10000 étapes pour plus de précision temporelle
Trisolaire.Simulation(Time=25 * YEAR, Nb_step=25000)

# Animation du système sur 10 secondes
Trisolaire.Animation(Animated_time=5,trail = 0.2,anim_temps = False)
