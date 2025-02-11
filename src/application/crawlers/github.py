import os
import shutil
import subprocess
import tempfile

from loguru import logger

from src.domain.documents import RepositoryDocument

from .base import BaseCrawler


class GithubCrawler(BaseCrawler):
    """Crawler for extracting content from GitHub repositories."""
    model = RepositoryDocument

    def __init__(self, ignore=(".git", ".toml", ".lock", ".png")) -> None:
        """Initializes the GitHub crawler.

        Args:
            ignore (tuple, optional): File and directory patterns to ignore. Defaults to (".git", ".toml", ".lock", ".png").
        """
        super().__init__()
        self._ignore = ignore

    def extract(self, link: str, **kwargs) -> None:
        """Extracts content from a GitHub repository and stores it in the database.

        Args:
            link (str): The URL of the GitHub repository.
            **kwargs: Additional keyword arguments, including the user object with `id` and `full_name` attributes.
        
        Raises:
            Exception: If an error occurs during extraction.
        """
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Repositroy already exists in database: {link}")

            return
        
        logger.info(f"Starting scrapping github repositroy: {link}")

        repo_name = link.rstrip("/").split("/")[-1]

        local_temp = tempfile.mkdtemp()
        original_cwd = os.getcwd()  # Store the current working directory

        try:
            os.chdir(local_temp)
            subprocess.run(["git", "clone", link], check=True)

            repo_path = os.path.join(local_temp, repo_name) # noqa: PTH118

            tree = {}
            for root, _, files in os.walk(repo_path):
                dir = root.replace(repo_path, "").lstrip("/")
                if dir.startswith(self._ignore):
                    continue
                for file in files:
                    if file.endswith(self._ignore):
                        continue
                    file_path = os.path.join(dir, file)  # noqa: PTH118
                    with open(os.path.join(root, file), "r", errors="ignore") as f:    # noqa: PTH123, PTH118
                        tree[file_path] = f.read().replace(" ","")

            user = kwargs["user"]
            instance = self.model(
                content=tree,
                name=repo_name,
                link=link,
                platform="github",
                author_id=user.id,
                author_full_name=user.full_name,
            )
            instance.save()
        except Exception:
            raise
        finally:
            os.chdir(original_cwd)  # Change back to original directory
            shutil.rmtree(local_temp)

        logger.info(f"Finished scrapping GitHub repository: {link}")




