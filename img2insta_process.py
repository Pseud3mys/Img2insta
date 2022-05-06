from PIL import Image, ImageOps, ImageFont, ImageDraw
from PIL import Image
from PIL.ExifTags import TAGS
import os
from pathlib import Path



def get_info(img):
    """
    lit les parametre utile de l'image
    :return: ApertureValue, FocalLength, ExposureTime, ISOSpeedRatings
    """
    img_exif = img.getexif()

    dico = {}
    for tag_id in img_exif:
        tag = TAGS.get(tag_id, tag_id)
        data = img_exif.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        # print(f"{tag:20}:{data}")
        dico[tag] = data

    ApertureValue = dico["ApertureValue"]
    FocalLength = dico["FocalLength"]
    ExposureTime = dico["ExposureTime"]
    ISOSpeedRatings = dico["ISOSpeedRatings"]
    return ApertureValue, FocalLength, ExposureTime, ISOSpeedRatings


def info2str(info, separator):
    """
    presente joliement les parametres lu
    :param info: get_info()
    :param separator: entre les different parametre
    :return:
    """
    ApertureValue, FocalLength, ExposureTime, ISOSpeedRatings = info
    # ExposureTime = ExposureTime
    str_expo = str(ExposureTime._numerator) + "/" + str(ExposureTime._denominator)
    str_aperture = "f/" + str(float(round(ApertureValue, 1)))
    str_focal = str(int(FocalLength)) + "mm"
    str_iso = "ISO " + str(ISOSpeedRatings)
    s = separator
    out = str_focal + s + str_aperture + s + str_expo + s + str_iso
    if separator == " ":
        max_lenght_text = out
    else:
        m = 0
        max_lenght_text = ""
        for a in [str_focal, str_aperture, str_expo, str_iso]:
            if len(a) > m:
                m = len(a)
                max_lenght_text = a
    return out, max_lenght_text


def _draw_text_90_angle(text: str, into, at, font, color):
    """
    :param into: l'image ou l'ecrire
    :param at: coin haut gauche
    """
    # Measure the text area
    wi, hi = font.getsize(text)

    # Copy the relevant area from the source image
    img = into.crop((at[0], at[1], at[0] + hi, at[1] + wi))

    # Rotate it backwards
    img = img.rotate(270, expand=1)

    # Print into the rotated area
    d = ImageDraw.Draw(img)
    d.text((0, 0), text, font=font, fill=color)

    # Rotate it forward again
    img = img.rotate(90, expand=1)

    # Insert it back into the source image
    into.paste(img, at)


# open image


def isHorizont(img):
    if img.size[1] == max(img.size):
        return False
    else:
        return True


def create_border(img, color, Min):
    """
    crée un bord pour rendre l'image carré.
    :param Min: la taille minimum du plus grand bord (pour écrire)
    :return:
    """
    cote = 0
    haut = 0
    bas = 0
    diff = (max(img.size) - min(img.size)) // 2
    # verticale
    if not isHorizont(img):
        cote = diff
        if cote < Min:
            cote = Min
            haut = cote - diff
            bas = haut
    # horizontale
    else:
        haut, bas = diff, diff
        if bas < Min:
            bas = Min
            haut = int(0.25 * (bas - diff)) + diff
            cote += (haut + bas) // 2 - diff
    border = (cote, haut, cote, bas)
    #print("border size: ", border)
    new_img = ImageOps.expand(img, border=border, fill=color)
    return new_img


def draw_text(square_img, color, text, font, isHorizont):
    """
    draw the text on the square image
    :param isHorizont: is the RAW image horizontale ?
    """
    #
    draw = ImageDraw.Draw(square_img)
    Xmax, Ymax = square_img.size
    wi, hi = font.getsize(text)  # taille du text
    if isHorizont:
        # coin haut gauche
        x = Xmax // 2 - wi // 2
        y = Ymax - int(hi * 1.15)
        draw.text((x, y), text, font=font, fill=color)
    else:
        # coin haut gauche
        x = Xmax - int(hi * 1.15)
        y = Ymax // 2 - wi // 2
        _draw_text_90_angle(text, square_img, (x, y), font, color)


def modify_image(img, color):
    info = get_info(img)
    #
    size = int(max(img.size) * 0.02)  # 2% of the image size
    font = ImageFont.truetype("arial.ttf", size)

    text, max_lenght = info2str(info, "  ")
    text_size = font.getsize(max_lenght)
    Min = int(text_size[1] * 1.30)
    new_img = create_border(img, color, Min)

    if color == "black":
        textcolor = "white"
    else:
        textcolor = "black"
    draw_text(new_img, textcolor, text, font, isHorizont(img))
    return new_img


def modify_images(in_images: [str], out_Dir: str, background_color="white"):
    # Create target Directory if don't exist
    if not os.path.exists(out_Dir):
        os.mkdir(out_Dir)
    i = 0
    for path in in_images:
        i += 1
        imgName = Path(path).stem
        print(str(i)+"/"+str(len(in_images))+" "+imgName)
        img = Image.open(path)
        new_img = modify_image(img, background_color)
        new_img.save(out_Dir+"/"+imgName+"_square.jpg")


#modify_images(["sample.jpg", "sample2.jpg"], "test")