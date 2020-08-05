import django as x
from PIL import Image

print(f"django ver: {x} - type: {type(x)}")

y=10


def get_div(y):
    z=y/2
    return z



img = Image.open('IMG_1335.jpg')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        newData.append((255, 255, 255, 0))
    else:
        if item[0] > 150:
            newData.append((0, 0, 0, 255))
        else:
            newData.append(item)
            print(item)


img.putdata(newData)
img.save("Background.jpg", "jpg")
img.show()
print(get_div(y))