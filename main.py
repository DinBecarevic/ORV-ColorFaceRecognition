import cv2
import numpy as np
import time

#.\venv\Scripts\activate

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # TODO: return (lower_bound, upper_bound) as np.ndarray of shape (1,3)
    pass


def zmanjsaj_sliko(slika, sirina, visina):
    # TODO: return resized image as np.ndarray
    pass


def prestej_piksle_z_barvo_koze(slika, barva_koze):
    lower_bound, upper_bound = barva_koze

    # we need to through every pixel in the image and check if it is in the range of the skin color
    # cv2.inRange creates a binary mask where skin color pixels are white (255) and others are black (0).
    mask = cv2.inRange(slika, lower_bound, upper_bound)

    # count non-zero pixels (255) in a mask
    return cv2.countNonZero(mask)


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    # TODO: return list of square regions where color matches skin color
    pass


def main():
    # TODO: implement the main logic here
    pass


if __name__ == "__main__":
    main()