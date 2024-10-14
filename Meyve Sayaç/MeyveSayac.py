import cv2
import numpy as np

# Görüntüyü yükle
image = cv2.imread("meyve.jpg")
task_image = image.copy()  # Orijinal görselin kopyasını alıp bunun üzerinden işlem yapmak için.

# Görüntüyü griye çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold işlemi
ret, thresh1 = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)

# Kontur bulma
contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #findcontours nesne sınırlarını bulur, retr_external en dıştaki konturları bulur, chain_approx_simple kontur noktalarını sadeleştirir.

# Kontur merkezlerini bul ve koordinatlara göre sırala
centers = []
for contour in contours:
    geo = cv2.moments(contour)
    if geo["m00"] != 0:
        cX = int(geo["m10"] / geo["m00"])  # X koordinatı
        cY = int(geo["m01"] / geo["m00"])  # Y koordinatı
        centers.append((cX, cY, contour))

# y ve x satırı blok/merkez ile sıralama ##önemli
centers = sorted(centers, key=lambda x: (x[1] // 100, x[0]))

# kontur, numara çiz
fruit_count = 0
for i, (cX, cY, contour) in enumerate(centers):
    fruit_count += 1  # meyve sayısını arttır

    # Kontur çiz ve numaralandır
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)  #drawcontours sayesinde orijinal görüntü üzerinde işlemi yapıp, grileştirdiğimiz görüntü üzerinde görüyoruz
    cv2.putText(image, str(fruit_count), (cX, cY), cv2.FONT_ITALIC, 0.6, (255, 0, 0), 2)

# görüntüleri yanyan birleştir
combined_image = cv2.hconcat([task_image, image])

# text
cv2.putText(combined_image, "Orijinal", (10, 30), cv2.FONT_ITALIC, 1, (255, 0, 0), 3, cv2.LINE_AA)
cv2.putText(combined_image, "Task", (650, 30), cv2.FONT_ITALIC, 1, (255, 0, 0), 3, cv2.LINE_AA)
cv2.putText(combined_image, f"Meyve Sayisi {fruit_count}", (500, 515), cv2.FONT_ITALIC, 1, (0, 0, 255), 3, cv2.LINE_AA)

# sonuç
cv2.imshow('Orijinal ve Islenmis Goruntu', combined_image)
tus = cv2.waitKey(0)
if tus == 27:
    cv2.destroyAllWindows()
elif tus == ord("d"):
    cv2.imwrite("YeniGoruntu.jpg", combined_image)  # Kaydet
