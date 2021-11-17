import os
import cv2
import numpy as np

def extract_dice(image_path, bounds, out_dir, base_out_name, tight_crop=False, mask_bgnd=True):
    image = cv2.imread(image_path)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower, upper = bounds
    range_mask = cv2.inRange(hsv_image, lower, upper)
    contours, _ = cv2.findContours(~range_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    i = 0
    for c in contours:
        topy, topx = c.min(0)[0]
        boty, botx = c.max(0)[0]
        ydiff = boty-topy
        xdiff = botx-topx
        if ydiff < 200 or xdiff < 200:
            continue

        if tight_crop:
            if xdiff > ydiff:
                botx += (ydiff-xdiff)
            else:
                boty += (xdiff-ydiff) // 2
                topy -= (xdiff-ydiff) // 2
        else:
            if xdiff > ydiff:
                boty += (xdiff-ydiff) // 2
                topy -= (xdiff-ydiff) // 2
            else:
                botx += (ydiff-xdiff) // 2
                topx -= (ydiff-xdiff) // 2

        final = image
        if mask_bgnd:
            mask = np.zeros_like(image)
            mask = cv2.drawContours(mask, [c], 0, [255,255,255], -1)
            final = np.zeros_like(image)
            final = cv2.bitwise_and(image, mask, mask=None)

        crop = final[topx:botx+1, topy:boty+1]
        crop = cv2.resize(crop, (50, 50), interpolation=cv2.INTER_AREA)
        out_path = os.path.join(out_dir, f"{base_out_name}_{i}.png")
        cv2.imwrite(out_path, crop)
        print(out_path)
        i += 1


def main():
    img_dir = "./orig_img/3"

    bounds = ((50, 0, 0), (140, 255, 255))
    # bounds_rgb = ((0, 0, 0), (80, 255, 255))

    for filename in os.listdir(img_dir):
        if os.path.isdir(os.path.join(img_dir, filename)):
            continue
        path = os.path.join(img_dir, filename)
        extract_dice(path, bounds, os.path.join(img_dir, "mask_crop"), filename.split(".")[0], True, True)
        extract_dice(path, bounds, os.path.join(img_dir, "crop"), filename.split(".")[0], True, False)
        extract_dice(path, bounds, os.path.join(img_dir, "mask"), filename.split(".")[0], False, True)
        extract_dice(path, bounds, os.path.join(img_dir, "cut"), filename.split(".")[0], False, False)

if __name__ == "__main__":
    main()