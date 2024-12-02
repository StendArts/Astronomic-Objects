import numpy as np
from Astronomic_objects import Body, System

### CONSTANTES ###
G = 6.67430e-11  # Constante gravitationnelle (m^3/kg/s^2)
MS = 1.98892e30  # Masse du Soleil (kg)
AU = 1.496e8    # 1 Unité Astronomique en kilomètres (km)
YEAR = 365.25 * 24 * 3600  # Une année en secondes

# Calcul de la vitesse orbitale en km/s pour correspondre aux positions en km
def orbital_velocity(mass_sun, orbital_radius_km):
    G_km_s2 = G * 1e-9  # Constante gravitationnelle en km^3/kg/s^2
    return np.sqrt(G_km_s2 * mass_sun / orbital_radius_km)

# Fonction pour appliquer l'inclinaison (rotation autour de l'axe x)
def apply_inclination(position, velocity, inclination_degrees):
    inclination_radians = np.radians(inclination_degrees)
    # Matrice de rotation autour de l'axe x
    rotation_matrix = np.array([[1, 0, 0],
                                [0, np.cos(inclination_radians), -np.sin(inclination_radians)],
                                [0, np.sin(inclination_radians),  np.cos(inclination_radians)]])
    # Appliquer la rotation à la position et à la vitesse
    position_inclined = np.dot(rotation_matrix, position)
    velocity_inclined = np.dot(rotation_matrix, velocity)
    return position_inclined, velocity_inclined

### DEFINITION DES CORPS ###
# Masse des étoiles et de la planète
mass_gamma_ceph_a = 1.05 * MS  # Gamma Cephei A (kg)
mass_gamma_ceph_b = 0.4 * MS   # Gamma Cephei B (kg)
mass_planet = 1.7 * 1.898e27    # Masse approximative de Jupiter (kg)

# Inclinaisons (en degrés)
inclination_b = 119.3  # Inclinaison de Gamma Cephei B
inclination_planet = 0.0  # Inclinaison de la planète

# Positions et vitesses initiales
# Les positions sont données en km et les vitesses en km/s

# Gamma Cephei A
gamma_ceph_a = Body(Name='Gamma Cephei A',
                    Position=np.array([[0.0], [0.0], [0.0]]) * AU,
                    Velocity=np.array([[0.0], [0.0], [0.0]]),
                    Mass=mass_gamma_ceph_a,
                    Radius=1.2 * 696340,  # Rayon en km
                    Temperature=4900,    # Température en K
                    Albedo=1.0,
                    Emissivity=0.95,
                    Color='r')

# Gamma Cephei B
# Distance approximative : 19.56 AU
distance_to_gamma_ceph_a_km = 19.56 * AU
velocity_gamma_ceph_b = orbital_velocity(mass_gamma_ceph_a, distance_to_gamma_ceph_a_km)

position_b = np.array([[distance_to_gamma_ceph_a_km], [0.0], [0.0]])
velocity_b = np.array([[0.0], [velocity_gamma_ceph_b], [0.0]])

# Appliquer l'inclinaison à Gamma Cephei B
position_b_inclined, velocity_b_inclined = apply_inclination(position_b, velocity_b, inclination_b)

gamma_ceph_b = Body(Name='Gamma Cephei B',
                    Position=position_b_inclined,
                    Velocity=velocity_b_inclined,
                    Mass=mass_gamma_ceph_b,
                    Radius=0.7 * 696340,  # Rayon en km
                    Temperature=3500,    # Température en K
                    Albedo=1.0,
                    Emissivity=0.95,
                    Color='b')

# Planète en orbite autour de Gamma Cephei A
orbital_radius_planet_km = 1.9 * AU
orbital_velocity_planet = orbital_velocity(mass_gamma_ceph_a, orbital_radius_planet_km)

position_planet = np.array([[orbital_radius_planet_km], [0.0], [0.0]])
velocity_planet = np.array([[0.0], [orbital_velocity_planet], [0.0]])

# Appliquer l'inclinaison à la planète
position_planet_inclined, velocity_planet_inclined = apply_inclination(position_planet, velocity_planet, inclination_planet)

planete = Body(Name='Planet',
               Position=position_planet_inclined,
               Velocity=velocity_planet_inclined,
               Mass=mass_planet,
               Radius=0.5 * 69911,  # Rayon approximatif en km
               Temperature=300,   # Température en K
               Albedo=0.3,
               Emissivity=0.95,
               Color='c')

### SIMULATION DU SYSTEME ###

# Système avec Gamma Cephei A, Gamma Cephei B et une planète
gamma_ceph_system = System([gamma_ceph_a, gamma_ceph_b, planete])

# Simulation du système sur 10 ans avec 5000 étapes pour plus de précision temporelle
gamma_ceph_system.Simulation(Time=100 * YEAR, Nb_step=50000)

# Animation du système sur 10 secondes
gamma_ceph_system.Animation(Animated_time=10,trail=0.4,anim_temps = False, fixed = 0)
