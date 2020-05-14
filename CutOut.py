import numpy as np
from PIL import Image

class Cutout(object):
    def __init__(self, hole_size):
        # 正方形马赛克的边长，像素为单位
        self.hole_size = hole_size

    def __call__(self, img):
        return cutout(img, self.hole_size)


def cutout(img, hole_size):
    y = np.random.randint(32)
    x = np.random.randint(32)

    half_size = hole_size // 2

    x1 = np.clip(x - half_size, 0, 32)
    x2 = np.clip(x + half_size, 0, 32)
    y1 = np.clip(y - half_size, 0, 32)
    y2 = np.clip(y + half_size, 0, 32)

    imgnp = np.array(img)

    imgnp[y1:y2, x1:x2] = 0
    img = Image.fromarray(imgnp.astype('uint8')).convert('RGB')
    return img