# FontSearch

Thank you for checking out FontSearch! FontSearch is an ongoing personal project with the goal of allowing natural language exploration of typography, inspired by the limited search and filter options available on the Google Fonts platform.

## Dataset

### Web Scraping

Over 65,0000 font families were scraped from the free font platform, Font Space. The .otf/.ttf files for each style of each font family was collected, as well as their tagged descriptors (e.g. 'retro', 'invitation', 'handwriting'). The scrape was performed using selenium.

### Font images

Using the .otf/.ttf files for each family and style, grayscale font images of each alphanumeric were generated and compiled onto a 7x8 grid, yielding arrays of shape (448, 448).

### Metadata and cleaning

The descriptive tags available on Font Space are susceptible to inconsistent shortenings and human error -- as such, tags with the same meaning were streamlined (e.g. 'bd', 'bld', 'bold' -> 'bold') and misspellings were corrected as much as possible. That being said, there still may be imperfections in the dataset. 

Tags with fewer than 5 unique instances were trimmed. Families with no styles or tags were also left out of the dataset. In doing so, the original size of over 100,000 families and styles to 93,121 final tagged font images.

### Labeling

There are 4038 unique labels, which are represented in the dataset using one-hot vectors. This leaves us with X of shape (93121, 448, 448) and y of shape (93121, 4038)

## Training

FontSearch is now in the training stage!! Stay tuned for updates! 
