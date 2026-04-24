#--------------------Columns Standardization--------------------
#Proper Case Standardization of the column names in the credit dataset
credit.columns = credit.columns.str.strip().str.lower().str.replace(' ', '_')
#Quality check after standardization
credit.columns

#Proper Case Standardization of the column names in the customer income dataset
customer_income.columns = customer_income.columns.str.strip().str.lower().str.replace(' ', '_')
#Quality check after standardization
customer_income.columns

#Proper Case Standardization of the column names in the customer gender dataset
customer_gender.columns = customer_gender.columns.str.strip().str.lower().str.replace(' ', '_')
#Quality check after standardization        
customer_gender.columns

#Proper Case Standardization of the column names in the customer dob dataset
customer_dob.columns = customer_dob.columns.str.strip().str.lower().str.replace(' ','_')
#Quality check after standardization
customer_dob.columns

#--------------------Customer Data gender dataset cleaning--------------------
#Check unique values in the gender column and standardize them if necessary
customer_gender['gender'].unique()
#Ensure gender is standardized to Male,Female or Other
customer_genderd=customer_gender.astype({'gender':'string'})
customer_gender['gender'].fillna('Other',inplace=True)
customer_gender['gender'].unique()
customer_gender['gender'] = customer_gender['gender'].replace   ({'M':'Male','F':'Female','Unspecified':'Other'})

#Formating of the citizenship column in the customer income dataset
customer_gender['citizenship'].unique()
customer_gender=customer_gender.astype({'citizenship':'string'})
customer_gender['citizenship'] = customer_gender['citizenship'].str.strip().str.capitalize()
customer_gender['citizenship'].fillna('Other',inplace=True)
customer_gender['citizenship'] = customer_gender['citizenship'].replace({'Citizen':'Kenyan',})

#Quality check after standardization
customer_gender['gender'].unique()
customer_gender['citizenship'].unique()


#--------------------Customer Data DOB dataset cleaning--------------------
#Check for age and group by age group
customer_dob['provider'].unique()
customer_dob['provider'].fillna('Other',inplace=True)
customer_dob['provider']=customer_dob['provider'].str.strip().str.capitalize()

#Quality check after standardization
customer_dob['provider'].unique()



#Drop Columns that are not needed for the analysis in the credit dataset
credit.drop(columns=['snapshot_date'],inplace=True)
credit.drop(columns=['unnamed:_28'],inplace=True)
#Quality check after dropping the columns
credit.columns  
