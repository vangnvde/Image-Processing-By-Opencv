import cv2
import numpy as np


def gamma_correction(image, gamma):
    invGamma = 1 / gamma
    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)
    imgGamma = cv2.LUT(image, table)
    return imgGamma


def sharpen(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    # kernel = np.array([[-1,-1,-1],
    #                    [-1, 9,-1],
    #                    [-1,-1,-1]])
    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    return image_sharp


def histogram(image):
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img_output


def blur(image, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.float32)/kernel_size**2
    dst = cv2.filter2D(image, -1, kernel)
    return dst


def median_blur(image, kernel_size):
    median = cv2.medianBlur(image, kernel_size)
    return median


def lowpass(image, size):
    F = np.fft.fft2(image)
    Fshift = np.fft.fftshift(F)
    M, N = image.shape
    H = np.zeros((M, N), dtype=np.float32)
    D0 = size
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            if D <= D0:
                H[u, v] = 1
            else:
                H[u, v] = 0
    Gshift = Fshift * H
    G = np.fft.ifftshift(Gshift)
    g = np.abs(np.fft.ifft2(G))
    return g


def highpass(image, size):
    F = np.fft.fft2(image)
    Fshift = np.fft.fftshift(F)
    M, N = image.shape
    H = np.zeros((M, N), dtype=np.float32)
    D0 = size
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            if D <= D0:
                H[u, v] = 1
            else:
                H[u, v] = 0
    H = 1 - H
    Gshift = Fshift * H
    G = np.fft.ifftshift(Gshift)
    g = np.abs(np.fft.ifft2(G))
    return g
