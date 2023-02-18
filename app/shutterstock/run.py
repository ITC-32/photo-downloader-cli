from app import root_run
from app.shutterstock import body_runner_shutterstock


if __name__ == "__main__":
    @root_run
    def run(excel_data_dir: str, offset: int, rubric: str, photos_dir: str, excel_file_name: str) -> None:
        body_runner_shutterstock(excel_data_dir, offset, rubric, photos_dir, excel_file_name)
