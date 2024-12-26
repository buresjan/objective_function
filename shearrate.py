import numpy as np
from scipy.interpolate import CubicSpline


shear_rate_data = np.array(
    [
        7561.19687467,
        8162.574,
        8317.22471111,
        8354.57411111,
        8311.72182222,
        8143.82944444,
        7944.35662222,
        6910.81295556,
        6713.96935556,
        6786.76435556,
        6734.21746667,
        6747.9641963,
        6701.43491111,
        6657.66053333,
        6630.12906667,
        6628.16809571,
        6568.17995556,
        6526.88277778,
        6518.08355556,
        6529.09684444,
        6513.08897778,
        6511.8096,
        6494.05188889,
        6504.91075556,
        6472.63682222,
    ]
)

offsets = np.array(
    [
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
        1.3,
        1.4,
        1.5,
        1.6,
        1.7,
        1.8,
        1.9,
        2.0,
        2.1,
        2.2,
        2.3,
        2.4,
    ]
)


def shear_rate(x, constraints=(0.0, 0.78)):
    if constraints is not None:
        limit_low, limit_up = constraints
        if np.any(x < limit_low) or np.any(x > limit_up):
            return np.array([1e9])

    tke_func = CubicSpline(offsets, shear_rate_data)

    return tke_func(x)


if __name__ == "__main__":
    pass
