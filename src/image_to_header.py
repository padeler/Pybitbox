'''
Create a header file with byte arrays representing 16x16 RGB images.
'''

import os
import cv2

out_name = "mario"
image_filenames = [
    "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/0.bmp",
    "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/1.bmp",
    "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/2.bmp",
    "/home/padeler/work/RibbaPi/resources/animations/selected/mario0/3.bmp",
        ]


out_name = "ben"
image_filenames = [
    "/home/padeler/work/RibbaPi/resources/animations/art/sw_ben/sw_ben/0.bmp",
    "/home/padeler/work/RibbaPi/resources/animations/art/sw_ben/sw_ben/10.bmp",
    "/home/padeler/work/RibbaPi/resources/animations/art/sw_ben/sw_ben/20.bmp",
    ]


def run():
    imgs = [ cv2.imread(f) for f in image_filenames ]
    out_file = "generated/"+out_name+".h"
    header = "/* \n" \
             " * Assets header: "+out_name+"\n" \
             " * Automatically generated from image files: \n * "+"\n * ".join(image_filenames)+"\n" \
             " */\n\n"


    with open(out_file, "w") as f:
        f.write(header)
        f.write("const uint8_t %s_frames = %d;\n" % (out_name, len(imgs)))
        f.write("\nconst byte %s[] PROGMEM = { \n" % out_name)
        for img in imgs:
            for v in img[:,:,::-1].reshape(-1).tolist():
                f.write("%s," % hex(v))
            f.write("\n")

        f.write("};\n")


if __name__ == '__main__':
    run()