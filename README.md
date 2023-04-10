# font-family
A tool that clusters fonts together based on their visual similarity. 

## To use:
1. Place fonts in the `fonts` folder. The more fonts the better!

2. Run `font-to-img-metadata.py`. This extracts metadata and a sheet of glyphs into the `output` folder.

3. Run `extract-features.py` This assigns each font to one of 5 clusters, and for now they are displayed visually in a folder called `collage`. 

4. ???

5. Profit.

## To do:
* Cluster based on a better algorithm
* Store the fonts and their vector scores in a vector database
* Let them talk via an API


*This project was co-authored by ChatGPT, because I am a designer.*
