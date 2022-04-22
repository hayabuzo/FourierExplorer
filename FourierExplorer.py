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

# Параметры

folder = 'input/'    # папка для входных файлов
outfolder = 'output/'  # папка для выходных файлов

img_center = 1      # центровка спектра
img_hist = 1        # выравнивание гистограммы
save_pic = 0        # экспорт отдельной картинки
save_stack = 1      # экспорт склеенной картинки

# создаем выходную директорию, если она еще не существует
if not os.path.exists(outfolder):
    os.mkdir(outfolder)

# Функции

# Функция очистки выходной папки
def clear_folder(folder):
    # получаем список файлов в папке
    dirlist = os.listdir(folder)
    # удаляем каждый файл
    if (len(dirlist)!=0):
        for i in range(len(dirlist)):
            os.remove(folder+dirlist[i])

# Разложение каждого из каналов в спектр,
# на вход функции подается номер канала, имя картинки и необходимость цетровки
def chan(n,img,shift):        
    img = np.fft.fft2(img[:,:,n])
    if shift==1:
        img = np.fft.fftshift(img)    # центровка спектра 
    return img

# Обработка всх каналов картинки
def comp(ims,shift,align):
    for i in (0,1,2):
        im[i] = np.log(1+abs(chan(i,ims,shift)))     # Создание визуализации для каналов
        im[i] = im[i]/im[i].max()                    # Масштабирование яркости
        
        if align==1:                                 # Выравнивание гистограммы
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
        
    impr = dstack((im[0],im[1],im[2]))                # Объединение каналов
    return impr

# получаем список файлов в папке
clear_folder(outfolder)
flist = os.listdir(folder)
# для каждого файла производим обработку


    
for i in range(len(flist)):
    # считываем файл
    ims = imread(folder+flist[i])
    if ims.shape[2]>2:
        ims = dstack((ims[:,:,0],ims[:,:,1],ims[:,:,2]))
    
    # Визуализация центрованного спектра: изображение, сдвиг, выравнивание гистограммы
    impr1 = comp(ims,img_center,img_hist)
    
    # Сохранение визуализации спектра
    if save_pic==1:
        imsave('export-'+str(cap)+'.'+extout, impr1)
    
    # Сохранение склеенной картинки и спектра
    if save_stack==1:
        if impr1.shape[0]>=impr1.shape[1]:
            imsave(outfolder+'stack-'+flist[i], np.hstack((ims,impr1))) 
        else:
            imsave(outfolder+'stack-'+flist[i], np.vstack((ims,impr1)))
    
    #imsave('export-'+str(cap)+'-st2.'+ext, np.hstack((imread(name),'export-'+str(cap)+'.'+extout)))
    
    # Строка состояния
    print("\r",flist[i]+' processed', end=" ")
    
print(' === processing finished ===')