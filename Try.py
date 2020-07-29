import django as x

x = x.__version__

print(f"django ver: {x} - type: {type(x)}")

x=10


def get_div(x):
    z=x/2
    return z

print(get_div(x))