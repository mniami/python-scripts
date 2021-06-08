import click
from moviepy.editor import *
from natsort import natsorted


@click.command()
@click.argument("path")
@click.argument("output-file-name")
def combine_movies(path: str, output_file_path: str):
    video_clips = []

    for root, dirs, files in os.walk(path):
        files = natsorted(files)
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.mp4', '.mov']:
                file_path = os.path.join(root, file)
                video = VideoFileClip(file_path)
                video_clips.append(video)

    final_clip = concatenate_videoclips(video_clips)
    final_clip.to_videofile(output_file_path, fps=video_clips[0].fps, remove_temp=True)


if __name__ == '__main__':
    combine_movies()
