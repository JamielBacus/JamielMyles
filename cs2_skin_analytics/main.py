# main.py
from src.scraper import run_scraper
from src.data_cleaning import clean_raw_data
from src.models import train_regression_model, train_classifier_model

def main():
    print("[1/3] Initializing pipeline extraction layout scripts...")
    raw_data = run_scraper()
    
    print("[2/3] Executing structural cleanup, reshaping, and target generation...")
    X, y_reg, y_clf = clean_raw_data(raw_data)
    
    print("[3/3] Training pipelines and compiling diagnostic loss matrices...")
    train_regression_model(X, y_reg)
    train_classifier_model(X, y_clf)
    
    print("\nPipeline analytics processed flawlessly.")

if __name__ == "__main__":
    main()
