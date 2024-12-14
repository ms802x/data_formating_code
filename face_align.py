import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def align_face(frames,faces):
    """
    Align face by rotating the frame so that the eyes are horizontal.

    :param frame: The input image (frame) as a NumPy array.
    :param left_eye: The coordinates of the left eye as [x, y].
    :param right_eye: The coordinates of the right eye as [x, y].
    :return: The rotated (aligned) frame.
    """
    right_mouth = faces[0][0][1][3]
    left_mouth = faces[0][0][1][4]
    x1,x2,y1,y2 = map(int,faces[0][0][0])
    frame = frames[0]

    # Calculate the angle between the eyes
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = 180+np.degrees(np.arctan2(dy, dx))  # Angle in degrees
    angle = -angle
    # Get the center of the eyes
    eyes_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)

    # Rotation matrix: rotate around the center of the eyes
    rotation_matrix = cv2.getRotationMatrix2D(eyes_center, angle, 1)

    # Rotate the image to align the eyes horizontally
    aligned_face = cv2.warpAffine(frame, rotation_matrix, (frame.shape[1], frame.shape[0]))
    crop_aligned_face = aligned_face[x2:x1,y2:y1]
    xmr1,ymr1 =  map(int,right_mouth)
    xml1,yml1 =  map(int,left_mouth)
    return aligned_face[yml1-10:ymr1+20,xmr1-20:xml1]
    

# Assuming frames[0] is the image to align
aligned_face = align_face(frames, faces)
