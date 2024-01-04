Lyrics2Images

Lyrics2Images is a versatile application that transforms song lyrics into visually stunning images. By leveraging the Genius API, it seamlessly retrieves lyrics based on the artist and song entered by the user. The application provides a user-friendly interface with various customization options, allowing you to generate images tailored to your preferences.
Features

    Genius API Integration: Automatically fetches lyrics for the specified artist and song.

    Customizable Inference: Choose the number of inference steps (1-100) to fine-tune the generated images.

    Extra Prompt: Enhance the generated images with an extra prompt, enabling specific styles (e.g., dark ambience, extremely detailed).

    Model Selection: Select a language model from Hugging Face's collection (e.g., dataautogpt3/OpenDalleV1.1).

    Skip Irrelevant Verses: Exclude empty or non-lyrical verses fetched from the Genius API.

    Output Path Configuration: Change the output path where the images will be saved.

Usage

    Clone the Repository:

    bash

git clone https://github.com/your-username/Lyrics2Images.git
cd Lyrics2Images

Install Dependencies:

bash

pip install -r requirements.txt

Run the Application:

bash

    python main.py

    Follow the on-screen instructions to enter the artist name, song name, and customize other options.

User Interface

All customization options are conveniently presented in the application's user interface. No need for manual configuration files. Simply interact with the prompts provided.
Contributing

If you'd like to contribute to Lyrics2Images, feel free to fork the repository, make your enhancements, and submit a pull request.
Issues

Encountered a bug or have a suggestion? Open an issue on the GitHub repository to help improve Lyrics2Images.
License

This project is licensed under the MIT License - see the LICENSE file for details.
