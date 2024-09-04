def rplus(radius, friction_vel, kin_visco):
    return (radius*1e-6) * friction_vel / kin_visco

def biasi_params(radius):
    mean = 0.016 - 0.0023 * (radius ** 0.545)
    stdv = 1.8 + 0.136 * (radius ** 1.4)
    return mean, stdv