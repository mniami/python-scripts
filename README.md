# python-scripts
Contains few useful scripts for image, video and pdf files processing

# Find duplicated images
find_duplicates - finds duplicated images, allows to remove them

## Listing duplicated images into html webpage
```
python3 find_duplicates/main.py [path_to_images] --output-path [output_directory_path]
```

## Moving duplicates into another folder
```
python3 find_duplicates/main.py [path_to_images] --output-path [output_directory_path] --move
```

# Color conversion
Converts image color pallet to another format
```
python3 color_conversion.py [path_to_image] [color_format]
```

# Combine videos
Concatenate multiple videos into one
```
python3 combine_videos.py [path_to_videos] [new_video_file_path]
```
# Fill pdf form
Fill pdf form using data from json file + removes watermark from the source pdf file

# Reduce image size
Reduces image size from path