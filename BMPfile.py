def OMG_AN_IMAGE(file_name: str, pixels: list, width: int, height: int):
    '''
    file_name: name of the file with no extension
    
    pixels: list of Blue Green Red pixels integers values eg: 
    [0xff, 0xff, 0xff, 0xed, 0xed, 0xd] two pixels

    width: width of the image a integer number (in pixels)
    heigth: heigth of the image a integer number (in pixels)'''

    if len(pixels) / 3 != width * height:
        raise ValueError('Some pixels are missing in your list.')
    
    if type(file_name) != str or type(pixels) != list or type(width) != int or type(height) != int:
        raise ValueError('Some argument is not the right type.')

    def b_array(int_list: list, size: int = 4):
        '''int_list lenght has to be less or equal size'''
        return bytearray(int_list + [0x0] * (size - len(int_list)))

    def pixel_bmp(BGR_pixel_list: list, bmp_width: int):
        count = 0
        canva = list()
        for code in BGR_pixel_list:
            count += 1
            canva.append(code)
            if count % (bmp_width * 3) == 0:
                canva += [0] * (4 - ((bmp_width * 3) % 4))

        return bytearray(canva)
        
    def find_size(numb: int):
        size = 54 + numb
        if size / 255**4 >= 1:
            raise ValueError('image size too big')
        
        else:
            bfour = int(size/255**3)
            bthree = int((size % 255**3) / 255**2)
            btwo = int(((size % 255**3) % 255**2) / 255)
            bone = int(((size % 255**3) % 255**2) % 255)
    
        return [bone, btwo, bthree, bfour]
    
    # creating pixels 

    bitmap = pixel_bmp(pixels, width)

    # creating the header

    tag = bytearray([0x42, 0x4d])
    file_size = b_array(find_size(len(bitmap)))
    reserved = b_array([])
    offset = b_array([0x36])

    header = tag + file_size + reserved + offset

    # creating DIB header

    dib_size = b_array([0x28])
    img_width = b_array([width])
    img_height = b_array([height])
    color_planes = b_array([0x1], 2)
    bpp = b_array([0x18], 2)
    compression = b_array([])
    img_size = b_array([])
    horizontal_resolution = b_array([0xc5])
    vertical_resolution = b_array([0xc5])
    palette = b_array([])
    important_colors = b_array([])

    dib_header = dib_size + img_width + img_height + color_planes + bpp + compression + img_size + horizontal_resolution + vertical_resolution + palette + important_colors


    with open('{}.bmp'.format(file_name), 'wb') as file:
        file.write(header + dib_header + bitmap)
