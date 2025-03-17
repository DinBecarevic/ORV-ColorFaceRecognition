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
    # TODO: return number of skin pixels in the image (square area)
    pass


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    # return: list of tuples (x, y, width, height, skin_pixel_count)

    height, width = slika.shape[:2] # :2 -> visina in širina
    results = []

    step_size = 16  #320/20 = 16px  in  240/15 = 16px

    for y in range(0, height - visina_skatle + 1, step_size): #0, 320-16+1, 16
        for x in range(0, width - sirina_skatle + 1, step_size):
            window = slika[y:y + visina_skatle, x:x + sirina_skatle] # window[0:15, 0:20]

            skin_px_count = prestej_piksle_z_barvo_koze(window, barva_koze)

            px_count_treshold = 0.6 * (sirina_skatle * visina_skatle) # 0.6 * (20*15) = 180px
            if skin_px_count > px_count_treshold:
                # multiply by 2 because slika is 2x smaller then webcam original
                results.append((x*2, y*2, sirina_skatle*2, visina_skatle*2, skin_px_count))

    return results


def main():
    # TODO: implement the main logic here
    pass


if __name__ == "__main__":
    main()