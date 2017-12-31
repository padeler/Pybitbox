#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
import numpy as np

import PIL

def run():
    out_file = "generated/font.h"
    char_range = list(range(32,127))
    # char_range = list(range(48,51))
    char_width = 5
    char_height = 10

    image = Image.new("1", (char_width*len(char_range), char_height), 0)
    font_path = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
    # font_path = "res/SFCompactDisplay-Regular.otf"
    usr_font = ImageFont.truetype(font_path, 9)
    d_usr = ImageDraw.Draw(image)

    ascii = "".join([chr(v) for v in char_range])
    print ascii

    d_usr = d_usr.text((0, 0), ascii, 255, font=usr_font)

    image.save("generated/test.png")
    cols, rows = image.size
    fnt = np.array(list(image.getdata(0)), dtype=np.ubyte).reshape(rows, cols)
    fnt_tr = np.zeros((char_height*len(char_range), char_width), dtype=np.ubyte)

    for idx in range(len(char_range)):
        # print "===>\n",fnt[:,idx*char_width:(idx+1)*char_width]
        fnt_tr[idx*char_height:(idx+1)*char_height, :] = fnt[:,idx*char_width:(idx+1)*char_width]

    # print fnt[:, 16*5:19*5]
    v = ord('0') - 32;
    print fnt_tr[v*char_height:(v+3)*char_height,:]

    fnt_packed = np.packbits(fnt_tr, axis=1).ravel()
    print fnt_packed.shape, fnt_tr.shape


    header = "/* \n" \
             " * ASCII Character set.\n" \
             " * Characters from ASCII [%d,%d).\n" \
             " * Character width %d, Character height %d.\n" \
             " * Character bits are packed horizontally\n" \
             " * Automatically generated from font file: %s\n" \
             " */\n\n"%(char_range[0], char_range[-1], char_width, char_height, font_path)


    with open(out_file, "w") as f:
        f.write(header)
        f.write("const uint8_t char_height = %d;\n"% char_height)
        f.write("const uint8_t char_width = %d;\n" % char_width)
        f.write("const uint8_t ascii_first = %d;\n" % char_range[0])
        f.write("const uint8_t charset_size = %d;\n" % len(char_range))

        f.write("\nconst byte charset[] PROGMEM = { \n")
        for r_idx,v in enumerate(list(fnt_packed)):
            idx = r_idx/char_height
            f.write("\t%s,"%hex(v))
            if r_idx%char_height==0:
                f.write(" // Char \"%s\"" % chr(char_range[idx]))
            f.write("\n")

        f.write("};\n")



if __name__ == '__main__':
    run()
