# -*- coding: utf-8 -*-
#%%
import cv2 
import easyocr
from matplotlib import pyplot as plt
import imutils
import numpy as np
from pyparsing import White

def PlakaOku(PathResim) -> str:#string değer döndürüyor
    img = cv2.imread(PathResim)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #gürültü temizleme
    edged = cv2.Canny(bfilter, 30, 200)     #köşe tanımlanmış resmimiz
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BAYER_BG2RGB))

    #resimdeki dörtgenleri tanıma kısmı
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #şekillerin bir döngü içinde sıralanmasını sağlayan fonksiyon

    #bulunan şekillerin bir dörtgen olup olmadığını kontrol etmek için bir döngü içinde kontrol eder
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True) #10 yazan yer tanınacak kenarların ne kadar düzgün bir hassasiyetle alınacağını ayarlar
        if len(approx) == 4:                 #eğer 4 kenar bulunursa bu nokta plaka olarak tanımlanacak
            location = approx
            break
    print(location) #plakanın koordinatlarını yazdırır

    #plakanın tam bulunduğu bölgeyi işaretleme
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1) #resimdeki maskelenen yerin koordinatlarının etrafını çizer
    new_image = cv2.bitwise_and(img, img, mask=mask)
    plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

    #plakayı bulduğumuz kısmı easyocr'da kullanmadan önce resimden ayırmak gerekiyor
    (x,y) = np.where(mask == 255)                #plakanın etrafındaki kısımların tamamının koordinatları
    (x1,y1) = (np.min(x) , np.min(y) )           #en düşük x ve y değerleri yani plakanın sol üst köşesi
    (x2, y2) = (np.max(x) , np.max(y) )          #en yüksek x ve y değerleri yani plakanın sağ alt köşesi
    cropped_image = gray[x1: x2+1 , y1:y2+1]     #verilen +1 değeri eğimli kenarlarda biraz daha geniş alınması için
    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

    #easyOCR sayesinde artık resimdeki yazıyı okuyabiliriz
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    result
    if result:
        return result[0][1] # plakayı döndürüyor
    else:
        return "{OKUNAMADI}"
    

# %%
