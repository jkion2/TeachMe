import base64
import glob
import os
import random
import subprocess
import time

SCRIPT_DIR = "./manim/scripts/"
VIDEO_DIR = "./manim/videos/"
MEDIA_DUMP_DIR = "./manim/media/"

os.makedirs(SCRIPT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(MEDIA_DUMP_DIR, exist_ok=True)


def random_chars() -> str:
    random.seed(time.time())
    chars: str = ""
    for _ in range(10):
        chars += chr(random.randint(97, 122))
    return chars


def parse_text_to_code(text: str) -> str:
    # Check formatting
    if not text.startswith("```"):
        raise ValueError("Code block must start with '```'")

    # Remove code braces
    lines = text.split("\n")
    lines = lines[1:-1]
    code = "\n".join(lines)

    return code


def write_code_to_file(code: str) -> str:
    """
    Writes a given code block to a file in the scripts directory.

    The filename will be a random 10 character string followed by '.py'.
    The file will be written in the scripts directory.

    Args:
        code: str - The code block to write to the file.

    Returns:
        str - The name of the file written to.
    """
    file_name: str = f"{random_chars()}.py"
    file_path: str = f"{SCRIPT_DIR}{file_name}"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(code)

    return file_name


def compile_code_to_video(file_name: str) -> None:
    file_path: str = f"{SCRIPT_DIR}{file_name}"
    video_path: str = f"{VIDEO_DIR}{file_name[:-3]}.mp4"

    commands: list[str] = [
        "manim",
        "-pql",
        "--fps",
        "10",
        "--media_dir",
        MEDIA_DUMP_DIR,
        file_path,
        "SolutionAnimation",
        "-o",
        video_path,
    ]

    result = subprocess.run(args=commands, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(result.stderr)

    print(f"{file_name} compiled successfully at {video_path}")


def fetch_video(file_name: str) -> str:
    """
    Fetch a video from the video directory and return it as a base64 encoded string.

    Args:
        file_name (str): The name of the video file to fetch.

    Returns:
        str: The base64 encoded video data.
    """
    video_path: str = f"{VIDEO_DIR}{file_name[:-3]}.mp4"

    with open(video_path, "rb") as file:
        video_data = file.read()

    return base64.b64encode(video_data).decode("utf-8")


def fetch_latest_code_file() -> str:
    pattern = os.path.join(SCRIPT_DIR, "*.py")
    files = glob.glob(pattern)

    if not files:
        raise FileNotFoundError("No code files found")

    latest_file = max(files, key=os.path.getmtime)
    return str(latest_file)


def fetech_latest_video_file() -> str:
    pattern = os.path.join(VIDEO_DIR, "*.mp4")
    files = glob.glob(pattern)

    if not files:
        raise FileNotFoundError("No video files found")

    latest_file = max(files, key=os.path.getmtime)
    return str(latest_file)


def fetch_desired_video() -> str:
    """
    Fetches the latest video file from the video directory and returns it as a base64 encoded string.
    The video file is determined by comparing the latest code file and video file in the respective directories.
    If the code and video files do not match, a ValueError is raised.
    """
    latest_code_file = fetch_latest_code_file()
    latest_video_file = fetech_latest_video_file()

    c_name: str = latest_code_file.split("/")[-1]
    v_name: str = latest_video_file.split("/")[-1]

    if not (c_name[:-3] == v_name[:-4]):
        raise ValueError("Code and video files do not match")

    with open(latest_video_file, "rb") as file:
        video_data = file.read()

    return base64.b64encode(video_data).decode("utf-8")
