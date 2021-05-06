"""
GENARATES A MACHINE READABLE CODE THAT CAN STORE A USER'S USERNAME, TO EFFICIENTLY FIND
THIER PROFILES AND SOCIAL MEDIA LINKS. FORMAT THE DATA WILL BE STORED IN IS MORSE CODE.
THEN WILL USE THE HELP BINARY FORMAT TO ASSIST WITH THE DECODING.

MORSE CODE FORMATTING RULES FOR THE FACE CODE: (NAME :=> SIZE :=> MEANING)
-> 1 DOT :=> 25x25 pixels :=> 0 IN BINARY
-> 1 DASH :=> 50x25 pixels :=> 1 IN BINARY
-> 1 SPACE :=> 50x25 pixels :=> NEXT CODE
-> LONG BLUE LINE => NULL
"""

# Dependencies
import cv2 as opencv
import utils.morse_code_encodings as helpers
import os


""" width, row and space of one single morse code character """
ROW_HEIGHT = 15
ROW_SPACE = 15
COL_WIDTH = 15
COL_SPACE = 15
ENCODING_PADDING = 30 # padding of every side on the facecode
USED_WIDTH = ENCODING_PADDING

LAST_COL = ENCODING_PADDING
LAST_ROW = ENCODING_PADDING


# Encodes a provided image with the morse code message given some data
def encode(filepath: str, data: str) -> str:
    # Check if the image exists or not
    file_exists = os.path.exists(filepath)

    if file_exists:
        """ INPUT IMAGE """
        # Read the data from the file provided
        image_data = opencv.imread(filepath)

        """ CONSTANTS """
        # Size of the image loaded
        IMAGE_DIMENSIONS = (len(image_data), len(image_data[0]))
        print(f'Image Dimensions: {IMAGE_DIMENSIONS}')

        # Determine the height of the section to be encoded in the image
        ENCODING_HEIGHT = _get_encoding_height()

        # Determine the padding from top, left and right sides
        ENCODING_PADDING_RIGHT = IMAGE_DIMENSIONS[1] - ENCODING_PADDING
        print(f'Encoding Padding Right: {ENCODING_PADDING_RIGHT}')

        # Make all characters in the data uppercase
        data = data.upper()
        print(f'Encoding Data: {data}')

        # Loop through the characters of the data provided
        for index, character in enumerate(data):
            # The representation of the character in Morse/Binary form
            character_morse_binary = helpers.MORSE_CODE_ENCODING[character]
            
            # Provide the details to an drawing method to make the drawings
            _draw_data_encodings(
                image=image_data,
                morse_codes=character_morse_binary,
                PADDING_RIGHT=ENCODING_PADDING_RIGHT,
                is_last_char=((index + 1) == len(data)))
        
        opencv.imshow('NULL FILL TEST', image_data)
        opencv.waitKey(0)
    else:
        return 'File not found', None

def _draw_data_encodings(image, morse_codes, PADDING_RIGHT, is_last_char = False):
    global LAST_ROW
    global LAST_COL

    """
    Draws a single character on the image, and returns the last position ended.
    Takes in the image data and the morse/binary encoding of the character to be encoded.
    """
    ROW_HEIGHT = 15
    COL_WIDTH = 15

    # the color used to paint the morse code
    MORSE_CODE_COLOR = _get_morse_code_color(image)

    # make sure the morse_codes is always a tuple
    if type(morse_codes) == int:
        morse_codes = [ morse_codes ]
    
    # the index of the last morse code to be encoded
    last_index = 0
    
    # check if the morse code will be drawn in full or not
    required_width = _get_required_morse_width(morse_codes)

    remaining_width = (len(image[0]) - LAST_COL - ENCODING_PADDING)

    if required_width <= remaining_width:

        # loop through every single morse binary code
        for index, code in enumerate(morse_codes):

            # also loop through every row needed to make a row of morse codes
            for row in range(LAST_ROW, (LAST_ROW + (ROW_HEIGHT + 1))):

                # draw a dash morse code char
                if code == 0:

                    # a dash has 2 times the width of a single column
                    for col in range(LAST_COL + COL_WIDTH, (LAST_COL + (COL_WIDTH * 2) + 1) + COL_WIDTH):

                        # rewrite the pixel to a while color
                        image[row][col - 1] = MORSE_CODE_COLOR

                        # check when the end of drawing the dash has ended
                        if row == (LAST_ROW + ROW_HEIGHT) and col == (LAST_COL + (COL_WIDTH + COL_WIDTH)):
                            LAST_COL = LAST_COL + (COL_SPACE * 3)

                            # check if the end of a morse code has been reached to add a double space
                            if (index + 1) == len(morse_codes):
                                LAST_COL += COL_SPACE * 2
                                        
                # draw a dot morse code char
                elif code == 1:

                    # a dot has the width of a single column
                    for col in range(LAST_COL + COL_WIDTH, (LAST_COL + COL_WIDTH) + COL_WIDTH):
                        
                        # rewrite the pixel to a while color
                        image[row][col - 1] = MORSE_CODE_COLOR
                        
                        # check when the end of drawing the dot has ended
                        if row == (LAST_ROW + ROW_HEIGHT) and col == (LAST_COL + COL_WIDTH):
                            
                            # give some space for the next morse character
                            LAST_COL = LAST_COL + (COL_SPACE * 2)

                            # check if the morse code has reached the end and make a double space
                            if (index + 1) == len(morse_codes):
                                LAST_COL += COL_SPACE * 2

    # when there is no more space to encode the morse code
    else:
        # fill up the columns with NULL data
        _fill_null(image=image, null_row=LAST_ROW, null_col=LAST_COL)

        LAST_ROW = LAST_ROW + (ROW_HEIGHT + 1)
        LAST_COL = ENCODING_PADDING

        # after filling the last row with NULL data, move to the next row to encode the next morse code
        _draw_data_encodings(
            image=image,
            morse_codes=morse_codes,
            PADDING_RIGHT=PADDING_RIGHT,
            is_last_char=is_last_char
        )


    # Check if this was the last character being encoded
    if is_last_char:
        # check if there is any width left to fill it in with NULL data
        remaining_width = len(image[0]) - USED_WIDTH
        if remaining_width > 3:
            _fill_null(image=image, null_row=LAST_ROW, null_col=LAST_COL)

    return LAST_ROW, LAST_COL


# calculates the height to be used to store the encodings of the Facecode.
def _get_encoding_height(MORSE_CODE_HEIGHT: int=20) -> int:
    # the number of rows available for the morse code
    AVAILABLE_ENCODING_ROWS = 6
    return MORSE_CODE_HEIGHT * AVAILABLE_ENCODING_ROWS


# calculates the width required to draw a particular morse encoding
def _get_required_morse_width(morse_codes: tuple) -> int:
    required_morse_width = 0
    # calculate the required morse width
    for morse_code in morse_codes:
        if morse_code == 0:
            dash_width = ( COL_WIDTH * 2 )
            space_width = ( COL_WIDTH * 2 )
            
            required_morse_width +=  (dash_width + space_width)
        else:
            dot_width = COL_WIDTH
            space_width = COL_WIDTH * 2
            
            required_morse_width += (dot_width + space_width)
    return required_morse_width


# takes in a number of the width remaining and the last row to fill it with NULL data
def _fill_null(image: list, null_col: int, null_row: int) -> None:
    # every single row of pixels of the null space
    for row in range(null_row, (null_row + ROW_HEIGHT) + 1):
        # every single pixel in the picture / null space
        for col in range(null_col + COL_SPACE, (len(image[0])) - ENCODING_PADDING):
            image[row][col] = [ 150, 20, 20 ]


# takes in the image loaded and determines whether or not it's dark or light to select the approriate color
# returns a color of the morse code in RGB suitable for the image
def _get_morse_code_color(image: list) -> list:
    blur_image = opencv.blur(image.copy(), (5, 5))
    if opencv.mean(blur_image)[0] > 127:
        return [0, 0, 0]
    else:
        return [255, 255, 255]

    


encode('/Users/libbylebyane/Projects/@Facecode/CONCEPTS/MF_Code/MFCODE_TEMPLATE.png', 'gingaandvanila')