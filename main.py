from Insurance.logger import lg
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import os, sys

# def test_logger_and_exception():
#     try:
#         lg.info("Starting the test_logger_and_exception")
#         result= 3/0
#         print(result)
#         lg.info("Ending point of the test_logger_and_exception")
#     except Exception as e:
#         lg.debug(str(e))
#         raise InsuranceException(e, sys)
    
if __name__== "__main__":
    try:
        # start_training_pipeline
        # test_logger_and_exception()
        get_collection_as_dataframe(database_name= "INSURANCE", collection_name="INSURANCE_PROJECT")
        
    except Exception as e:
        print(e)