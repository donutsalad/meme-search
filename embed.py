import pickle
import glob
from PIL import Image
from transformers import AutoProcessor, SiglipVisionModel
import os

filename = "./memes.imgidx"

def calculate_tensors(files, existing_files):
    model = SiglipVisionModel.from_pretrained("google/siglip-base-patch16-224")
    processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

    stack = []
    for img in files:
        if img not in existing_files:
            try:
                with Image.open(img) as image:
                    inputs = processor(images=image, return_tensors="pt")
                    outputs = model(**inputs)
                    pooled_output = outputs.pooler_output

                    stack.append({"filepath": img, "tensor": pooled_output})
                    print(f"Done with {img}")
            except Exception as e:
                print(f"Problem with file: {img}. Skipping. Error: {e}")
        else:
            print(f"Already processed {img}. Skipping.")
        
    return stack

def main():
    supported_formats = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.tiff", "*.ico", "*.webp"]
    full_names = []
    for fmt in supported_formats:
        full_names.extend(glob.glob(os.path.join("/home/isabelle/memes/", fmt)))
    
    # Load existing data if exists
    existing_data = []
    existing_files = []
    if os.path.exists(filename):
        with open(filename, 'rb') as infile:
            existing_data = pickle.load(infile)
            existing_files = [entry["filepath"] for entry in existing_data]
    
    # Calculate new tensors
    new_data = calculate_tensors(full_names, existing_files)
    
    # Combine old and new data
    combined_data = existing_data + new_data
    
    # Save combined data
    with open(filename, 'wb') as outfile:
        pickle.dump(combined_data, outfile)
    
    # Delete chunked files
    chunk_files = glob.glob(f"{filename}.*")
    for file in chunk_files:
        os.remove(file)
    
    print("Done!")

if __name__ == "__main__":
    main()