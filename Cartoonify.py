import numpy as n
import cv2 as c

def image_input():
    image = input("Please enter the path of the image you would like to access: ")

    img = c.imread(image)

    while True:
        if img is None:
            print(f"Could not access the image please try again")
            break
        else:
            print("Prcoessing image...")

        c.imshow('Image', img)
        c.waitKey(0)
        c.destroyAllWindows()
        break

def video():
    consent = input("Do you give permission to access your camera Y/n? : ")
    while True:
        if consent == 'Y' or consent == 'y':
            print("Acessing your camera now...")

        elif consent == 'N' or consent == 'n':
            print("You need to provide your consent to access your camera!")
            break

        else:
            print("Plesae provide a valid input!")
            continue

        cap = c.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            width = int((cap.get(3)))
            height = int((cap.get(4)))

            c.imshow('frame', frame)

            if c.waitKey(1) == ord('q'):
                break
        
        cap.release()
        c.destroyAllWindows()
        print("press q to exit")
        break

choice = input('Would you like to edit an image[press A] or something from yoour webcam[Press B]: ')
if choice == 'A' or choice == 'a':
    image_input()
elif choice == 'B' or choice == 'b':
    video()
else:
    print("Please give a valid input!")