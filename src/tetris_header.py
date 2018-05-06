# 0 ==> empty block
# 1 ==> piece block
# 2 ==> occupied block


I = [
     [ 0, 0, 1, 0,
       0, 0, 1, 0,
       0, 0, 1, 0,
       0, 0, 1, 0,],

     [ 0, 0, 0, 0,
       0, 0, 0, 0,
       0, 0, 0, 0,
       1, 1, 1, 1,],
    ]

O = [
      [ 0, 0, 0, 0,
        0, 0, 0, 0,
        0, 1, 1, 0,
        0, 1, 1, 0,],
    ]


L = [
      [ 0, 0, 0, 0,
        0, 1, 0, 0,
        0, 1, 0, 0,
        0, 1, 1, 0,],

      [0, 0, 0, 0,
       0, 0, 0, 0,
       0, 0, 0, 1,
       0, 1, 1, 1, ],

      [0, 0, 0, 0,
       0, 1, 1, 0,
       0, 2, 1, 0,
       0, 2, 1, 0, ],

      [0, 0, 0, 0,
       0, 0, 0, 0,
       0, 1, 1, 1,
       0, 1, 2, 2, ],
    ]

pieces = [
    I[0],I[1],I[0],I[1],
    L[0],L[1],L[2],L[3],
]


out_name = "tetris_pieces"
def run():
    out_file = "generated/"+out_name+".h"
    header = "/* \n" \
             " * Assets header: "+out_name+"\n" \
             " */\n\n"

    with open(out_file, "w") as f:
        f.write(header)
        f.write("\nconst byte %s[][16] PROGMEM = { \n" % out_name)
        for p in pieces:
            f.write("\n{ ")
            for v in p:
                f.write("%s," % hex(v))
            f.write("}")
        f.write("};\n")

if __name__ == '__main__':
    run()