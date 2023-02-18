from app.depositphotos import body_runner_depositphotos
from app.shutterstock import body_runner_shutterstock
from app.utils.runner import root_run


@root_run
def run(excel_data_dir: str, offset: int, rubric: str, photos_dir: str, excel_file_name: str) -> None:
    body_runner_depositphotos(excel_data_dir + "_depositphotos", offset, rubric, photos_dir, excel_file_name)
    body_runner_shutterstock(excel_data_dir + "_shutterstock", offset, rubric, photos_dir, excel_file_name)
