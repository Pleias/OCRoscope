import os
import re
import glob
import json
import string
from statistics import mean 

import pycld2 as cld2

#Generic function to detect languages
def detect_languages(segment):
    langs = cld2.detect(segment)[2]
    result = [(lang[1], lang[2]) for lang in langs]
    result.sort(key=lambda x: x[1], reverse=True)
    return result[:3]


#Counting the ratio of non-letters to letters but there must be a better way.
def letter_ratio(s):
    letter_count = sum(char.isalpha() for char in s)
    non_letter_count = len(s) - letter_count
    
    # Calculate the ratio
    if non_letter_count == 0:
        ratio = 1
    else:
        ratio = letter_count / non_letter_count
    return ratio

#Generic function to split texts into segments.
#(cannot use the sample version for everything )
def split_text(text, segment_length):
    words = text.split()
    num_segments = (len(words) + segment_length - 1) // segment_length
    list_segment = []
    id_segment = 0
    for i in range(num_segments):
        start = i * segment_length
        end = min(start + segment_length, len(words))
        segment = words[start:end]
        if len(segment) == segment_length:
            list_segment.append(' '.join(words[start:end]))
    return list_segment

#Function for text split but this time with an option of a sampling ratio.
#10 => 1 ngram out of 10.
#Speeds up processing significantly but at a cost in accuracy for short texts.
def split_text_sampling(text, segment_length, sampling_ratio = 1, min_letter_ratio = .3):
    words = text.split()
    num_segments = (len(words) + segment_length - 1) // segment_length
    list_segment = []

    #If there are less segments than the squared sampling ratio we redefine it to get a fixed number of segments
    #(maybe we should take ^3 instead)
    if num_segments <= sampling_ratio^2:
        if num_segments >= sampling_ratio:
            sampling_ratio = round(num_segments/sampling_ratio)
        else:
            sampling_ratio = 1
    
    #We initialize the id segment (for sampling)
    #And a count of numeric content (for easier filtering)
    id_segment = 0
    numeric_content = 0
    for i in range(num_segments):
        id_segment = id_segment+1
        start = i * segment_length
        end = min(start + segment_length, len(words))
        segment = words[start:end]
        if len(segment) == segment_length:
            if (id_segment % sampling_ratio) == 0:
                if letter_ratio(segment) > min_letter_ratio:
                    if len(segment)>0:
                        list_segment.append(' '.join(words[start:end]))
                else:
                    numeric_content += 1
    return list_segment, numeric_content
