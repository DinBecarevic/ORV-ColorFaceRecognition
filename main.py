import cv2
import numpy as np
import time

#.\venv\Scripts\activate

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # region of interest
    x1, y1 = levo_zgoraj
    x2, y2 = desno_spodaj
    roi = slika[y1:y2, x1:x2]

    mean_color = np.mean(roi, axis=(0, 1)) # axis (width and height)
    tolerance = np.array([50, 50, 50])

    lower_bound = np.array([[max(0, mean_color[0] - tolerance[0]),
                             max(0, mean_color[1] - tolerance[1]),
                             max(0, mean_color[2] - tolerance[2])]])

    upper_bound = np.array([[min(255, mean_color[0] + tolerance[0]),
                             min(255, mean_color[1] + tolerance[1]),
                             min(255, mean_color[2] + tolerance[2])]])

    #npr. za kožo lower_bound = np.array([[0, 48, 80]]) in upper_bound = np.array([[20, 255, 255]])

    return (lower_bound, upper_bound)


def zmanjsaj_sliko(slika, sirina, visina):
    # TODO: return resized image as np.ndarray
    pass


def prestej_piksle_z_barvo_koze(slika, barva_koze):
    # TODO: return number of skin pixels in the image (square area)
    pass


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    # TODO: return list of square regions where color matches skin color
    pass


def main():
    # TODO: implement the main logic here
    pass


if __name__ == "__main__":
    main()