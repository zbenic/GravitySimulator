import numpy as np

GRAVITATIONAL_CONSTANT = 6.67408e-11  # m3 kg-1 s-2

class PhysicalObject:
    def __init__(self, object_id, position, diameter, velocity_vec, color, total_object_count, timestep):
        self.object_id = object_id
        self.position_vec = position
        self.diameter = diameter
        self.velocity_vec = velocity_vec
        self.color = color
        self.mass = self.get_object_mass()
        self.accelerations = np.zeros(shape=(total_object_count, 2))  # 2 is the number of dimensions
        self.timestep = timestep

    def get_object_mass(self):
        return self.mass

    def _get_object_acceleration(self, celestial_objects):
        #  http://www.scholarpedia.org/article/N-body_simulations_(gravitational), eq (2)
        total_object_acc = self.accelerations.sum(axis=0)
        for celestial_object in celestial_objects:
            connecting_vec = np.subtract(self.position_vec, celestial_object.position_vec)
            celestial_object.accelerations[celestial_object.object_id] = celestial_object.mass * connecting_vec *\
                                                                         np.linalg.norm(connecting_vec) ** (-3) * (-1)
            total_object_acc += celestial_object.accelerations[celestial_object.object_id] * (-1)
        return -GRAVITATIONAL_CONSTANT * total_object_acc

    def _calculate_object_velocity(self, celestial_objects):
        object_acc_vec = self._get_object_acceleration(celestial_objects)
        self.velocity_vec += object_acc_vec * self.timestep

    def _calculate_object_position(self):
        # self.position_vec += self.velocity_vec * self.timestep
        # TODO: try to avoid unsafe casting
        np.add(self.position_vec, self.velocity_vec * self.timestep, out=self.position_vec, casting='unsafe')

    def _get_object_position(self, celestial_objects):
        self._calculate_object_velocity(celestial_objects)
        self._calculate_object_position()

    def collide_object_with(self, collider_object):
        raise NotImplementedError

    def update(self, celestial_objects):
        self._get_object_position(celestial_objects)


class TerrestrialPlanet(PhysicalObject):
    density = 5515  # kg / m3
    real_diameter = 12.742e6  # m

    def get_object_mass(self):
        return self.density * 4 / 3 * np.pi * pow((self.diameter / 2), 3)


class YellowSun(PhysicalObject):
    density = 1410  # kg / m3
    real_diameter = 1.3927e9  # m

    def get_object_mass(self):
        return self.density * 4 / 3 * np.pi * pow((self.diameter / 2), 3)
