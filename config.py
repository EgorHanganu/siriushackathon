import os

OUTPUT_FOLDER_PATH = "Output"

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BUCKET_NAME = 'hackaton-2024-sendphoto'

os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_KEY")
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'






AI_PROMPT = '''\n\nSTRONGLY SEND ONLY JSON WITHOUT ANY CAPTIONS! Put information from the text above to the values in provided json. If information missing, put null. Note that this data will be used to create a invoice or bill. The data i gave you is an contract or an official document where are specified the condition of these papers (which i need to store and manage). Be careful that there can be contracts which have temporary or subscription billing, in such case their service can be paid depending on the date when the contract come to effect and is closed (take care of the payment terms and conditions)

{
  "currency": string,  
  "languageCode": string, 
   "contractDate": string, // Date when the contract was elaborated (can be null)   dd-mm-yyyy

  "contractStartDate": string,   // Date when contract comes into effect dd-mm-yyyy
  "contractDueDate": string,   // Date when contract come to it's end dd-mm-yyyy
  "fromLegalEntityName": string, # Without entity type 
"fromLegalEntityType": string, 
  "fromEmail": string,
  "toEntityName": string, 
  "toEntityType": string, 
  "toEmail": string,
  "toPhone": string,
  "toAddress": string,
  "services": [{
"serviceDescription": string,
"quantity": number,
"duration": number, // If the contract is temporary 
"serviceDuration": ["day", "week", "month", "year"], // If the contract is temporary  should be chosen one of the following entities appropriate to current contract. not array

 "proportion": [ "week", "month", "year"], // This parameter should aware me if the contract could be paid on a pro rata temporis basis, and point the minimal amount of entites (for example if the service should be payed monthly, but in contract is such posibility to pay daily, then in this field should be indicated days)
      "price": number // Price per 1 piece of quantity per 1 duration unit
  
}], 
  "Notes": [string], //Array of strings where are specified some notes regarding the agreement (like taxes for delaying the payment, and so one)
  "bankDetailsSeller": string, 
  "bankDetailsBuyer": string,
  "companyPromoInfoPhone": string,
  "companyPromoInfoEmail": string,
  "companyPromoInfoWebPage": string,
  "tax": number,
  "discount": number,
  "total": number,  // The amount of money which should be payed for the entire contract (if the contract don't have limit, this field should be empty)
  "isExpense": bool,
  "limited": boolean, // The value which will show if the contract has a specific term
 

}'''