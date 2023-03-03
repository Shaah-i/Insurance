"""
# batch prediction
# training pipeline
"""

from Insurance.pipeline.batch_prediction import start_batch_prediction
from Insurance.pipeline.training_pipeline import start_training_pipeline

# file_path = "G:\ML Study\DS practice\Insurance_premium\Insurance\insurance.csv"

if __name__ == "__main__":
    try:
        # output = start_batch_prediction(input_file_path= file_path)
        output_file = start_training_pipeline()
        print(output_file)
    except Exception as e:
        print(e)
