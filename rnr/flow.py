import numpy as np


class Flow:
    def __init__(self,
                 duration: float,
                 dt: float,
                 spinup_time: float,
                 target_velocity: float,
                 fluid_density: float,
                 kin_visco: float,
                 surf_energy: float,
                 ) -> None:

        self.duration = duration
        self.dt = dt
        self.spinup_time = spinup_time
        self.target_velocity = target_velocity
        self.fluid_density = fluid_density
        self.kin_visco = kin_visco
        self.surf_energy = surf_energy

        self.time = np.arange(0, self.duration, self.dt)
        self.friction_vel = self._generate_flow()

    def _generate_flow(self):
        # If the spin-up time is greater than 0, friction velocity increases linearly to reacg the target velocity.
        # In practice, a linear increase in free-stream velocity does NOT correspond to a linear increase in friction
        # velocity
        if self.spinup_time > 0:
            friction_vel = np.array([
                0.99 * self.target_velocity * t / self.spinup_time + 0.01 * self.target_velocity if t < self.spinup_time else self.target_velocity for t in self.time
            ])
        else:
            friction_vel = np.ones_like(self.time) * self.target_velocity

        return friction_vel
