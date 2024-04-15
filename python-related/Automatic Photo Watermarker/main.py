from tkinter import *
from PIL import Image, ImageDraw, ImageFont


# - - - - - - - - - - - - - - - - - - - - - - - - IMAGE PROCESSING - - - - - - - - - - - - - - - - - - - - - - - - - -
def set_watermark(image_path, custom_text):
    img = image_path.replace('\\', '/')

    with Image.open(img).convert('RGBA') as base_image:
        watermark_image = Image.new(mode='RGBA', size=base_image.size, color=(255, 255, 255, 0))
        watermark_font = ImageFont.truetype(font='verdana', size=40)

        drawing_board = ImageDraw.Draw(watermark_image)
        drawing_board.text(xy=(80, 80), text=custom_text, font=watermark_font, fill=(255, 255, 255, 255))

        processed_image = Image.alpha_composite(im1=base_image, im2=watermark_image)
        # processed_image.show()
        processed_image.save('watermarked_pic' + '.png')

# - - - - - - - - - - - - - - - - - - - - - - - - IMAGE PROCESSING - - - - - - - - - - - - - - - - - - - - - - - - - -


def user_input():
    path = box_drop.get()  # input('Enter the image path: -> ')
    text = 'mh23'  # input('Enter the text you want: -> ')
    set_watermark(image_path=path, custom_text=text)


# - - - - - - - - - - - - - - - - - - - - - - - - - TKINTER PART - - - - - - - - - - - - - - - - - - - - - - - - - - -
window = Tk()  # UI setup...

window.minsize(width=300, height=100)
window.title('Photo Watermarker')
window.config(padx=20, pady=20)

# buttons...
drop_label = Label(text='Drop Image Path: ')
drop_label.grid(row=0, column=0)

# entry_boxs...
box_drop = Entry()
box_drop.grid(row=0, column=1, columnspan=2)

# buttons...
process_button = Button(text='Start Processing', command=user_input)
process_button.grid(row=1, column=1)

window.mainloop()  # for keeping the screen on...

# - - - - - - - - - - - - - - - - - - - - - - - - - TKINTER PART - - - - - - - - - - - - - - - - - - - - - - - - - - -
