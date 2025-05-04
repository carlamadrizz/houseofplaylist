# houseofplaylist
AI project
What does each file do?
All files connect to create one seamless user interface.

app.py
This file implements the code for the user interface that will generate a playlist for the user based on a mood they enter. In the function "mood_to_genres", each mood is connected to a list of genres. This function is later used to generate a playlist after the mood has been analyzed. To follow along with the mood analyzation, "detect_mood_from_prompt" from mood_parser.py analyzes the text input from the prompt and returns a mood label. Examples include happy, sad, chill.
The user interface utilizes the Streamlit library for the title, text_input, subheader, buttons, etc. It is a great way to format the UI. In regards to the Spotify implementation, this file also loads the environment variables for the Spotify API credentials. Afterwards, the file fetches song reccomendations from Spotify using a Try and Except statement. A playlist is then made using an if-else statement. The user will be notified with a message if a playlist is created and will be provided with a link to that playlist on Spotfiy. It is important to note: the command "streamlit run app.py" launches the web application. 


main.py
This file essentially does the same thing as app.py, although it is command line interface. First, it loads the clients credentials from .env. A .env file stores an application's environment variables or sensitive information; in this case it's the client credientials. Next, it connects and authenticates with Spotify. If there is a user profile currently in use, the user will see a message confirming that they are logged in. This file also uses mood_to_genres to create a map of moods and genres determined by Spotify. Through the terminal, the user will be asked to fill a prompt for their current vibe. Using the functions detect_mood_from_prompt, mood_to_features, and mood_to_genres the mood will be detected and receive its corresponding features and genres. Next, song reccomndations will be extracted from Spotify, a playlist will be created, and a link to that playlist will be provided at the end. This file is run with "python main.py".

mood_parser.py
Contains detect_mood_from_prompt and mood_to_features which are implemented in the other two files. As you could infer, the first function is used to analyze text prompts. It is a keyword-based functiono that maps the user input to a mood. The available moods are as follow: sad, happy, chiill, hype, angry, chill. mood_to_features is in a dictionary format that maps moods to Spotify's audio parameters. Each mood has valence, energy, and tempo parameters. In regards to music, valence is a value of measurement that determines the positivity levels of a song. For example, sad has a valence level of 0.2 whereas hype has a valence level of 0.8.

