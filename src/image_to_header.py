'''
Create a header file with byte arrays representing 16x16 RGB images.
'''

import os
import cv2

# out_name = "mario"
# image_filenames = [
#     "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/1.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/2.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/3.bmp",
#         ]
#

# out_name = "ben"
# image_filenames = [
#     "/home/padeler/work/RibbaPi/resources/animations/art/speeder/speeder/0.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/art/speeder/speeder/1.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/art/speeder/speeder/2.bmp",
#     ]
#

#
# out_name = "fire"
# image_filenames = [
#     "/home/padeler/work/RibbaPi/resources/animations/gameframe/fire/0.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/gameframe/fire/1.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/gameframe/fire/2.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/gameframe/fire/3.bmp",
#     "/home/padeler/work/RibbaPi/resources/animations/gameframe/fire/4.bmp",
#     ]


out_name = "heart"
image_filenames = [
    "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/0.bmp",
    "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/1.bmp",
    "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/2.bmp",
    ]

def run():

    target_size = (16,16)
    res_imgs = [ cv2.imread(f) for f in image_filenames ]
    # res_imgs = [cv2.resize(i, target_size, interpolation=cv2.INTER_NEAREST) for i in res_imgs]

    out_file = "generated/"+out_name+".h"
    header = "/* \n" \
             " * Assets header: "+out_name+"\n" \
             " * Automatically generated from image files: \n * "+"\n * ".join(image_filenames)+"\n" \
             " */\n\n"


    with open(out_file, "w") as f:
        f.write(header)
        f.write("#define %s_frames %d\n" % (out_name, len(res_imgs)))
        f.write("#define %s_width %d\n" % (out_name, target_size[0]))
        f.write("#define %s_height %d\n" % (out_name, target_size[1]))
        f.write("\nconst byte %s[] PROGMEM = { \n" % out_name)
        for img in res_imgs:
            for v in img[:,:,::-1].reshape(-1).tolist():
                f.write("%s," % hex(v))
            f.write("\n")

        f.write("};\n")


if __name__ == '__main__':
    run()