from colorthief import ColorThief
import matplotlib.pyplot as plt
import colorsys

ct = ColorThief('copy.png')
dominant_color = ct.get_color(quality=1)

# plt.imshow([[dominant_color]])
# plt.show()

palette = ct.get_palette(color_count=10)
plt.imshow([[palette[i] for i in range(len(palette))]])
plt.show()

for color in palette:
    print(color)
    print(f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}')

