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
    # TODO: return list of square regions where color matches skin color
    pass


def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # print webcam resolution
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Webcam resolution: {width} x {height}")

    # target size for processing
    target_width, target_height = 320, 240

    skin_color_determined = False
    barva_koze = None

    while True:
        # capture frame by frame
        retrn, frame = cap.read() # retrn = True/False, frame = slika

        if not retrn:
            print("Error: Failed to capture image")
            break

        frame = cv2.flip(frame, 1)

        if not skin_color_determined:
            # 640x480 is the resolution of the webcam by default
            levo_zgoraj = (int(width) // 3, int(height) // 6)
            desno_spodaj = (2 * int(width) // 3, 5 * int(height) // 6)

            # face selection rectangle
            cv2.rectangle(frame, levo_zgoraj, desno_spodaj, (0, 255, 0), 2)

            cv2.putText(frame, "Position face in box and press 'S'",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            cv2.imshow('Face Detection', frame)

            # wait for "s" key to get skin color
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                barva_koze = doloci_barvo_koze(frame, levo_zgoraj, desno_spodaj)
                skin_color_determined = True
                print("skin color determined!")
        else:
            # debug: display min and max color values as a box color in right corner
            lower_bound, upper_bound = barva_koze
            cv2.rectangle(frame, (0, 0), (50, 50), lower_bound[0], -1)
            cv2.rectangle(frame, (50, 0), (100, 50), upper_bound[0], -1)

            # resize the frame for processing
            resized_frame = zmanjsaj_sliko(frame, target_width, target_height)

            # process the frame with boxes (16x16)
            skatla_sirina = target_width // 20 # 320/20 = 16
            skatla_visina = target_height // 15 # 240/15 = 16

            rezultati = obdelaj_sliko_s_skatlami(resized_frame, skatla_sirina, skatla_visina, barva_koze)

            # display boxes for potential faces
            for x, y, w, h, count in rezultati:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # show the frame
            cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()