# OCRoscope
**OCRoscope** is a small python package to measure OCR quality and other related metrics.

<p align="center">
<img src="https://raw.githubusercontent.com/Pleias/ocroscope/main/ocroscope_logo.jpg" alt="ocroscope logo" height="300px"/>
</p>

OCRoscope aims to provide a standardized automated baseline for OCR evaluation. While OCR systems like Tesseract or ABBYY commonly give an estimate of OCR quality, this measure is not always communicated and, even more crucially, is not harmonized and will vary significantly across softwares or versions of the same software. The standardized measure of OCRoscope can be used to assess the feasibility of several downstream tasks on OCR corpus. For intance, named entity recognition methods relying on syntax analysis usually requires an OCR of sufficient quality, as even an occasional missing word can break up the sentence analysis. This is less of a requirement for other tasks such as supervised classification on occurrence counts of pre-training of transformer models.

## Methodology

OCRoscope leverages the differential results of language detection techniques for short and long OCR texts. On long texts, language detection is usually resilient to mistakes. This is no longer the case when language detection is applied on very short segments. The standard measure of OCR quality in OCRscope checks is based on a ratio of ngrams (7-grams by default) with a language not matching the one detected on long segments.

Consequently, OCRoscope does not yield a rate of recognized vs. non-recognized words, even though both indicators should be largely correlated.

## Typical usage

Given a text, OCRoscope will return a python object with associated metrics:
* A standardized rate of OCR quality.
* A standardized rate of non-character content.

```python
from ocroscope import ocr_evaluation
import pandas as pd
import json

current_data = json.load(open("french_ocr.json"))

for element in current_data:
    ocr_estimate = ocr_evaluation(id = element["file_id"], text = element["sampled_text"])
    ocr_estimate.calculate_ocr_rate()
    element["ocr_quality"], element["numeric_content"] = ocr_estimate.ratio_segment, ocr_estimate.ratio_numeric

with open("estimate_french_ocr.json", 'w') as text_write:
    json.dump(current_data, text_write)
```
