# OCRoscope
**OCRoscope** is a small python package to measure OCR quality and other related metrics.

<p align="center">
<img src="https://raw.githubusercontent.com/Pleias/ocroscope/main/ocroscope_logo.jpg" alt="ocroscope logo" height="300px"/>
</p>

OCRoscope aims to provide a standardized automated baseline for OCR evaluation. While OCR systems like Tesseract or ABBYY commonly give an estimate of OCR quality, this measure is not always communicated and, even more crucially, is not harmonized and will vary significantly across softwares or versions of the same software.

The standardized measure of OCRoscope can be used to assess the feasibility of several downstream tasks on OCR corpus. For intance, named entity recognition methods relying on syntax analysis usually requires an OCR of sufficient quality, as even an occasional missing word can break up the sentence analysis. This is less of a requirement for other tasks such as supervised classification on occurrence counts of pre-training of transformer models.

OCRoscope relies on cld2 for OCR rate estimation and should run in a little more than 80 languages.

## Use
The easiest way to use OCRoscope is to try the official [demo on Colab](https://colab.research.google.com/drive/1tXJYi6fz9mEWISWBmaLpVgwnLqk1Nive?usp=sharing).

Given a text, OCRoscope will return a python object with associated metrics:
* A standardized rate of OCR quality.
* A standardized rate of non-character content.

```python
from ocroscope import ocr_evaluation
import urllib.request, json

with urllib.request.urlopen("https://raw.githubusercontent.com/Pleias/OCRoscope/main/notebook/sample_french_ocr.json") as url:
    sample_ocr = json.load(url)

from ocroscope import ocr_evaluation

for ocr_text in sample_ocr:
    ocr_estimate = ocr_evaluation(id = ocr_text["file_id"], text = ocr_text["sampled_text"])
    ocr_estimate.calculate_ocr_rate()
    ocr_text["ocr_quality"], ocr_text["nonchar"] = ocr_estimate.ratio_segment, ocr_estimate.ratio_nonchar
```

## Method

OCRoscope leverages the differential results of language detection techniques for short and long OCR texts. On long texts, language detection is usually resilient to mistakes. This is no longer the case when language detection is applied on very short segments. The standard measure of OCR quality in OCRscope checks is based on a ratio of ngrams (7-grams by default) with a language not matching the one detected on long segments.

Language detection is performed by cld2 (through the Python package Pycld2). While better language detection model exists (including cld2 successor, cld3), cld2 is likely the fastest currently available and is struggling more with OCR noises which is unexpectedly a feature for OCRoscope. OCR quality rate estimated through cld2 is rather well distributed, which makes it easier to differentiate really good OCR quality from correct one.

To illustrate the approach, this long text is correctly identified as French with >99% confidence by cld2, as despite the many mistakes, there are enough non-ambiguous French words:

> NOUVELLES POLI TI Q^U E S. Suede. Stockholm , le 2 5 décembre 1792. Le général Toll ira à Varsovie en quarté d'envoyé de la Suede auprès du roi et de la république ; A 1 même rey.u l'ordre de s'y rendra incessamment. 11 paraît que k Uc-régeik a des craintes ; il a fait venir chez l*ji les membres c Ij*``` tribunal 4e la cour , et leur a rtmis son lesfca n at. La fermentation qu'a causée 1 ,'ari r?tavh n k M p v riote Thorild tî'est pas appaisée y le luigage qv'il a yailé an duc-régent a été bien entendu par le peu) k y ir M» (U i n'entendrait pas l'apostrdphe suivante ? ttRxc3xa7nd &gt;la libuk à r otre raison , et ne et nous force pas de i'ache'ef r i te n :e sang,.
>
> Le duc a fait x,épa4idre sur-le-champ une fjtbprijuun à te us les habitans di$ Toyaume , pour les detourntr de mr laisser sé luire par de fa,ux bruits et des jugemens pe rver$ , e i en même temps l'ordre a. été donné à la garnison de charger et de se tenir prête à marcher.
> 
> (*Mercure Français*, 1793, January 25th)

Yet one short ngram ("n k M p v riote Thorild") is classified as unknown by cld2. Complete processing by OCRoscope yiled of rate of 41% non-recognized 7-grams, which results in an OCR quality rate of 59%. In comparison, the self-estimated rate of OCR valid words by the French National Library is significantly higher (85%) for the whole document.
