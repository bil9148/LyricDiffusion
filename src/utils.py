from typing import List
import shutil
from huggingface_hub import notebook_login, HfApi, ModelFilter


class HuggingFace:

    @staticmethod
    def get_all_model_names(sort="downloads", limit=10, direction=-1) -> List:
        api = HfApi()
        models = api.list_models(
            filter=ModelFilter(
                task="text-to-image",
            ), sort=sort, limit=limit, direction=direction
        )
        models = list(models)

        modelNames = []

        for model in models:
            modelNames.append(model.id)

        return modelNames

    @staticmethod
    def auth_hugging_face():
        notebook_login()


def parse_lyrics(path: str, prompt: str) -> List[str]:
    """
    Parses the lyrics plain file into a list of verses

    Args:
        path: The lyrics path
        prompt: Extra params

    Returns:
        A list of verses
    """
    with open(path) as f:
        verses = f.readlines()

    verses_clean = []
    for verse in verses:
        verse = verse.replace("\n", "")
        verse = verse.replace(".", "")
        if verse:
            verse += f" {prompt}"
            verses_clean.append(verse)
    return verses_clean


def zip_folder(folder_path: str, zip_path: str):
    shutil.make_archive(zip_path, 'zip', folder_path)
