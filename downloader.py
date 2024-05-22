from bing_image_downloader import downloader
import csv
import multiprocessing

commonName = input("common name: ")
aspects = ["leaves", "flowers", "fruit", "bark", "twigs", "tree shape"]

def downloadImagesForTree(scientificName, commonName):
    for aspect in aspects:
        downloader.download(
            scientificName + " " + aspect,
            limit=3,
            output_dir="images/" + commonName + "/" + aspect,
        )

table = []

with open('treeList.txt') as csvFile:
    reader = csv.reader(csvFile)

    for row in reader:
        table.append(row)



procs = []
for row in table:
    proc = multiprocessing.Process(target=downloadImagesForTree, args=[row[0], row[1]])
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()