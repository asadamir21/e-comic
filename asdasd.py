import os, glob, shutil


for ComicImageFileName in glob.glob("Dummy/" + next(os.walk('./Dummy/'))[1][0] + '/*.jpg'):
    print(ComicImageFileName.replace(os.sep, '/'))

shutil.rmtree("Dummy/"+next(os.walk('./Dummy/'))[1][0])