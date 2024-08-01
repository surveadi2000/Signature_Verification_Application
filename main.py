import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from signature import match

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=[("Image files", "*.jpeg;*.png;*.jpg")])
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            img_name = "./temp/test_img1.png" if sign == 1 else "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    filename = os.getcwd() + '\\temp\\test_img1.png' if sign == 1 else os.getcwd() + '\\temp\\test_img2.png'
    res = messagebox.askquestion('Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match", f"Signatures are {result:.2f}% similar!!")
    else:
        messagebox.showinfo("Success: Signatures Match", f"Signatures are {result:.2f}% similar!!")
    return True

root = tk.Tk()
root.title("Signature Matching")
root.geometry("600x400")
root.config(bg="#f0f8ff")  # Light background color

# Label styling
uname_label = tk.Label(root, text="Compare Two Signatures:", font=("Arial", 16, "bold"), bg="#f0f8ff")
uname_label.pack(pady=10)

# Signature 1
img1_frame = tk.Frame(root, bg="#e6f7ff")
img1_frame.pack(pady=10, fill=tk.X, padx=20)

img1_message = tk.Label(img1_frame, text="Signature 1", font=("Arial", 12), bg="#e6f7ff")
img1_message.pack(side=tk.LEFT, padx=10)

image1_path_entry = tk.Entry(img1_frame, font=("Arial", 12))
image1_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

img1_capture_button = tk.Button(img1_frame, text="Capture", font=("Arial", 12), command=lambda: captureImage(ent=image1_path_entry, sign=1), bg="#66b3ff", fg="white", relief=tk.RAISED)
img1_capture_button.pack(side=tk.RIGHT, padx=10)

img1_browse_button = tk.Button(img1_frame, text="Browse", font=("Arial", 12), command=lambda: browsefunc(ent=image1_path_entry), bg="#66b3ff", fg="white", relief=tk.RAISED)
img1_browse_button.pack(side=tk.RIGHT, padx=10)

# Signature 2
img2_frame = tk.Frame(root, bg="#e6f7ff")
img2_frame.pack(pady=10, fill=tk.X, padx=20)

img2_message = tk.Label(img2_frame, text="Signature 2", font=("Arial", 12), bg="#e6f7ff")
img2_message.pack(side=tk.LEFT, padx=10)

image2_path_entry = tk.Entry(img2_frame, font=("Arial", 12))
image2_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

img2_capture_button = tk.Button(img2_frame, text="Capture", font=("Arial", 12), command=lambda: captureImage(ent=image2_path_entry, sign=2), bg="#66b3ff", fg="white", relief=tk.RAISED)
img2_capture_button.pack(side=tk.RIGHT, padx=10)

img2_browse_button = tk.Button(img2_frame, text="Browse", font=("Arial", 12), command=lambda: browsefunc(ent=image2_path_entry), bg="#66b3ff", fg="white", relief=tk.RAISED)
img2_browse_button.pack(side=tk.RIGHT, padx=10)

# Compare Button
compare_button = tk.Button(root, text="Compare", font=("Arial", 14, "bold"), command=lambda: checkSimilarity(window=root, path1=image1_path_entry.get(), path2=image2_path_entry.get()), bg="#ff6666", fg="white", relief=tk.RAISED)
compare_button.pack(pady=20)

root.mainloop()
