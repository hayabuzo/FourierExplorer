from skimage.io import imread, imshow, imsave
from skimage import img_as_float, img_as_ubyte
from numpy import histogram as hist
from numpy import dstack
import numpy as np
import os

import warnings
warnings.filterwarnings("ignore")

global name, ims 

im=[0,0,0]
impr=[0,0,0]

# ���������

folder = 'input/'    # ����� ��� ������� ������
outfolder = 'output/'  # ����� ��� �������� ������

img_center = 1      # ��������� �������
img_hist = 1        # ������������ �����������
save_pic = 0        # ������� ��������� ��������
save_stack = 1      # ������� ��������� ��������

# ������� �������� ����������, ���� ��� ��� �� ����������
if not os.path.exists(outfolder):
    os.mkdir(outfolder)

# �������

# ������� ������� �������� �����
def clear_folder(folder):
    # �������� ������ ������ � �����
    dirlist = os.listdir(folder)
    # ������� ������ ����
    if (len(dirlist)!=0):
        for i in range(len(dirlist)):
            os.remove(folder+dirlist[i])

# ���������� ������� �� ������� � ������,
# �� ���� ������� �������� ����� ������, ��� �������� � ������������� ��������
def chan(n,img,shift):        
    img = np.fft.fft2(img[:,:,n])
    if shift==1:
        img = np.fft.fftshift(img)    # ��������� ������� 
    return img

# ��������� ��� ������� ��������
def comp(ims,shift,align):
    for i in (0,1,2):
        im[i] = np.log(1+abs(chan(i,ims,shift)))     # �������� ������������ ��� �������
        im[i] = im[i]/im[i].max()                    # ��������������� �������
        
        if align==1:                                 # ������������ �����������
            imt = img_as_ubyte(im[i])
            iy, ix = imt.shape
            values, bin_edges = hist(imt.ravel(), bins=range(257))
            for k in range(257):
                cdf = np.cumsum(values[:k])
            count = 0
            for m in range(256):
                count += cdf[m]
                if count > 0:
                    x_min = i
                    break
            cdfmin = cdf[x_min:].min()    
            imt = np.round( (cdf[imt]-cdfmin)/(iy*ix-1)*255 )
            imt = np.array(imt, dtype=np.uint8)
            im[i] = imt            
        
    impr = dstack((im[0],im[1],im[2]))                # ����������� �������
    return impr

# �������� ������ ������ � �����
clear_folder(outfolder)
flist = os.listdir(folder)
# ��� ������� ����� ���������� ���������


    
for i in range(len(flist)):
    # ��������� ����
    ims = imread(folder+flist[i])
    if ims.shape[2]>2:
        ims = dstack((ims[:,:,0],ims[:,:,1],ims[:,:,2]))
    
    # ������������ ������������� �������: �����������, �����, ������������ �����������
    impr1 = comp(ims,img_center,img_hist)
    
    # ���������� ������������ �������
    if save_pic==1:
        imsave('export-'+str(cap)+'.'+extout, impr1)
    
    # ���������� ��������� �������� � �������
    if save_stack==1:
        if impr1.shape[0]>=impr1.shape[1]:
            imsave(outfolder+'stack-'+flist[i], np.hstack((ims,impr1))) 
        else:
            imsave(outfolder+'stack-'+flist[i], np.vstack((ims,impr1)))
    
    #imsave('export-'+str(cap)+'-st2.'+ext, np.hstack((imread(name),'export-'+str(cap)+'.'+extout)))
    
    # ������ ���������
    print("\r",flist[i]+' processed', end=" ")
    
print(' === processing finished ===')