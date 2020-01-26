import numpy as np

GRAVITATIONAL_CONSTANT = 6.67408e-11  # m3 kg-1 s-2

class PhysicalObject:
    def __init__(self, object_id, position, diameter, velocity_vec, color):
        self.object_id = object_id
        self.position_vec = position
        self.diameter = diameter
        self.velocity_vec = velocity_vec
        self.color = color
        self.mass = self.get_object_mass()

    def get_object_mass(self):
        raise NotImplementedError

    def get_object_acc(self, celestial_objects):
        #  http://www.scholarpedia.org/article/N-body_simulations_(gravitational), eq (2)
        total_object_acc = 0.0
        for obj_idx in range(0, len(celestial_objects)):
            # paired_object = celestial_objects[obj_idx]
            connecting_vec = np.subtract(self.position_vec, celestial_objects[obj_idx].position_vec)
            total_object_acc += celestial_objects[obj_idx].mass * connecting_vec *\
                (np.linalg.norm(connecting_vec)) ^ (-3)
        return -GRAVITATIONAL_CONSTANT * total_object_acc

    def get_object_velocity(self):
        object_acc_vec = self.get_object_acc()
        return self.velocity_vec + object_acc_vec * dt

    def get_object_next_position(self):
        raise NotImplementedError

    def collide_object_with(self, collider_object):
        return

    def update(self):



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