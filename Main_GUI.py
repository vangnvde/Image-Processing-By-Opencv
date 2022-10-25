import asyncio
import PySimpleGUI as sg
import cv2
import Filter
import RealTime_GUI

BACKGROUND_IMAGE_PRAME = '#f5eec9'

file_types = [("All", "*"),
              ("JPEG (*.jpg)", "*.jpg"),
              ("PNG (*.png)", "*.png")]
sg.theme('Light Grey 1')


def convert_image(image):
    height = image.shape[0]
    width = image.shape[1]
    if width > 400 and height > 400:
        image = cv2.resize(image, (400, 400))
    image_end = cv2.imencode('.png', image)[1].tobytes()
    return image_end


work_lap_title = [
    [sg.Text("IMT301 Image Processing", size=(50, 1),
             font=('Any 15'), justification='center')],
]

background_image = convert_image(cv2.imread("./no-img.png", 1))
upload_image = [
    [
        sg.Text("Upload Image",),
        sg.In(size=(30, 1), enable_events=True, key="IMAGE UPLOAD"),
        sg.FileBrowse(file_types=file_types),
        sg.Button('Enter', key="UPLOAD")
    ],
]

original_image_column = [
    [
        sg.Text("Original Image"),
    ],
    [
        sg.Image(size=(400, 400), key="IMAGE", data=background_image),
    ],
]

filters_column = [
    [
        sg.Text("Gamma", size=(12, 1)),
        sg.Input(size=(10, 1), key="GAMMA"),
        sg.Button("Enter", key="BTN GAMMA"),
    ],
    [
        sg.Text("Histogram ", size=(12, 1)),
        sg.Button("Enter", key="BTN HIS"),
    ],
    [
        sg.Text("Sharpen", size=(12, 1)),
        sg.Button("Enter", key="BTN SHARPEN"),
    ],
    [
        sg.Text("Averaging/Blur", size=(12, 1)),
        sg.Input(size=(10, 1), key="BLUR"),
        sg.Button("Enter", key="BTN BLUR"),
    ],
    [
        sg.Text("Median Blurring", size=(12, 1)),
        sg.Input(size=(10, 1), enable_events=True, key="MEDIAN"),
        sg.Button("Enter", key="BTN MEDIAN"),
    ],
    [
        sg.Text("Ideal Lowpass", size=(12, 1)),
        sg.Input(size=(10, 1), enable_events=True, key="LOWPASS"),
        sg.Button("Enter", key="BTN LOWPASS"),
    ],
    [
        sg.Text("Ideal Highpass", size=(12, 1)),
        sg.Input(size=(10, 1), enable_events=True, key="HIGHPASS"),
        sg.Button("Enter", key="BTN HIGHPASS"),
    ],

    [sg.Push(),
        sg.Button("Clear"),
        sg.VPush(),
     ]
]

filter_image_column = [
    [
        sg.Text("After filter Image")
    ],
    [
        sg.Image(background_color=BACKGROUND_IMAGE_PRAME, size=(
            400, 400), key="FILTER IMAGE", data=background_image)
    ],
]


# ----- Full layout -----


image_layout = [
    [work_lap_title],
    [upload_image],
    [
        sg.Column(original_image_column),
        sg.Column(filters_column),
        sg.Column(filter_image_column),
    ],
    [
        sg.Button('Real Time Video',  size=(15, 1), font='Helvetica 14')
    ]
]
window = sg.Window('Image Filter', image_layout,
                   finalize=True, element_justification='c')


# def make_video_win():
#     video_layout = [[sg.Text('Real Time Video', size=(40, 1), justification='center', font='Helvetica 20')],
#                     [sg.Image(filename='', key='VIDEO')],
#                     [sg.Button('Start', size=(10, 1), font='Helvetica 14'),
#                      sg.Button('Stop', size=(10, 1), font='Any 14'),
#                      sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]
#     return sg.Window('Real Time Video', video_layout, finalize=True)


image = None


def main():
    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "IMAGE UPLOAD" or event == 'UPLOAD':
            try:
                image = cv2.imread(values["IMAGE UPLOAD"], 1)
                image_end = convert_image(image)
                window["IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Have some problems when try to open image, choose another!", title='Error')
        if event == "BTN GAMMA":
            try:
                gamma = float(values["GAMMA"])
                image_end = Filter.gamma_correction(image, (gamma))
                image_end = convert_image(image_end)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Input is a number > 0 pls!", title='Error')

        if event == "BTN BLUR":
            try:
                size = values["BLUR"]
                image_end = Filter.blur(image, int(size))
                image_end = convert_image(image_end)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Input is a odd number > 0 pls!", title='Error')

        if event == "BTN MEDIAN":
            try:
                size = values["MEDIAN"]
                image = Filter.median_blur(image, int(size))
                image_end = convert_image(image)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Input is a odd number > 0 pls!", title='Error')
        if event == 'BTN HIS':
            try:
                image_end = Filter.histogram(image)
                image_end = convert_image(image_end)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Unknow problem!", title='Error')

        if event == 'BTN SHARPEN':
            try:
                image_end = Filter.sharpen(image)
                image_end = convert_image(image_end)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Unknow problem!", title='Error')

        if event == 'BTN LOWPASS':
            image = cv2.imread(values["IMAGE UPLOAD"], 0)
            try:
                size = int(values["LOWPASS"])
                image = Filter.lowpass(image, size)
                image_end = convert_image(image)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Input is a number > 0 pls!", title='Error')

        if event == 'BTN HIGHPASS':
            image = cv2.imread(values["IMAGE UPLOAD"], 0)
            try:
                size = int(values["HIGHPASS"])
                image = Filter.highpass(image, size)
                image_end = convert_image(image)
                window["FILTER IMAGE"].update(data=image_end)
            except:
                sg.Popup(
                    "Input is a number > 0 pls!", title='Error')
        if event == "Real Time Video":
            RealTime_GUI.main()

        if event == "Clear":
            image = None
            window["IMAGE"].update(background_image)
            window["FILTER IMAGE"].update(background_image)

    window.close()


if __name__ == "__main__":
    main()
