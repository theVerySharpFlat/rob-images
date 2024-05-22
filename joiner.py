from PIL import Image
from bing_image_downloader import downloader
import csv
import multiprocessing

import pandoc

from reportlab.pdfgen.canvas import Canvas, aspectRatioFix

from reportlab.lib.pagesizes import letter

from pathlib import Path

aspects = ["leaves", "flowers", "fruit", "bark", "twigs", "tree shape"]

table = []

with open("treeList.txt") as csvFile:
    reader = csv.reader(csvFile)

    for row in reader:
        table.append(row)

row = table[0]

canvas = Canvas("trees.pdf", pagesize=letter)


def title(string):
    canvas.setFontSize(35)
    canvas.drawCentredString(letter[0] / 2.0, letter[1] * (7 / 8), string)


def heading(string, y, size=35):
    canvas.setFontSize(size)
    canvas.drawCentredString(letter[0] / 2.0, letter[1] - y, string)


for row in table:
    sciName = row[0]
    comName = row[1]

    startPosY = 0.0
    for aspect in aspects:
        root = "images/" + comName + "/" + aspect

        startPosX = 0.0

        paths = Path(root).rglob("*.*")
        pathsLen = 0
        for _ in paths:
            pathsLen += 1

        paths = Path(root).rglob("*.*")

        maxWidth = letter[0] / pathsLen
        maxHeight = (1 / len(aspects)) * 0.75 * letter[1]

        for path in paths:
            img = Image.open(path)
            aspectRatio = img.width / img.height

            width = maxWidth
            height = maxWidth / aspectRatio

            if height > maxHeight:
                height = maxHeight 
                width = height * aspectRatio

            heading(comName + f" ({sciName})", 50)
            heading(aspect, 100, 20)

            canvas.drawImage(
                path, x=startPosX, y=startPosY, width=width, height=height
            )
            startPosX += maxWidth

        startPosY += (1 / len(aspects)) * 0.75 * letter[1]

    canvas.showPage()


canvas.save()
