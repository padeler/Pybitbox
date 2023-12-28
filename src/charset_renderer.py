#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
# %% 
# print(ord('9'))
# %% 

def draw_char(char, font, size):
    image = Image.new("1", size, 0)
    d_usr = ImageDraw.Draw(image)
    d_usr = d_usr.text((0, 0), char, 255, font=font)
    
    return image

def prepare_font(font_path, char_range, char_width, char_height, font_size=9):
    img_save_path = "generated/font"
    os.makedirs(img_save_path, exist_ok=True)
    
    usr_font = ImageFont.truetype(font_path, font_size)
    
    ascii = "".join([chr(v) for v in char_range])
    print(f"[{ascii}]")
    char_list = []
    for c in ascii:
        c_img = draw_char(c, usr_font, (char_width, char_height))
        fnt = np.array(list(c_img.getdata(0)), dtype=np.ubyte).reshape(char_height, char_width)
        print(f"===>{c}\n",fnt)
        char_list.append(fnt)
        # save image
        c_img.save(f"{os.path.join(img_save_path,str(ord(c)))}.jpg")

    fnt_tr = np.vstack(char_list)
    
    fnt_packed = np.packbits(fnt_tr, axis=1).ravel()
    print(fnt_packed.shape, fnt_tr.shape)
    
    return fnt_packed
    
def run():
    out_file = "generated/font.h"
    char_range = list(range(32,127))
    out_file = "generated/font09.h"
    char_range = list(range(48,58))
    char_width = 5
    char_height = 10
    
    font_size = 9

    font_path = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    # font_path = "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf"
    # font_path = "res/SFCompactDisplay-Regular.otf"

    fnt_packed = prepare_font(font_path, char_range, char_width, char_height, font_size)

    # Save font to header file
    header = "/* \n" \
             " * ASCII Character set.\n" \
             " * Characters from ASCII [%d,%d].\n" \
             " * Character width %d, Character height %d.\n" \
             " * Character bits are packed horizontally\n" \
             " * Automatically generated from font file: %s\n" \
             " */\n\n"%(char_range[0], char_range[-1], char_width, char_height, font_path)


    with open(out_file, "w") as f:
        f.write(header)
        f.write("#define char_height %d\n"% char_height)
        f.write("#define char_width %d\n" % char_width)
        f.write("#define ascii_first %d\n" % char_range[0])
        f.write("#define charset_size %d\n" % len(char_range))

        f.write("\nconst byte charset[] PROGMEM = { \n")
        for r_idx,v in enumerate(list(fnt_packed)):
            idx = r_idx//char_height
            f.write("\t%s,"%hex(v))
            if r_idx%char_height==0:
                f.write(" // Char \"%s\"" % chr(char_range[idx]))
            f.write("\n")

        f.write("};\n")


if __name__ == '__main__':
    run()
