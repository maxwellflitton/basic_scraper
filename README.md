# basic_scraper
basic web scraper written in python. 

## install using pip
```
pip install git+https://github.com/maxwellflitton/basic_scraper.git#egg=basic_scraper
```

## Use
Use directly by using the ```BasicWorker``` object:

```python
from basic_scaper.worker import BasicWorker

example = BasicWorker(url="https://www.johnlewis.com/browse/men/mens-t-shirts/_/N-ebg")

labels = example.word_filter(tag_type="span", class_name="product-card__title-inner")
image_data = example.image_filter(tag_type="img", class_name="product-card__image")
```

## Threaded
There's a threaded support for getting image data. It roughly halves the time it takes 
to complete:

threaded: 0.2209627628326416

sequential: 0.49100375175476074

```python
from basic_scaper.worker import BasicWorker

example = BasicWorker(url="https://www.johnlewis.com/browse/men/mens-t-shirts/_/N-ebg")
image_data = example.threaded_image_filter(tag_type="img", class_name="product-card__image")
```

