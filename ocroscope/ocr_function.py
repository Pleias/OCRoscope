import os
import re
import glob
import json
import string
from statistics import mean 
from random import sample 

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


#Function for text split but this time with an option of using a sample instead
#For long texts, a sample of 1000 should be more than enough to
def split_text(text, segment_length, sample_size = None, min_letter_ratio = .3):
    words = text.split()
    num_segments = (len(words) + segment_length - 1) // segment_length
    list_segment = []
    
    #We initialize the id segment (for sampling)
    #And a count of numeric content (for easier filtering)
    nonchar_content = 0

    #We iterate over the segments and keep them if they pass the heuristic for letter/non-letter ratio
    for i in range(num_segments):
        start = i * segment_length
        end = min(start + segment_length, len(words))
        segment = words[start:end]
        if len(segment) == segment_length:
            if letter_ratio(segment) > min_letter_ratio:
                if len(segment)>0:
                    list_segment.append(' '.join(words[start:end]))
            else:
                nonchar_content += 1
    
    #We activate the sampling mode if there is a sample_size specified and if the number of segments in the text is longer the sample size.
    if sample_size is not None:
        if len(list_segment) >= sample_size:
            list_segment = sample(list_segment, sample_size)
        
    return list_segment, nonchar_content
