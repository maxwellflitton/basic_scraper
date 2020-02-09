# basic_scraper
basic web scraper written in python. 

## Use
Use directly by using the ```BasicWorker``` object:

```python
from basic_scaper.worker import BasicWorker

example = BasicWorker(url="https://www.johnlewis.com/browse/men/mens-t-shirts/_/N-ebg")

labels = example.word_filter(tag_type="span", class_name="product-card__title-inner")
image_data = example.image_filter(tag_type="img", class_name="product-card__image")
```



