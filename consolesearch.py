import pickle
from transformers import AutoTokenizer, SiglipTextModel
from sentence_transformers import util

def load_indexed_data(filename):
    print("Loading indexed data...")
    with open(filename, 'rb') as indexed:
        return pickle.load(indexed)

def load_models():
    print("Loading Neural Networks...")
    model = SiglipTextModel.from_pretrained("google/siglip-base-patch16-224")
    tokenizer = AutoTokenizer.from_pretrained("google/siglip-base-patch16-224")
    return model, tokenizer

def cosine_to_confidence(cosine_similarity):
    """ Converts cosine similarity into a more user-friendly confidence score """
    if cosine_similarity > 0.075:
        return 100 * (cosine_similarity ** 0.1)
    else:
        return 100 * (cosine_similarity ** 0.1)

def image_search(saved_data, model, tokenizer):
    embedding_text = input("Enter search text: ")

    inputs = tokenizer(embedding_text, padding="max_length", return_tensors="pt")
    outputs = model(**inputs)
    pooled_output = outputs.pooler_output

    similarities = [
        {
            "filepath": img["filepath"],
            "cosine": util.pytorch_cos_sim(pooled_output, img["tensor"][0]).item()
        }
        for img in saved_data
    ]

    results = sorted(similarities, key=lambda x: x["cosine"], reverse=True)[:10]

    print("\nTop Ten Results:")
    for i, result in enumerate(results, 1):
        confidence_score = cosine_to_confidence(result["cosine"])
        print(f'{i}. {result["filepath"]} - {confidence_score:.2f}% confidence')

if __name__ == "__main__":
    print("Meme Search\n")
    saved_data = load_indexed_data("otherimages.imgidx")
    model, tokenizer = load_models()

    while True:
        image_search(saved_data, model, tokenizer)
        print("\n---\n")