# OCRoscope
**OCRoscope** is a small python package to measure OCR quality and other related metrics.

OCRoscope aims to provide a standardized automated baseline for OCR evaluation.

<p align="center">
<img src="https://raw.githubusercontent.com/Pleias/ocroscope/main/ocroscope.jpg" alt="marginalia logo" height="150px"/>
</p>

## Typical usage

Given a text, OCRoscope will return a python object with associated metrics:
* A standardized rate of OCR quality.
* A standardized rate of numeric/tabular content.

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
