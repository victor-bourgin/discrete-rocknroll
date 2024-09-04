class Flow:
    def __init__(self,
                 friction_vel: float,
                 fluid_density: float,
                 kin_visco: float,
                 ) -> None:

        self.friction_vel = friction_vel
        self.fluid_density = fluid_density
        self.kin_visco = kin_visco