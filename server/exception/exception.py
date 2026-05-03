# Sys module helps us make changes in the python runtime enviroment and helps us get all the error details occured in the project
import sys
from server.logging.logger import logging
# Creating a resuable function that fetches error details from the sys module and prints a custom error message 
def error_message_details(error,error_detail:sys):
    # exc tb will contain all details regarding exception like type , file name , line number etc
   _,_,exc_tb = error_detail.exc_info()
#    Getting filename from sys.errordetail
   file_name = exc_tb.tb_frame.f_code.co_filename
   
   error_message = 'Error occured in python script name [{0}] , line number [{1}] , error message[{2}]'.format(file_name,exc_tb.tb_lineno,str(error))
   
   return error_message

# Creating custom error class 
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail=error_detail)
        
    def __str__(self):
        return self.error_message
    
if __name__=='__main__':
    try:
        a = 4/0 
        print(a)
    except Exception as e:
        logging.info(CustomException(e,sys))
        raise CustomException(e,sys)
    