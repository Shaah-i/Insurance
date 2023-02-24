from Insurance.logger import lg
from Insurance.exception import InsuranceException
import os, sys

def test_logger_and_exception():
    try:
        lg.info("Starting the test_logger_and_exception")
        result= 3/0
        print(result)
        lg.info("Ending point of the test_logger_and_exception")
    except Exception as e:
        lg.debug(str(e))
        raise InsuranceException(e, sys)
    
if __name__== "__main__":
    try:
        test_logger_and_exception()
    except Exception as e:
        print(e)