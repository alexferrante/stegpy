from PIL import Image

class Merge(object):
    def toInt(rgb):
        r, g, b = rgb
        return (int(r,2), int(g,2), int(b,2))
    def toBinary(rgb):
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))
    def overlayBinary(rgb_A, rgb_B):
        r1, g1, b1 = rgb_A
        r2, g2, b2 = rgb_B
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb
    def encode(image_A, image_B, out):
        pixels_A = image_A.load()
        pixels_B = image_B.load()

        res = Image.new(image_A.mode, image_A.size)
        pixels_res = res.load()

        for i in range(image_A.size[0]):
            for j in range(image_A.size[1]):
                rgb_A = Merge.toBinary(pixels_A[i, j])
                rgb_B = Merge.toBinary((0, 0, 0))
                if i < image_B.size[0] and j < image_B.size[1]:
                    rgb_B = Merge.toBinary(pixels_B[i, j])
                rgb = Merge.overlayBinary(rgb_A, rgb_B)
                pixels_res[i, j] = Merge.toInt(rgb)
        res.save(out)
    def decode(image, out):
        pixels = image.load()
        res = Image.new(image.mode, image.size)
        pixels_res = res.load()
        res_size = image.size

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                r, g, b = Merge.toBinary(pixels[i, j])
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')
                pixels_res[i ,j] = Merge.toInt(rgb)
                if pixels_res[i, j] != (0, 0, 0):
                    res_size = (i + 1, j + 1)
        res = res.crop((0, 0, res_size[0], res_size[1]))
        res.save(out)
        
image_A = Image.open("final.png")
image_B = Image.open("secret.png")
Merge.encode(image_A, image_B, "pic.png")
    
