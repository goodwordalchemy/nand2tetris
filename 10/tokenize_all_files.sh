find . -name *.jack | xargs -I {} python -m jack_analyzer.jack_tokenizer {}
