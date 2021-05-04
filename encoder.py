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

        # Determine the height of the section to be encoded in the image
        ENCODING_HEIGHT = _get_encoding_height()

        # Determine the padding from top, left and right sides
        ENCODING_PADDING = 20
        ENCODING_PADDING_RIGHT = IMAGE_DIMENSIONS[1] - ENCODING_PADDING

        # Characters that have already been encoded
        encoded_characters = list()

        """ FLAGS """
        # The last height and width of the last encoding
        LAST_ROW_HEIGHT = ENCODING_PADDING
        LAST_COL_WIDTH = ENCODING_PADDING

        # Make all characters in the data uppercase
        data = data.upper()
        print(f'DATA => {data}')

        # Loop through the characters of the data provided
        for character in data:
            # The representation of the character in Morse/Binary form
            character_morse_binary = helpers.MORSE_CODE_ENCODING[character]
            
            # Provide the details to an drawing method to make the drawings
            LAST_ROW_HEIGHT, LAST_COL_WIDTH = _draw_data_encodings(
                image=image_data,
                morse_codes=character_morse_binary,
                PADDING_RIGHT=ENCODING_PADDING_RIGHT,
                LAST_ROW=LAST_ROW_HEIGHT,
                LAST_COL=LAST_COL_WIDTH)

        opencv.imshow('Encoded Test Image', image_data)
        opencv.waitKey(0)
    else:
        return 'File not found', None

def _draw_data_encodings(image, morse_codes, PADDING_RIGHT, LAST_ROW, LAST_COL, is_space = True):
    """
    Draws a single character on the image, and returns the last position ended.
    Takes in the image data and the morse/binary encoding of the character to be encoded.
    """
    ROW_HEIGHT = 15
    COL_WIDTH = 15

    points_drawn = dict()

    # make sure the morse_codes is always a tuple
    if type(morse_codes) == int:
        morse_codes = [ morse_codes ]
    
    # check if the morse code will be drawn in full or not
    required_width = _get_required_morse_width(morse_codes)
    remaining_width = (PADDING_RIGHT - COL_WIDTH)
    if required_width < remaining_width:
        for index, code in enumerate(morse_codes):
            for row in range(LAST_ROW, (LAST_ROW + (ROW_HEIGHT + 1))):
                # draw a dash morse code char
                if code == 0:
                    # a dash has 2 times the width of a single column
                    for col in range(LAST_COL + COL_WIDTH, (LAST_COL + (COL_WIDTH * 2) + 1) + COL_WIDTH):
                        # rewrite the pixel to a while color
                        image[row][col - 1] = [ 255, 255, 255 ]

                        # check when the end of drawing the dash has ended
                        if row == (LAST_ROW + ROW_HEIGHT) and col == (LAST_COL + (COL_WIDTH + COL_WIDTH)):
                            LAST_COL = LAST_COL + (COL_WIDTH * 3)
                            if (index + 1) == len(morse_codes):
                                LAST_COL += COL_WIDTH * 2
                                        
                # draw a dot morse code char
                elif code == 1:
                    # a dot has the width of a single column
                    for col in range(LAST_COL + COL_WIDTH, (LAST_COL + COL_WIDTH) + COL_WIDTH):
                        print(LAST_COL)
                        # rewrite the pixel to a while color
                        image[row][col - 1] = [ 255, 255, 255 ]
                        
                        # check when the end of drawing the dot has ended
                        if row == (LAST_ROW + ROW_HEIGHT) and col == (LAST_COL + COL_WIDTH):
                            LAST_COL = LAST_COL + (COL_WIDTH * 2)
                            if (index + 1) == len(morse_codes):
                                LAST_COL += COL_WIDTH * 2

    else:
        print(f'NULL') 
        return LAST_ROW + ROW_HEIGHT, COL_WIDTH       
        # LAST_ROW, LAST_COL = _draw_data_encodings(
        #     image=image,
        #     morse_codes=(),
        #     PADDING_RIGHT=PADDING_RIGHT,
        #     LAST_ROW=(LAST_COL + ROW_HEIGHT),
        #     LAST_COL=COL_WIDTH)

    return LAST_ROW, LAST_COL


# calculates the height to be used to store the encodings of the Facecode.
def _get_encoding_height(MORSE_CODE_HEIGHT: int=20) -> int:
    # the number of rows available for the morse code
    AVAILABLE_ENCODING_ROWS = 6
    return MORSE_CODE_HEIGHT * AVAILABLE_ENCODING_ROWS


# calculates the width required to draw a particular morse encoding
def _get_required_morse_width(morse_codes: tuple) -> int:
    # width of one single morse code
    MORSE_WIDTH = 20
    MORSE_SPACE = 20
    
    required_morse_width = 0
    # calculate the required morse width
    for morse_code in morse_codes:
        if morse_code == 0:
            required_morse_width += ( MORSE_WIDTH * 2 ) + MORSE_SPACE
        else:
            required_morse_width += MORSE_WIDTH + MORSE_SPACE
    return required_morse_width


encode('/Users/libbylebyane/Projects/@Facecode/CONCEPTS/MF_Code/MFCODE_TEMPLATE.png', 'reece')