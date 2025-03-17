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
    # return as np.ndarray
    return cv2.resize(slika, (sirina, visina), interpolation=cv2.INTER_AREA) # INTER_AREA - resampling using pixel area relation


def prestej_piksle_z_barvo_koze(slika, barva_koze):
    lower_bound, upper_bound = barva_koze
    #  error: (-215:Assertion failed) lb.type() == ub.type() in function 'cv::inRange'
    # we need to round the float up and convert to int
    lower_bound = np.round(lower_bound).astype(int)
    upper_bound = np.round(upper_bound).astype(int)

    # we need to through every pixel in the image and check if it is in the range of the skin color
    # cv2.inRange creates a binary mask where skin color pixels are white (255) and others are black (0).
    mask = cv2.inRange(slika, lower_bound, upper_bound)

    # count non-zero pixels (255) in a mask
    return cv2.countNonZero(mask)


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

    # FPS calculation
    prev_frame_time = 0 # seconds.ms
    new_frame_time = 0

    skin_color_determined = False
    barva_koze = None

    while True:
        # capture frame by frame
        retrn, frame = cap.read() # retrn = True/False, frame = slika

        if not retrn:
            print("Error: Failed to capture image")
            break

        frame = cv2.flip(frame, 1)

        # calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0  # 1 / (seconds.ms - seconds.ms)
        prev_frame_time = new_frame_time

        # Convert fps to string for display
        fps_text = f"FPS: {fps:.2f}"

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

            # add FPS text to the frame
            cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 1)

            # show the frame
            cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()