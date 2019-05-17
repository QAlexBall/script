import sys

from PIL import Image
if len(sys.argv) == 2:
    path = sys.argv[1]
    print(sys.argv[1])
    im = Image.open(str(path))
    im.show()
else:
    print("please return a right path.")
    print("format to [show_image.sh path/to/image]")
