# Contributors 
Annmarie Zheng
Larry Zhao
Matthew Waldeck
Taran Deshpande

# Running the Reach
Use ```pip``` to install ```numpy```, ```plotly```, ```python-midi```, and ```pygame```. This project was built using Python 2.7, so newer versions may cause compile errors.```pygame``` doesn’t work with the python that comes normally with Apple devices; it only works with the versions of python downloaded form python.org. 

UPDATE: Plotly has since updated to chart_studio which has caused the data visualization component to throw errors due to updated syntax. Since this was not the main component of the project, the data visualization code has been commented out. Sample charts can be seen in in the sample graphs folder. 

This project was a competetive group project created for the EECS 183 Showcase during the 2017 fall semester. The project has two components: the core and the reach. The core was a starting point to direct every group and was designed by course instructors. As such, the results from each group were near identical. When running the program, this can be found under "Option 1: Generate Song Lyrics...". The reach component of the project challenged each group extend the idea of song generation in the best way they could devise. As such, group projects were unique and meant to compete with eachother during the showcase.  Our groups attempt at the core can be found under "Generate a song using data from Nintendo Gamecube" when running the program, and showcases our best attempt at the task. This aspect of the project was unique among showcase competitors and was designed exclusivly our group members. 

To run the program, run ```generate.py```. The lyrics generator from the core has not been altered, but the music generator has been updated to produce songs with different instruments and layers. The user can choose various parameters of the songs to generate off of, or they can have the program randomly select those parameters. If ```pygame``` wasn't installed, after generating a new song, when the program asks if you want to hear the song that has just been generated, enter ```n``` for no. Newly generated songs can be found in the folder "midi." Sample songs that were previously generated can also be found in that folder.


