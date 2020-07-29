import django as x

x = x.__version__

print(f"django ver: {x} - type: {type(x)}")

y=10


def get_div(y):
    z=y/2
    return z

print(get_div(y))