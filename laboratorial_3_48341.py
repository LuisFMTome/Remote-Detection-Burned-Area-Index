# -*- coding: utf-8 -*-
"""
@author: Luís Filipe Medeiros Tomé, 48341
"""
import matplotlib.pyplot as plt
from imageio import imread, imwrite
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

def cBAIMS(b8, b11):
    """
    Requires:
        b8 = list (banda infravermelha) and b11 = list (banda SWIR)
    Ensures:
        Resultado do calculo de BAIMS
    """
    baims = 1 / ((b8.astype(float) - 0.05)**2 + (b11.astype(float) - 0.2)**2)
    return baims

def cNVDIandNBRS(b1, b2):
    """
    NVDI: b1 = b8 (banda infravermelha) and b2 = b4 (banda vermelha)
    NBRS: b1 = b8 (banda infravermelha) and b2 = b11 (banda SWIR)
        
    Requires:
        b1 = list and b2 = list
    Ensures:
        Resultado do calculo de NVDI ou NBRS
    """
    c = (b1 - b2) / (b1 + b2)
    return c

print('Carregando imagens de Pedrogao, antes e depois do incendio...')
pJunho = imread('subset_0_of_S2A_MSIL1C_20170614T112111_N0205_R037_T29TNE_20170614T112422_extractor_resampled.tif').astype(float)/10000
pJulho = imread('subset_0_of_S2A_MSIL1C_20170704T112111_N0205_R037_T29TNE_20170704T112431_extractor_resampled.tif').astype(float)/10000
print('Carregamento terminado.')

# =============================================================================
# Bandas:
    # Vermelha:		B4 =  pJunho[2,:,:] ; pJulho[2,:,:]
    # Infravermelha:	B8 =  pJunho[3,:,:] ; pJulho[3,:,:]
    # SWIR:		B11 = pJunho[4,:,:] ; pJulho[4,:,:]
# =============================================================================

print('Calculos de NVDI, NBRS, BAI e BAIMS das imagens e diferenças entre imagens dos resultados NVDI e BAIMS...')
dBAIMS = cBAIMS(pJulho[3,:,:], pJulho[4,:,:]) - cBAIMS(pJunho[3,:,:], pJunho[4,:,:])
dNVDI = cNVDIandNBRS(pJulho[3,:,:], pJulho[2,:,:]) - cNVDIandNBRS(pJunho[3,:,:], pJunho[2,:,:])
nbrsJulho = cNVDIandNBRS(pJulho[3,:,:], pJulho[4,:,:])
baiJulho = 1 / ((pJulho[3,:,:] - 0.06)**2 + (pJulho[2,:,:] - 0.1)**2) 
print('Calculos Terminados.')

print('Execução de operação logica...')
areaArdida = ((dBAIMS > 46.8143) & (dNVDI < -0.17767) & (nbrsJulho < -0.17079) & (baiJulho > 188.88)).astype(float)
print('Operação logica terminada.')

print('Guardar imagem da região ardida...')
imwrite('AreaArdidaPedrogao2017.tif', areaArdida)
print('Imagem guardada.')

plt.figure();plt.imshow(areaArdida, 'gray');plt.axis('off');plt.title('Incêndio em Pedrogão, Julho de 2017')

print('Execução terminada.')