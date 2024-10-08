# importing datetime module for now()
import datetime
    
# using now() to get current time
current_time = datetime.datetime.now()
    
# Printing attributes of now().
print ("The attributes of now() are : ")
    
print ("Year: ", end = "")
print (current_time.year)
    
print ("Month: ", end = "")
print (current_time.month)
    
print ("Day: ", end = "")
print (current_time.day)
