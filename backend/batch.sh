python get_images.py
python process_images.py "data/images/*.jpg"
python assemble_vectors.py
python check_clarifai.py
python create_base_json.py
python create_data_json.py
cp -rp data/data.json ../
cp -rp data/features.npy ../
