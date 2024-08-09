import pickle
import glob
from PIL import Image
from transformers import AutoProcessor, SiglipVisionModel
import os
import gc  # import garbage collector

chunk_folder = "./chunked_memes/"
output_filename = "./complete_memes.imgidx"
search_string = "/home/isabelle/memes"
os.makedirs(chunk_folder, exist_ok=True)

def calculate_tensors(files, model, processor):
    stack = []
    for img in files:
        try:
            with Image.open(img) as image:
                inputs = processor(images=image, return_tensors="pt")
                outputs = model(**inputs)
                pooled_output = outputs.pooler_output

                stack.append({"filepath": img, "tensor": pooled_output})
                print(f"Done with {img}")
        except Exception as e:
            print(f"Problem with file: {img}. Skipping. Error: {e}")
        
    return stack

def process_images():
    supported_formats = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.tiff", "*.ico", "*.webp"]
    full_names = []
    for fmt in supported_formats:
        full_names.extend(glob.glob(os.path.join(search_string, fmt)))
    
    step_size = 25
    model = SiglipVisionModel.from_pretrained("google/siglip-base-patch16-224")
    processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

    num_chunks = (len(full_names) + step_size - 1) // step_size  # Calculate number of chunks
    for index in range(num_chunks):
        print(f"Processing Chunk {index + 1}\n")

        start_idx = index * step_size
        end_idx = min((index + 1) * step_size, len(full_names))
        chunk_files = full_names[start_idx:end_idx]
        calculated = calculate_tensors(chunk_files, model, processor)

        print(f"Writing to file chunk {index + 1}")
        with open(f"{chunk_folder}memes.imgidx.{index + 1}", 'wb') as fileout:
            pickle.dump(calculated, fileout)

        # Clear memory of individual chunks after saving them
        del calculated
        gc.collect()  # force garbage collection after each chunk

        print(f"Done with chunk {index + 1}/{num_chunks}!")

    print("Processing Done!")

def consolidate_chunks():
    searches = []
    chunk_files = glob.glob(os.path.join(chunk_folder, "memes.imgidx.*"))

    for chunk_file in chunk_files:
        with open(chunk_file, "rb") as infile:
            images = pickle.load(infile)
            searches.extend(images)

    with open(output_filename, "wb") as outfile:
        pickle.dump(searches, outfile)

    print("Consolidation Done!")

if __name__ == "__main__":
    process_images()
    consolidate_chunks()