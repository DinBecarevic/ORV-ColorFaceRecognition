import cv2
import numpy as np
import time

#.\venv\Scripts\activate

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # TODO: return (lower_bound, upper_bound) as np.ndarray of shape (1,3)
    pass


def zmanjsaj_sliko(slika, sirina, visina):
    # return as np.ndarray
    return cv2.resize(slika, (sirina, visina), interpolation=cv2.INTER_AREA) # INTER_AREA - resampling using pixel area relation


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