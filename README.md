# font-family
A tool that clusters fonts together based on their visual similarity. 

## To use:

0. Install the prerequisites using after having installed Python 3: ``` pip : -r requirements.txt ```

1. Place fonts in the `fonts` folder. The more fonts the better!

2. Run `font-to-img-metadata.py`. This extracts metadata and a sheet of glyphs into the `output` folder.

3. Run `similarity-calculator.py`.

4. Run `cluster-visualizer.py`.

5. ???

6. Profit.

## To do:
* Cluster based on a better algorithm
* Store the fonts and their vector scores in a vector database
* Let them talk via an API


*This project was co-authored by ChatGPT, because I am a designer.*
