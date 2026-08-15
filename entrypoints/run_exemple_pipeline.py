import os
import sys

# Adiciona o diretório raiz ao sys.path para garantir as importações do pacote
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from include.pipelines.exemple_pipeline import ExemplePipeline

if __name__ == "__main__":
    extractor = ExemplePipeline()
    extractor.execute()
