#!/usr/bin/env python3

"""
convert image to pdf file
"""

#Author: mrbeann <https://github.com/mrbeann/jpg2pdf>
import os
import sys
import glob
import platform

from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab import rl_settings

from PIL import Image

import importlib
importlib.reload(sys)

def topdf(path,recursion=None,pictureType=None,sizeMode=None,width=None,height=None,fit=None,save=None):
    """
    Parameters
    ----------
    path : string
           path of the pictures

    recursion : boolean
                None or False for no recursion
                True for recursion to children folder
                wether to recursion or not

    pictureType : list
                  type of pictures,for example :jpg,png...
    sizeMode : int
           None or 0 for pdf's pagesize is the biggest of all the pictures
           1 for pdf's pagesize is the min of all the pictures
           2 for pdf's pagesize is the given value of width and height
           to choose how to determine the size of pdf

    width : int
            width of the pdf page

    height : int
            height of the pdf page

    fit : boolean
           None or False for fit the picture size to pagesize
           True for keep the size of the pictures
           wether to keep the picture size or not

    save : string
           path to save the pdf
    """
    print(path)
    if platform.system() == 'Windows':
        path = path.replace('\\','/')
    if path[-1] != '/':
        path = (path + '/')
    print(path)
    if recursion == True:
        for i in os.listdir(path):
            if os.path.isdir(os.path.abspath(os.path.join(path, i))):
                topdf(path+i,recursion,pictureType,sizeMode,width,height,fit,save)
    filelist = []
    if pictureType == None:
        filelist = glob.glob(os.path.join(path, '*.jpg'))
    else:
        for i in pictureType:
            filelist.extend(glob.glob(os.path.join(path, '*.'+i)))

    filelist = list(sorted(filelist))
    maxw = 0
    maxh = 0
    if sizeMode == None or sizeMode == 0:
        for i in filelist:
            print(f'----,{i}')
            im = Image.open(i)
            if maxw < im.size[0]:
                maxw = im.size[0]
            if maxh < im.size[1]:
                maxh = im.size[1]
    elif sizeMode == 1:
        maxw = 999999
        maxh = 999999
        for i in filelist:
            im = Image.open(i)
            if maxw > im.size[0]:
                maxw = im.size[0]
            if maxh > im.size[1]:
                maxh = im.size[1]
    else:
        if width == None or height == None:
            raise Exception("no width or height provid")
        maxw = width
        maxh = height

    maxsize = (maxw,maxh)
    if save == None:
        filename_pdf = path
    else:
        filename_pdf = save

    filename_pdf = os.path.join(filename_pdf, os.path.basename(path if '/' != path[-1] else path[:-1]))

    #filename_pdf = filename_pdf.decode('utf8','ignore')
    filename_pdf = filename_pdf + '.pdf'
    print(filename_pdf)
    c = canvas.Canvas(filename_pdf, pagesize=maxsize )

    l = len(filelist)
    for i in range(l):
        print(filelist[i])
        (w, h) =maxsize
        width, height = letter
        if fit == True:
            c.drawImage(filelist[i] , 0,0)
        else:
            c.drawImage(filelist[i] , 0,0,maxw,maxh)
        c.showPage()
    c.save()
    print("end.")

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description="img2pdf")
    parser.add_argument('-s', '--source_dir', help='where the source pictures in')
    parser.add_argument('-t', '--pict_types', type=str, nargs='+', help='pict_types, eg: png,jpg,etc')
    parser.add_argument('-m', '--size_mode', default=0, type=int, help='''size mode: 0 the biggest of all the pictures
           1 the min of all the pictures
           2 the given value of width and height''')
    parser.add_argument('-W', '--width', type=int, default=0, help='only needed when size_mode = 2')
    parser.add_argument('-H', '--height', type=int, default=0, help='only needed when size_mode = 2')
    args = parser.parse_args(sys.argv[1:])
    print(args.pict_types)
    topdf(args.source_dir, pictureType=args.pict_types, save=args.source_dir, sizeMode=args.size_mode, width=args.width, height=args.height)
