import numpy as np
from Astronomic_objects import Body, System

### CONSTANTES ###
G = 6.67430e-11  # Constante gravitationnelle (m^3/kg/s^2)
MS = 1.98892e30  # Masse du Soleil (kg)
AU = 1.496e8     # 1 Unité Astronomique en kilomètres (km)
YEAR = 365.25 * 24 * 3600  # Une année en secondes
EARTH_MASS = 5.972e24  # Masse de la Terre en kg
JUPITER_MASS = 1.898e27  # Masse de Jupiter en kg

# Calcul de la vitesse orbitale en km/s pour correspondre aux positions en km
def orbital_velocity(mass_sun, orbital_radius_km):
    G_km_s2 = G * 1e-9  # Constante gravitationnelle en km^3/kg/s^2
    return np.sqrt(G_km_s2 * mass_sun / orbital_radius_km)

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

# Soleil
Soleil = Body(Name='Sun',
              Position=np.array([[0.0], [0.0], [0.0]]),  # Soleil au centre
              Velocity=np.array([[0.0], [0.0], [0.0]]),  # Soleil immobile
              Mass=MS,
              Radius=696340,
              Temperature=5778,  # Température moyenne du Soleil
              Albedo=1.0,
              Emissivity=0.95,
              Color='gold')

# Inclinaisons des orbites des planètes en degrés (par rapport à l'écliptique)
inclinations = {
    'Mercure': 7.0,
    'Vénus': 3.39,
    'Terre': 0.0,
    'Mars': 1.85,
    'Jupiter': 1.31,
    'Saturne': 2.49,
    'Uranus': 0.77,
    'Neptune': 1.77,
    'Pluton': 17.2  # Optionnel, car Pluton n'est plus considérée comme une planète principale
}

# Paramètres des planètes du système solaire (distance en AU, masse en kg, rayon en km, inclinaison)
planets_params = {
    'Mercure': {'distance': 0.39, 'mass': 3.285e23, 'radius': 2439.7, 'temperature': 440, 'color': 'gray'},
    'Vénus': {'distance': 0.72, 'mass': 4.867e24, 'radius': 6051.8, 'temperature': 737, 'color': 'orange'},
    'Terre': {'distance': 1.00, 'mass': 5.972e24, 'radius': 6371, 'temperature': 288, 'color': 'royalblue'},
    'Mars': {'distance': 1.52, 'mass': 6.39e23, 'radius': 3389.5, 'temperature': 210, 'color': 'red'},
    'Jupiter': {'distance': 5.20, 'mass': 1.898e27, 'radius': 69911, 'temperature': 165, 'color': 'chocolate'},
    'Saturne': {'distance': 9.58, 'mass': 5.683e26, 'radius': 58232, 'temperature': 134, 'color': 'darksalmon'},
    'Uranus': {'distance': 19.22, 'mass': 8.681e25, 'radius': 25362, 'temperature': 76, 'color': 'cyan'},
    'Neptune': {'distance': 30.05, 'mass': 1.024e26, 'radius': 24622, 'temperature': 72, 'color': 'blue'},
    'Pluton': {'distance': 39.48, 'mass': 1.309e22, 'radius': 1188.3, 'temperature': 44, 'color': 'brown'}  # Optionnel
}

### CREATION DES PLANETES ###

planets = []

for planet_name, params in planets_params.items():
    distance_au = params['distance']
    distance_km = distance_au * AU
    mass = params['mass']
    radius = params['radius']
    temperature = params['temperature']
    color = params['color']
    inclination = inclinations.get(planet_name, 0.0)
    
    # Position et vitesse initiales dans le plan de l'écliptique
    position = np.array([[distance_km], [0.0], [0.0]])
    velocity = np.array([[0.0], [orbital_velocity(MS, distance_km)], [0.0]])
    
    # Appliquer l'inclinaison
    position, velocity = apply_inclination(position, velocity, inclination)
    
    # Création de l'objet planète
    planet = Body(Name=planet_name,
                  Position=position,
                  Velocity=velocity,
                  Mass=mass,
                  Radius=radius,
                  Temperature=temperature,
                  Albedo=0.3,
                  Emissivity=0.95,
                  Color=color)
    
    planets.append(planet)

### AJOUT DE LA LUNE ET DES LUNES DE JUPITER ###

# Lune de la Terre
moon_distance_km = 384400  # Distance Terre-Lune en km
moon_velocity_km_s = orbital_velocity(EARTH_MASS, moon_distance_km)
moon_inclination = 5.14  # Inclinaison orbitale de la Lune par rapport à l'écliptique

# Position et vitesse de la Lune par rapport à la Terre
moon_position = np.array([[moon_distance_km], [0.0], [0.0]])
moon_velocity = np.array([[0.0], [moon_velocity_km_s], [0.0]])

# Appliquer l'inclinaison à la Lune
moon_position, moon_velocity = apply_inclination(moon_position, moon_velocity, moon_inclination)

Lune = Body(Name='Moon',
            Position=planets[2].Position + moon_position,  # Terre + Lune
            Velocity=planets[2].Velocity + moon_velocity,  # Terre + Lune
            Mass=7.34767309e22,
            Radius=1737.4,
            Temperature=273,
            Albedo=0.12,
            Emissivity=0.95,
            Color='lightgray')

# Lunes galiléennes de Jupiter
jupiter_moons_params = {
    'Io': {'distance': 421700, 'mass': 8.9319e22, 'radius': 1821.6, 'inclination': 0.05, 'color': 'gold'},
    'Europe': {'distance': 671034, 'mass': 4.7998e22, 'radius': 1560.8, 'inclination': 0.47, 'color': 'lightblue'},
    'Ganymede': {'distance': 1070400, 'mass': 1.4819e23, 'radius': 2634.1, 'inclination': 0.2, 'color': 'gray'},
    'Callisto': {'distance': 1882700, 'mass': 1.0759e23, 'radius': 2410.3, 'inclination': 0.28, 'color': 'darkgray'}
}

jupiter_moons = []

for moon_name, params in jupiter_moons_params.items():
    moon_distance_km = params['distance']
    moon_mass = params['mass']
    moon_radius = params['radius']
    moon_inclination = params['inclination']
    moon_color = params['color']
    
    # Calcul de la vitesse orbitale
    moon_velocity_km_s = orbital_velocity(JUPITER_MASS, moon_distance_km)
    
    # Position et vitesse de la lune par rapport à Jupiter
    moon_position = np.array([[moon_distance_km], [0.0], [0.0]])
    moon_velocity = np.array([[0.0], [moon_velocity_km_s], [0.0]])
    
    # Appliquer l'inclinaison
    moon_position, moon_velocity = apply_inclination(moon_position, moon_velocity, moon_inclination)
    
    # Création de l'objet lune
    moon = Body(Name=moon_name,
                Position=planets[4].Position + moon_position,  # Jupiter + lune
                Velocity=planets[4].Velocity + moon_velocity,  # Jupiter + lune
                Mass=moon_mass,
                Radius=moon_radius,
                Temperature=100,
                Albedo=0.3,
                Emissivity=0.95,
                Color=moon_color)
    
    jupiter_moons.append(moon)

### SIMULATION DU SYSTEME SOLAIRE ###

# Inclure le Soleil, les planètes, la Lune et les lunes de Jupiter dans le système
solar_system = System([Soleil] + planets + [Lune] + jupiter_moons)

# Simulation sur 1 an avec 10000 étapes pour une précision adéquate
solar_system.Simulation(Time=10 * YEAR, Nb_step=10000)

# Animation du système sur 10 secondes
solar_system.Animation(Animated_time=60, trail = 0.02, anim_temps=False, fixed = 0)
