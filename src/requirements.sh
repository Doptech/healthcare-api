!pip install https://huggingface.co/Vrushali/en_disease_pipeline/resolve/main/en_disease_pipeline-any-py3-none-any.whl
pip install git+https://github.com/openai/whisper.git --no-deps
python -m spacy download en_core_web_sm
pip install "layoutparser[ocr]"
sudo apt install tesseract-ocr