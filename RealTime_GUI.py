import PySimpleGUI as sg
import cv2
import numpy as np

contrast_true = np.arange(1.0, 3.0, 0.02, dtype=float)
blur_true = np.arange(1, 20, 2, dtype=int)

cap = cv2.VideoCapture(0)


def main():
    sg.theme('Light Grey 1')
    contrast = 1
    brightness = 1
    blur = 1
    layout = [
        [sg.Text('Real Time Video Filter', size=(40, 1),
                 justification='center', font='Helvetica 20')],
        [sg.Image(filename='', size=(640, 480),
                  key='image', background_color="#b6b6b6")],
        [
            sg.Push(),
            sg.Button('Record', size=(10, 1), font='Helvetica 14'),
            sg.Button('Stop', size=(10, 1), font='Any 14'),
            sg.Button('Exit', size=(10, 1), font='Helvetica 14'),
            sg.VPush(),
        ],
        [
            sg.Button('Histogram'),
        ],
        [
            sg.Text("Contrast", size=(10, 1)),
            sg.Slider(orientation='horizontal', key='Slider Con',
                      default_value=contrast, enable_events=True, range=(1, 100), size=(35, 12)),
        ],
        [
            sg.Text("Brightness", size=(10, 1)),
            sg.Slider(orientation='horizontal', key='Slider Bri',
                      default_value=brightness, enable_events=True, range=(1, 100), size=(35, 12)),
        ],
        [
            sg.Text("Blur", size=(10, 1)),
            sg.Slider(orientation='horizontal', key='Slider Blur',
                      default_value=blur, enable_events=True, range=(1, 10), size=(35, 12)),
        ],
    ]

    window = sg.Window('Real Time Video Filter',
                       layout)

    recording = False
    histogram = False
    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return
        elif event == 'Record':
            recording = True
        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 182)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
        if event == "Slider Con":
            contrast = int(values["Slider Con"])
        if event == "Slider Bri":
            brightness = int(values["Slider Bri"])
        if event == "Slider Blur":
            blur = int(values["Slider Blur"])
        if event == "Histogram":
            histogram = not histogram
        if recording:
            try:
                ret, frame = cap.read()
                new_frame = cv2.convertScaleAbs(
                    frame, alpha=contrast_true[contrast-1], beta=brightness)
                if histogram:
                    img_yuv = cv2.cvtColor(new_frame, cv2.COLOR_BGR2YUV)
                    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                    new_frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
                kernel = np.ones(
                    (blur_true[blur-1], blur_true[blur-1]), np.float32)/blur_true[blur-1]**2
                dst = cv2.filter2D(new_frame, -1, kernel)
                imgbytes = cv2.imencode('.png', dst)[1].tobytes()
                window['image'].update(
                    data=imgbytes)
            except:
                recording = False
                sg.Popup(
                    "Can not open camera, please check your camera!", title='Error')

    window.close()
