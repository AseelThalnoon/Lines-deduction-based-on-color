import os
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt  # To show on the screen
from PIL import Image


def PutText(index, pt1):
    cv2.putText(rgb, "line-" + str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Read the image
file = "sample-1.jpg"
img = cv2.imread(file)
rgb2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.imshow(rgb)
plt.title('Original Image')
plt.show()
# Make it Black & White

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(rgb, 300, 500)

#edges2 = cv2.Canny(gray, 300, 500, apertureSize=3)


plt.imshow(edges)
plt.title('Edge Image')
plt.xticks([]), plt.yticks([])
#cv2.imwrite("gray.png", edges)
plt.show()

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, 30, 5)


"""
lines_list = []
lines2 = cv2.HoughLinesP(
    edges2,  # Input edge image
    1,  # Distance resolution in pixels
    np.pi / 180,  # Angle resolution in radians
    threshold=200,  # Min number of votes for valid line
    minLineLength=10,  # Min allowed length of line
    maxLineGap=5  # Max allowed gap between line for joining them
)
"""
"""
# Iterate over points
for points in lines2:
    # Extracted points nested in the list
    x1, y1, x2, y2 = points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(rgb3, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Maintain a simples lookup list for points
    lines_list.append([(x1, y1), (x2, y2)])

plt.title("New All lines")
plt.imshow(rgb3)  # cmap prevents yellow image
#cv2.imwrite("all-lines.png", rgb3)

plt.show()

"""


im = Image.open(file)  # Can be many different formats.
pix = im.load()

colors = [
    ("black", (0, 0, 0)),
    ("silver", (192, 192, 192)),
    ("gray", (128, 128, 128)),
    ("light-gray", (191, 191, 191)),
    ("white", (255, 255, 255)),
    ("maroon", (128, 0, 0)),
    ("red", (255, 0, 0)),
    ("purple", (128, 0, 128)),
    ("fuchsia", (255, 0, 255)),
    ("green", (0, 128, 0)),
    ("lime", (0, 255, 0)),
    ("olive", (128, 128, 0)),
    ("yellow", (255, 255, 0)),
    ("navy", (0, 0, 128)),
    ("blue", (0, 0, 255)),
    ("teal", (0, 128, 128)),
    ("aqua", (0, 255, 255))
]

def distance(a,b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    dz = a[2]-b[2]
    return math.sqrt(dx*dx+dy*dy+dz*dz)

def findclosest(pixel):
    mn = 999999
    for name, rgb in colors:
        d = distance(pixel, rgb)
        if d < mn:
            mn = d
            color = name
    return color


contours, z = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
width, height = im.size

#drawing all lines
for line in lines:
    pt1 = (line[0][0], line[0][1])
    pt2 = (line[0][2], line[0][3])
    cv2.line(rgb2, pt1, pt2, (0, 0, 255), 2)
    # cv2.putText(rgb2, "line-"+str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
plt.title("All lines")
plt.imshow(rgb2)  # cmap prevents yellow image
plt.show()

#Labelling all lines or only someof them

def PutText(index, pt1):
        cv2.putText(rgb, "line-" + str(index), pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Index of the Lines
index = 0
all_lines = []
colored_lines = []

# Filitering the lines based on color and surrounding pixels
for line in lines:
    pt1 = (line[0][0], line[0][1])
    pt2 = (line[0][2], line[0][3])
    all_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])

    if pt1[1] < height/2 or pt2[1] < height/2:
        index = index + 1
        continue

    pick_color = "white"
    number_of_pix = 2

    # Original point
    if (findclosest(pix[pt1[0], pt1[1]]) == pick_color or findclosest(pix[pt2[0], pt2[1]]) == pick_color):
        cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
        colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
        PutText(index, pt1)





    elif(pt1[0] + number_of_pix < width and pt1[1] + number_of_pix < height) and (pt2[0] + number_of_pix < width and pt2[1] + number_of_pix < height):
        for x in range(1, number_of_pix+1):

            # Upper left
            if (findclosest(pix[pt1[0]-x, pt1[1]-x]) == pick_color or findclosest(pix[pt2[0]-x, pt2[1]-x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break





            # Upper middle
            elif (findclosest(pix[pt1[0]-x, pt1[1]]) == pick_color or findclosest(pix[pt2[0]-x, pt2[1]]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # Upper right
            elif (findclosest(pix[pt1[0]-x, pt1[1]+x]) == pick_color or findclosest(pix[pt2[0]-x, pt2[1]+x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # left
            elif (findclosest(pix[pt1[0], pt1[1]-x]) == pick_color or findclosest(pix[pt2[0], pt2[1]-x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # right
            elif (findclosest(pix[pt1[0], pt1[1] + x]) == pick_color or findclosest(pix[pt2[0], pt2[1] + x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            #Lower right
            elif (findclosest(pix[pt1[0]+x, pt1[1]+x]) == pick_color or findclosest(pix[pt2[0]+x, pt2[1]+x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # lower middle
            elif (findclosest(pix[pt1[0]+x, pt1[1]]) == pick_color or findclosest(pix[pt2[0]+x, pt2[1]]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break




            # Lower left
            elif (findclosest(pix[pt1[0] + x, pt1[1]-x]) == pick_color or findclosest(pix[pt2[0] + x, pt2[1]-x]) == pick_color):
                cv2.line(rgb, pt1, pt2, (0, 0, 255), 2)
                colored_lines.append([index, pt1[0], pt1[1], pt2[0], pt2[1]])
                PutText(index, pt1)
                break

    index = index + 1


# Writing the output text file
with open('all-lines.txt', 'w') as f:
    for line in all_lines:
        f.write("line-" + str(line[0]) + " [" + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "]\n")

with open('colored-lines.txt', 'w') as f:
    for line in colored_lines:
        f.write("line-" + str(line[0]) + " [" + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "]\n")



plt.title(pick_color+ " Lines" + " " + "("+str(number_of_pix)+") Pixel")
plt.imshow(rgb)
plt.show()

