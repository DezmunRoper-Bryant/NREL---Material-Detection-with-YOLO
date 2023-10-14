# from rescale import *
import cv2 as cv
import numpy as np


# rescale an image by some scale
def rescaleFrame(frame, scale=0.75):
    # works with images, videos, and live videos
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


# rescale a live video
def changeRes(capture, width, height):
    # Only works with live video
    capture.set(3, width)
    capture.set(4, height)


# read an image
def showPicture(location, scale=0.75):
    img = cv.imread(location)
    img_resized = rescaleFrame(img, scale)
    cv.imshow('Cat', img_resized)
    cv.waitKey(0)


# read a video
def showVideo(location, scale=1):
    capture = cv.VideoCapture(location)
    while True:
        isTrue, frame = capture.read()
        frame_resized = rescaleFrame(frame, scale)
        cv.imshow('Video', frame_resized)

        if cv.waitKey(20) & 0xFF == ord('d'):
            break
    capture.read()
    cv.destroyAllWindows()


# resize an image based on the square size you want it to be
# def pixel_adjust(image_url, pixel_count):
#     picture = cv.imread(image_url)
def pixel_adjust(image_url, pixel_count):
    picture = image_url
    if picture.shape[0] > pixel_count:
        picture = rescaleFrame(picture, pixel_count / (picture.shape[0]))
    if picture.shape[1] > pixel_count:
        picture = rescaleFrame(picture, pixel_count / (picture.shape[1]))

    blank_image = np.zeros((pixel_count, pixel_count, 3), dtype=np.uint8)

    # Calculate the position to center the image
    x_offset = int((pixel_count - picture.shape[1]) / 2)
    y_offset = int((pixel_count - picture.shape[0]) / 2)

    # Copy the resized image to the centered position
    blank_image[y_offset:y_offset + picture.shape[0], x_offset:x_offset + picture.shape[1]] = picture

    return blank_image
