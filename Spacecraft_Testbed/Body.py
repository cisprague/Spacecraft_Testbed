'''''''''''''''''''''''''''''''''''''''''''''''''''''
// Authored by Christopher Iliffe Sprague          //
// Christopher.Iliffe.Sprague@gmail.com            //
// +1 703 851 6842                                 //
// https://github.com/CISprague/Spacecraft_Testbed //
'''''''''''''''''''''''''''''''''''''''''''''''''''''

import numpy                       as     np
import matplotlib                  as     mpl
import matplotlib.pyplot           as     plt
import matplotlib.animation        as     animation
import mpl_toolkits.mplot3d.axes3d as     p3
from   scipy                       import constants
from   Utilities                   import *
from   matplotlib.colors           import cnames
from   mpl_toolkits.mplot3d        import Axes3D
from   aerocalc.std_atm            import alt2density

class Body(object):

    '''In classical mechanics a physical body is collection of matter having properties including mass, velocity, momentum and energy. The matter exists in a volume of three-dimensional space.'''

    # Instance record
    _instances = []

    def __init__(self, name, mass=None):
        # __base__ attribute will return the Body class
        self.__base__   = Body
        # Name of body
        self.name       = name
        # Mass of body
        self.mass       = np.float64(mass)
        # Time record
        self.times      = np.empty([1, 0], dtype=np.float64)
        # Position record
        self.positions  = np.empty([0, 3], dtype=np.float64)
        # Velocity record
        self.velocities = np.empty([0, 3], dtype=np.float64)
        # Append to _instances
        Body._instances.append(self)
        return None

    def Position_and_Velocity(self, time):
        return None

    def Position_and_Velocity_WRT(self, body_ref, time):
        '''Returns position and velocity of measured body
        with respect to a reference body, both of Body.'''
        # Reference body's barycentric position and velocity
        P0V0 = body_ref.Position_and_Velocity(time)
        # Measured body's barycentric position and velocity
        PV   = self.Position_and_Velocity(time)
        # Measured body's position and velocity with respect
        # to reference body
        pv   = np.subtract(PV, P0V0)
        # Returns (2,3) numpy array
        return pv

    def Update_Position_and_Velocity(self, time):
        '''This function takes as its argument time,
        which will be obtained from the time step of
        the simulation, and updates the historical
        arrays, namely: (1,_) times, (_,3) positions,
        and (_,3) velocities.'''
        # Barycentric position and velocity of body at time (2,3)
        pv              = self.Position_and_Velocity(time)
        # Append results to history keeping list for this body
        self.times      = np.append(self.times, time)
        self.positions  = np.vstack([self.positions , pv[0, :]])
        self.velocities = np.vstack([self.velocities, pv[1, :]])
        # Also returns barycentric position and velocty
        return None

    def Plot_3D(self, figure, body_ref=None):
        if body_ref is None:
            pos = self.positions
        else:
            pos = np.subtract(body_ref.positions, self.positions)
            pass
        x = pos[:, 0]
        y = pos[:, 1]
        z = pos[:, 2]
        ax = figure.gca(projection='3d')
        ax._axis3don = True
        ax.plot(x, y, z)
        return None


class Celestial_Body(Body):
    '''
    A celestial body is any natural body outside of
    Earth's atmosphere. Examples are the Moon,
    Sun, and other planets outside our solar system.
    '''

    # Instance record
    _instances = []

    def __init__(self, name, mass=None, satellites=True):

        # Fundamentally initialise the celestial body
        Body.__init__(self, name, mass)
        # Assign its unique attributes
        Assign_Celestial_Body_Attributes(self)

        # If it is specified to include satellites
        if satellites is True:

            try:
                # Instantiate the dictionary of satellite collections
                sat_dic = Satellite_Dictionary(name)
                # List of satellite collection types
                for sat_type in sat_dic.keys():
                    # Instantiate the satellite collection type
                    sct = Satellites()
                    # List of collections within that type
                    for sat_col in sat_dic[sat_type].keys():
                        # Instantiate the satellite collection
                        sc = Satellite_Collection(sat_col, self)
                        sc.satellite_type = sat_type
                        # List of object of that satellite
                        for sat_obj in sat_dic[sat_type][sat_col].keys():
                            # Instantiate the object as a Satellite instance
                            s = Satellite(sat_obj, self)
                            # Line 1 of the TLE for this object
                            s.line1 = sat_dic[sat_type][sat_col][sat_obj][0]
                            # Line 2
                            s.line2 = sat_dic[sat_type][sat_col][sat_obj][1]
                            # Assign the satellite object to its collection
                            setattr(sc, sat_obj, s)
                        setattr(sct, sat_col, sc)
                    setattr(self, 'Satellites', sct)
            except:
                pass
        Celestial_Body._instances.append(self)
        return None

    def Position_and_Velocity(self, time):
        return Position_and_Velocity_Celestial_Body(self, time)
    pass


class Satellite(Body):
    '''
    A satellite is a moon, planet or machine that orbits a planet or star. For example, Earth is a satellite because it orbits the sun. Likewise, the moon is a satellite because it orbits Earth. Usually, the word "satellite" refers to a machine that is launched into space and moves around Earth or another body in space.
    '''
    # Instance tracking
    _instances = []

    def __init__(self, name,  attracting_body, mass=None):
        Body.__init__(self, name, mass)
        # The attracting body of the satellite
        self.attracting_body = attracting_body
        Satellite._instances.append(self)
        return None

    def Position_and_Velocity(self, time):
        return Position_and_Velocity_Satellite(self, time)
    pass


class Satellite_Collection(object):
    '''Acts as a namespace organising satellites'''

    def __init__(self, name, attracting_body):
        # The name of the collection
        self.name            = name
        # The name of its attracting body
        self.attracting_body = attracting_body
        return None
    pass


class Satellites(object):
    '''Acts as a namespace organising satellite'''

    def __init__(self):
        return None
    pass

class Spacecraft(Body):
    '''
    A spacecraft is a vehicle used for traveling in space. An object of this type is capable of making its own decisions an actively altering its dynamics via thrust.

    DV: Delta-V is a measure of the potential impulse needed to perform maneuvres. It is a scaler that has the units of speed. It is not the same as the physical change in velocity of the vehicle. Delta-V is produced by reaction engines, such as rocket engines, and is proportional to the thrust per unit mass, and brun time, and is used to determine the mass of propellant required for the given maneuvre through the Tsiolkovsky  rocket equation. For Multiple maneuvres, delta-V sums linearly.

    Isp: Specific impulse is a measure of the efficiency of rocket and jet engines. By definition, it is the total impulse (or change in momentum) delivered per unit of propellant consumed and is dimensionally equivalent to the generated thrust divided by the propellant flow rate.

    T_max: Maxium thrust is the maximum amount of thrust the spacecraft is capable of outputing at any time. This value is determined by the spacecraft specific propulsion system configuration. In the context of a CubeSat, this is easily determined through specifications provided by comerical off the shelf (COTS) hardware that may be procured.

    DV            [m/s]   = scaler
    Isp           [s]     = scaler
    T_max         [N]     = scaler
    times         [s]     = [ t_i    ...    t_I  ]
    positions     [m]     = | x_i    y_i    z_i  |
                            | :      :      :    |
                            | x_I    y_I    z_I  |
    velocities    [m/s]   = | vx_i   vy_i   vz_i |
                            | :      :      :    |
                            | vx_I   vy_I   vz_I |
    accelerations [m/s^2] = | ax_i   ay_i   az_i |
                            | :     :     :      |
                            | ax_I   ay_I   az_I |
    '''

    def __init__(self      , name,
                 epoch_p   , epoch_v, epoch_t, area=0.01,
                 epoch_m=4    , DV=220 , Isp=220, T_max=11.16):
        Body.__init__(self, name, epoch_m)
        # The potential delta V [m/s]
        self.DV            = 220
        # Specific impulse      [s]
        self.Isp           = 220
        # Max thrust            [N]
        self.T_max         = 11.16
        # Mass                  [kg]
        self.masses        = np.asarray([epoch_m])
        # Area                  [m^2]
        self.area          = area
        # Epoch time            [s]
        self.times         = np.append(self.times, epoch_t)
        # Positions             [m]
        self.positions     = np.asarray([epoch_p])
        # Velocities            [m/s]
        self.velocities    = np.asarray([epoch_v])
        # Acceleration          [m/s^2]
        self.accelerations = np.asarray([self.Acceleration(Celestial_Body._instances)])


    def Position_and_Velocity_WRT(self, body):
        '''Computes position and velocity of spacecraft with respect to a specified body.'''
        p            = self.positions[-1]  # Most recent position
        v            = self.velocities[-1] # Most recent velocity
        t            = self.times[-1]      # Most recent time
        # Position and velocity of the body
        P, V         = body.Position_and_Velocity(t)
        # Relative position and velocity of spacecraft to body
        p_rel, v_rel = np.subtract(p, P), np.subtract(v, V)
        return p_rel, v_rel

    def Gravitational_Acceleration(self, body):
        '''Computes the gravitational acceleration of the spacecraft due to the influence of a massive body.'''
        # Newtonian gravitational constant                    [m^3 kg^-1 s^-2]
        G      = constants.G
        # Mass of massive body                                [kg]
        M      = body.mass
        # Position of spacecraft with respect to massive body [m], [m/s]
        r, v   = self.Position_and_Velocity_WRT(body)
        # Magnitude of spacecraft's relative position         [m]
        r_norm = np.linalg.norm(r)
        # Unit vector directed from massive body to spacecraft
        r_hat  = np.divide(r, r_norm)
        # Gravitational acceleration vector                   [m/s^2]
        g      = np.multiply(-G, M)
        g      = np.divide(g, np.power(r_norm, 2))
        g      = np.multiply(g, r_hat)
        return g

    def Cummulative_Gravitational_Acceleration(self, bodies):
        '''Computes the cummulative gravitational acceleration due the influence of all the massive bodies in the interplanetary environment.'''
        g     = 0
        for body in bodies:
            g += self.Gravitational_Acceleration(body)
        return g

    def Solar_Radiation_Acceleration(self, sun):
        '''Computes the spacecraft's acceleration due to solar radiation pressure at a given distance from the Sun, assuming it is a sphere.'''

        # Coefficient of reflectivity
        CR    = 0.75
        # Solar radiation constant                     [kg*m/s^2]
        G     = 1e+17
        # Distance vector from the Sun                 [m]
        R_vec = self.Position_and_Velocity_WRT(sun)[0]
        # Magnitude of distance                        [m]
        R     = np.linalg.norm(R_vec)
        # Solar radiation pressure                     [Pa]
        P     = np.divide(G, np.power(R, 2))
        # Most recent mass of spacecraft               [kg]
        m     = self.masses[-1]
        # Cross sectional area seen by the Sun         [m^2]
        A     = self.area
        # Unit vector from the Sun to the spacecraft
        u_hat = np.divide(R_vec, R)
        # Acceleration due to solar radiation pressure [m/s^2]
        a     = np.divide(P, m)
        a     = np.multiply(CR, a)
        a     = np.multiply(a, A)
        a     = np.multiply(a, u_hat)
        return a

    def Altitude(self, body):
        '''Computes the spacecrafts scaler distance away from the body's surface'''
        # Mean distance from the body's centre to its surface
        radius = np.divide(body.diameter, 2)
        # Spacecraft's distance from centre of body
        r      = np.linalg.norm(self.Position_and_Velocity_WRT(body))
        # Spacecraft's altitude
        H      = np.subtract(r, radius)
        return H

    def Aerodynamic_Acceleration(self, body):
        '''Computes the spacecraft's acceleration due to aerodynamic drag whilst encountering the body's atmosphere.'''
        # Altitude of spacecraft above the body [m]
        H = self.Altitude(body)
        # Atmospheric density at this altitude  [kg/m^3]
        try:
            rho = alt2density(H, alt_units='m', density_units='kg/m**3')
        except:
            rho = 0.0
        return rho

    def Acceleration(self, bodies):
        '''Computes the overall acceleration of the spacecraft due to the pressence of the solar system's bodies.'''
        a         = 0
        for body in bodies:
            a    += self.Gravitational_Acceleration(body)
            if body.name is 'Earth':
                a += self.Aerodynamic_Acceleration(body)
            if body.name is 'Sun':
                a += self.Solar_Radiation_Acceleration(body)
        return a
