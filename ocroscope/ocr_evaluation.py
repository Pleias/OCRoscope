from .ocr_function import detect_languages, letter_ratio, split_text
from statistics import mean 

#Generic class for ocr evaluation
class ocr_evaluation:
    def __init__(self, id = None, text = None):
        self.id = id
        self.text = text
        self.length_text = len(text.split())
    
    def calculate_ocr_rate(self, language_detection_segment = 1000, ocr_detection_segment = 7, sample_size = 1000):
        if self.length_text <= ocr_detection_segment:
            print("Text is too short for OCR rate recognition. Aborting!")
        else:
            text = self.text.replace('-\n', '')

            if self.length_text <= language_detection_segment:
                language_list = []
                for language in detect_languages(self.text):
                    if language[1] > 20:
                        language_list.append(language[0])
            else:
                segments_lang = split_text(text, segment_length = language_detection_segment)
                language_list = []
                for segment in segments_lang:
                    for language in detect_languages(segment):
                        if language[1] > 20:
                            language_list.append(language[0])
                language_list = list(sorted(language_list))

            #Now OCR:
            segments, self.numeric_content = split_text(text, segment_length = ocr_detection_segment, sample_size = 1000)
            self.unidentified_segment = 0
            self.identified_segment = 0
            list_probability = []
            for segment in segments:
                try:
                    language, probability = detect_languages(segment)[0]
                    list_probability.append(probability)
                except:
                    pass
                if language not in language_list:
                    self.unidentified_segment += 1
                else:
                    self.identified_segment += 1
            if (self.identified_segment+self.unidentified_segment) > 0:

                #The final rate with a ratio per 100
                self.ratio_segment = self.unidentified_segment/(self.identified_segment+self.unidentified_segment)
                self.ratio_segment = round(100-(self.ratio_segment*100))
                
                #Rate for numeric content
                self.ratio_numeric = self.numeric_content/(self.identified_segment+self.unidentified_segment+self.numeric_content)
                self.ratio_numeric = round(self.ratio_numeric*100)
                self.probability = mean(list_probability)
            else:
                self.ratio_segment = None
                self.probability = None
                self.ratio_numeric = None
