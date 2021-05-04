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


def encode(image_path, data: str):
    """
    Takes an image file path and encodes the data provided to this function in string.
    `image_path`: The path of the image to be encoded with data provided.
    `data`: The data to encoded in the image provided.
    """
    # Read the image file to be encoded to get the RGB Values of the image
    image_data = opencv.imread(image_path)

    # Encoding section height, without any padding
    total_encoding_height = get_encoding_height()

    # The padding of the encoding section, same size as one morse code dot
    PADDING = 25
    PADDING_RIGHT = (len(image_data[0]) - PADDING)
    
    encoded_characters = list() # Characters that have already been encoded

    # CHARACTER FLAGS
    character_index = 0 # The position of the character to be encoded on the image
    morse_height = 0
    morse_width = 0 # The number of pixels that have been processed
    morse_index = 0
    
    current_binary = 0
    is_skip_pixel = False # Determines whether a space has been found or not
    is_double_skip = False
    
    # Go through every single row of pixels using the total_encoding_height
    for row in range(0, total_encoding_height):
        # End the row loop if all data has been encoded
        if (len(data) - 1) != character_index:            
            # Apply the padding to the row of the encoding
            if row not in range(0, PADDING):
                # Go through every character to find their morse code
                for col, pixel in enumerate(image_data[row]):
                    # Apply padding to the every pixel columns
                    if col not in range(0, PADDING) and col <= PADDING_RIGHT:
                        # Check if a space has been reached
                        if not is_skip_pixel:
                            if len(data) != (character_index + 1):
                                morse_encoding = helpers.MORSE_CODE_ENCODING[data[character_index].capitalize()]
                                morse_width += 1

                                if morse_index < len(morse_encoding) and morse_encoding[morse_index] == 1:
                                    image_data[row][col] = [ 255, 255, 255 ]
                                else:
                                    pass

                                # Check if a space has been reached
                                if morse_width == 25:
                                    if morse_index < len(morse_encoding):
                                        if morse_encoding[morse_index] == 0:
                                            is_skip_pixel = True
                                            is_double_skip = True
                                    morse_width = 0
                                    morse_index += 1
                            else:
                                # TODO: Create a NULL dash
                                print('NULL')
                                break
                        else:
                            # Give a space without writing anything
                            morse_width += 1
                            if morse_width == 25:
                                morse_width = 0
                                is_skip_pixel = False
                    else:
                        pass

                # Increment the height of the morse code and check whether or not to move to the next line
                morse_height += 1
                if morse_height == 25:
                    character_index += 1
                    print(character_index)
                    morse_height = 0
            else:
                pass
        else:
            print('END')
            break

    opencv.imshow('Encoded Image', image_data)
    opencv.waitKey(0)


def get_encoding_height(morse_code_size=25):
    """
    Calculates the height to be used to store the encodings in the Facecode.
    
    param `morse_code_size`: The size of one morse code dot in pixels, default=25
    """
    # The size of one morse code dot
    MORSE_CODE_SIZE = 25
    # The height of the section that stores the Morse Facecode
    ENCODING_SECTION_HEIGHT = MORSE_CODE_SIZE * 6

    # Return the calcalated value
    return ENCODING_SECTION_HEIGHT


encode('/Users/libbylebyane/Projects/@Facecode/CONCEPTS/MF_Code/MFCODE_TEMPLATE.png', 'le')