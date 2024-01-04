<h1>Lyrics2Images</h1>

Lyrics2Images is a versatile application that transforms song lyrics into visually stunning images. By leveraging the Genius API, it seamlessly retrieves lyrics based on the artist and song entered by the user. The application provides a user-friendly interface with various customization options, allowing you to generate images tailored to your preferences.
Features

    Genius API Integration: Automatically fetches lyrics for the specified artist and song.

    Customizable Inference: Choose the number of inference steps (1-100) to fine-tune the generated images.

    Extra Prompt: Enhance the generated images with an extra prompt, enabling specific styles (e.g., dark ambience, extremely detailed).

    Model Selection: Select a language model from Hugging Face's collection (e.g., dataautogpt3/OpenDalleV1.1).

    Skip Irrelevant Verses: Exclude empty or non-lyrical verses fetched from the Genius API.

    Output Path Configuration: Change the output path where the images will be saved.

<h2>Usage</h2>

Clone the repository

    git clone https://github.com/bil9148/L2I/


Install Dependencies:

    pip install -r requirements.txt

Run the Application:

    python main.py

Follow the on-screen instructions to enter the artist name, song name, and customize other options.

<h2>User Interface</h2>

All customization options are conveniently presented in the application's user interface. No need for manual configuration files. Simply interact with the prompts provided.

<h2>Contributing</h2>

If you'd like to contribute to Lyrics2Images, feel free to fork the repository, make your enhancements, and submit a pull request.

<h2>Issues</h2>

Encountered a bug or have a suggestion? Open an issue on the GitHub repository to help improve Lyrics2Images.

<h2>License</h2>

This project is licensed under the MIT License - see the LICENSE file for details.
