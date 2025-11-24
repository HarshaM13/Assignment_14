from src.extract import extract_data
from src.transform import transform_data
from src.model import pred_model
#from src.load import load_data

def main():
    df_covid = extract_data()
    processed_df = transform_data(df_covid)
    predicted_df = pred_model(processed_df)
    #load_data()  # publishes processed dataset
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
