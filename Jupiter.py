import numpy as np
from Astronomic_objects import Body, System

### CONSTANTES ###
G = 6.67430e-11  # Constante gravitationnelle (m^3/kg/s^2)
MJ = 1.898e27    # Masse de Jupiter (kg)
AU = 1.496e8     # 1 Unité Astronomique en kilomètres (km)
YEAR = 365.25 * 24 * 3600  # Une année en secondes
DAY = 24 * 3600  # Un jour en secondes

# Constantes spécifiques pour les lunes galiléennes
RJ = 71492  # Rayon de Jupiter en kilomètres

# Calcul de la vitesse orbitale en km/s pour correspondre aux positions en km
def orbital_velocity(mass_jupiter, orbital_radius_km):
    G_km_s2 = G * 1e-9  # Constante gravitationnelle en km^3/kg/s^2
    return np.sqrt(G_km_s2 * mass_jupiter / orbital_radius_km)

# Fonction pour calculer les positions et les vitesses en fonction de l'inclinaison
def apply_inclination(position, velocity, inclination_deg):
    inclination_rad = np.radians(inclination_deg)
    
    # Matrice de rotation autour de l'axe x (pour incliner l'orbite)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(inclination_rad), -np.sin(inclination_rad)],
        [0, np.sin(inclination_rad), np.cos(inclination_rad)]
    ])
    
    # Appliquer la rotation à la position et à la vitesse
    rotated_position = np.dot(rotation_matrix, position)
    rotated_velocity = np.dot(rotation_matrix, velocity)
    
    return rotated_position, rotated_velocity

### DEFINITION DES CORPS ###

# Jupiter
Jupiter = Body(Name='Jupiter',
               Position=np.array([[0.0], [0.0], [0.0]]),  # Jupiter au centre
               Velocity=np.array([[0.0], [0.0], [0.0]]),  # Jupiter immobile au centre du système
               Mass=MJ,
               Radius=RJ,
               Temperature=165,  # Température moyenne de Jupiter en K
               Albedo=0.52,
               Emissivity=0.95,
               Color='orange')

# Lunes Galiléennes avec inclinaison des orbites en degrés
inclinations = {
    'Io': 0.036,        # Inclinaison en degrés
    'Europe': 0.47,     # Inclinaison en degrés
    'Ganymede': 0.2,    # Inclinaison en degrés
    'Callisto': 2.02    # Inclinaison en degrés
}

# Io
Io_position = np.array([[421700], [0.0], [0.0]])
Io_velocity = np.array([[0.0], [orbital_velocity(MJ, 421700)], [0.0]])
Io_position, Io_velocity = apply_inclination(Io_position, Io_velocity, inclinations['Io'])

Io = Body(Name='Io',
          Position=Io_position,
          Velocity=Io_velocity,
          Mass=8.9319e22,  # Masse de Io en kg
          Radius=1821.6,  # Rayon de Io en km
          Temperature=130,  # Température moyenne de Io en K
          Albedo=0.63,
          Emissivity=0.95,
          Color='red')

# Europe
Europe_position = np.array([[671034], [0.0], [0.0]])
Europe_velocity = np.array([[0.0], [orbital_velocity(MJ, 671034)], [0.0]])
Europe_position, Europe_velocity = apply_inclination(Europe_position, Europe_velocity, inclinations['Europe'])

Europe = Body(Name='Europe',
              Position=Europe_position,
              Velocity=Europe_velocity,
              Mass=4.7998e22,  # Masse de Europe en kg
              Radius=1560.8,  # Rayon de Europe en km
              Temperature=102,  # Température moyenne de Europe en K
              Albedo=0.68,
              Emissivity=0.95,
              Color='cyan')

# Ganymède
Ganymede_position = np.array([[1070400], [0.0], [0.0]])
Ganymede_velocity = np.array([[0.0], [orbital_velocity(MJ, 1070400)], [0.0]])
Ganymede_position, Ganymede_velocity = apply_inclination(Ganymede_position, Ganymede_velocity, inclinations['Ganymede'])

Ganymede = Body(Name='Ganymede',
                Position=Ganymede_position,
                Velocity=Ganymede_velocity,
                Mass=1.4819e23,  # Masse de Ganymède en kg
                Radius=2634.1,  # Rayon de Ganymède en km
                Temperature=110,  # Température moyenne de Ganymède en K
                Albedo=0.43,
                Emissivity=0.95,
                Color='blue')

# Callisto
Callisto_position = np.array([[1882700], [0.0], [0.0]])
Callisto_velocity = np.array([[0.0], [orbital_velocity(MJ, 1882700)], [0.0]])
Callisto_position, Callisto_velocity = apply_inclination(Callisto_position, Callisto_velocity, inclinations['Callisto'])

Callisto = Body(Name='Callisto',
                Position=Callisto_position,
                Velocity=Callisto_velocity,
                Mass=1.0759e23,  # Masse de Callisto en kg
                Radius=2410.3,  # Rayon de Callisto en km
                Temperature=134,  # Température moyenne de Callisto en K
                Albedo=0.19,
                Emissivity=0.95,
                Color='gray')

### SIMULATION DU SYSTEME ###

# Système avec Jupiter et ses lunes
Jupiter_System = System([Jupiter, Io, Europe, Ganymede, Callisto])

# Simulation du système sur 100 jours avec 10000 étapes pour une précision élevée
Jupiter_System.Simulation(Time=100 * DAY, Nb_step=10000)

# Animation du système sur 10 secondes
Jupiter_System.Animation(Animated_time=60,trail = 0.05,anim_temps = False, fixed = 0)
