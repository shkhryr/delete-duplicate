import os
from PIL import Image
from multiprocessing import Pool


# Function to resize and lower quality of an individual image
def process_image(input_path, output_path, scale=0.2, quality=30):
    try:
        image = Image.open(input_path)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        resized_image.save(output_path, optimize=True, quality=quality)
        image.close()
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")


if __name__ == "__main__":
    # Path to the input folder
    input_folder = "input"

    # Path to the output folder
    output_folder = "output"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of image files in the input folder
    image_files = os.listdir(input_folder)

    # Create a Pool of worker processes
    num_processes = os.cpu_count()  # You can adjust the number of processes
    with Pool(processes=num_processes) as pool:
        for file_name in image_files:
            print(f"Processing {file_name}")
            input_image_path = os.path.join(input_folder, file_name)
            output_image_path = os.path.join(output_folder, file_name)
            pool.apply_async(process_image, (input_image_path, output_image_path))

        # Close the pool and wait for all processes to complete
        pool.close()
        pool.join()

    print("All images have been successfully processed.")
