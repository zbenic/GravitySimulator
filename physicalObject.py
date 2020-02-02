import numpy as np

# GRAVITATIONAL_CONSTANT = 6.67408e-11  # m3 kg-1 s-2
GRAVITATIONAL_CONSTANT = 1  # m3 kg-1 s-2
EPS = 10          # pixels
MIN_DISTANCE = 5  # pixels


class PhysicalObject:
    def __init__(self, object_id, position, diameter, velocity_vec, color, total_object_count, timestep):
        self.object_id = object_id
        self.position_vec = position.astype(np.float32)
        self.diameter = diameter
        self.velocity_vec = velocity_vec.astype(np.float32)
        self.color = color
        self.mass = self._get_object_mass()
        self.accelerations = np.zeros(shape=(total_object_count, 2))  # 2 is the number of dimensions
        self.old_total_acc_vec = np.zeros(2)                          # 2 is the number of dimensions
        self.timestep = timestep
        self.object_is_valid = True

    def _get_object_mass(self):
        raise NotImplementedError

    def _get_object_acceleration(self, celestial_objects):
        #  http://www.scholarpedia.org/article/N-body_simulations_(gravitational), eq (2)
        total_object_acc = self.old_total_acc_vec + self.accelerations.sum(axis=0)
        for celestial_object in celestial_objects:
            connecting_vec = np.subtract(self.position_vec, celestial_object.position_vec)
            celestial_object.accelerations[celestial_object.object_id] = celestial_object.mass * connecting_vec *\
                (np.linalg.norm(connecting_vec) ** 2 + EPS ** 2) ** (-3. / 2) * (-1)
            total_object_acc += celestial_object.accelerations[celestial_object.object_id] * (-1)
        return -GRAVITATIONAL_CONSTANT * total_object_acc

    def _calculate_object_velocity(self, celestial_objects):
        object_acc_vec = self._get_object_acceleration(celestial_objects)
        self.old_total_acc_vec = object_acc_vec
        self.velocity_vec += object_acc_vec * self.timestep

    def _calculate_object_position(self):
        self.position_vec += self.velocity_vec * self.timestep

    def _get_object_position(self, celestial_objects):
        self._calculate_object_velocity(celestial_objects)
        self._calculate_object_position()

    @staticmethod
    def merge_objects(main_object, secondary_object):
        secondary_object.object_is_valid = False
        main_object.mass += secondary_object.mass
        # equal density for all object is assumed
        # TODO: enable different object types (densities) to be merged
        main_object.diameter = int(np.ceil(np.power(3 * main_object.mass / (4 * np.pi * TerrestrialPlanet.density), 1. / 3) * 2))

    def check_for_collisions_and_merge(self, celestial_objects):
        # collision of only 2 bodies handled
        # TODO: add collision of multiple bodies
        if self.object_is_valid:
            for celestial_object in celestial_objects:
                if np.linalg.norm(np.subtract(self.position_vec, celestial_object.position_vec)) <= MIN_DISTANCE:
                    plastic_collision_acc_vec = (self.mass * self.old_total_acc_vec +
                                                 celestial_object.mass * celestial_object.old_total_acc_vec) /\
                                                (self.mass + celestial_object.mass)
                    plastic_collision_vel_vec = (self.mass * self.velocity_vec +
                                                 celestial_object.mass * celestial_object.velocity_vec) /\
                                                (self.mass + celestial_object.mass)
                    if self.mass >= celestial_object.mass:
                        self.old_total_acc_vec = plastic_collision_acc_vec
                        self.velocity_vec = plastic_collision_vel_vec
                        PhysicalObject.merge_objects(self, celestial_object)
                    else:
                        celestial_object.old_total_acc_vec = plastic_collision_acc_vec
                        celestial_object.velocity_vec = plastic_collision_vel_vec
                        PhysicalObject.merge_objects(celestial_object, self)

                    break

    def update(self, celestial_objects):
        self._get_object_position(celestial_objects)


class TerrestrialPlanet(PhysicalObject):
    density = 5515  # kg / m3
    real_diameter = 12.742e6  # m

    def _get_object_mass(self):
        return self.density * 4 / 3 * np.pi * pow((self.diameter / 2), 3)


class YellowSun(PhysicalObject):
    density = 1410  # kg / m3
    real_diameter = 1.3927e9  # m

    def _get_object_mass(self):
        return self.density * 4 / 3 * np.pi * pow((self.diameter / 2), 3)
