from app import root_run, body_runner_depositphotos


if __name__ == "__main__":
    @root_run
    def run(excel_data_dir: str, offset: int, rubric: str, photos_dir: str, excel_file_name: str) -> None:
        body_runner_depositphotos(excel_data_dir, offset, rubric, photos_dir, excel_file_name)
