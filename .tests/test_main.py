import sys
import os
sys.path.append(os.getcwd())

import main
import cv2 as cv
import numpy as np

def test_zmanjsaj_sliko():
    slika = cv.imread('.utils/ronaldo.jpeg') 
    slika_zmanjsana = main.zmanjsaj_sliko(slika, 320, 240)
    assert slika_zmanjsana.shape[0] == 240
    assert slika_zmanjsana.shape[1] == 320
    assert slika_zmanjsana.shape[2] == 3
 
def test_prestej_piksle_z_barvo_koze():
    slika = cv.imread('.utils/ronaldo.jpeg') 
    barva_koze = (np.array([0, 0, 0]), np.array([255, 255, 255]))
    stevilo_piklov = main.prestej_piksle_z_barvo_koze(slika, barva_koze)
    assert stevilo_piklov == slika.shape[0] * slika.shape[1]


def test_obdelaj_sliko():
    slika = cv.imread('.utils/ronaldo.jpeg') 

    def st_kvadratov(sirina_slike, visina_slike, sirina_skatle, visina_skatle):
        return ((sirina_slike - sirina_skatle) // sirina_skatle + 1) * ((visina_slike - visina_skatle) // visina_skatle + 1)

    # Primer 1
    sirina_skatle = 320
    visina_skatle = 240
    barva_koze = (np.array([255, 0, 0]), np.array([255, 0, 0]))
    skatle = main.obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze)
    assert len(skatle) == st_kvadratov(slika.shape[1], slika.shape[0], sirina_skatle, visina_skatle)