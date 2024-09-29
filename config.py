import os

OUTPUT_FOLDER_PATH = "Output"

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BUCKET_NAME = 'hackaton-2024-sendphoto'

os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_KEY")
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'




AI_PROMPT = '''SEND ONLY JSON! Please analyze the provided contract text and extract the relevant data to fill the following JSON structure (if you doesn’t find data set null). Ensure to capture details for both companies, contract terms, services, bank details, notes, and invoice information. Structure the response in a stable, typed JSON format, following the schema provided. Creating the invoices take care about the dueDate which is the last date when the invoice can be payed. Inside Invoice if there is no a date specified in contract for createdAt then all data in invoices should consider that the createdAt is the current date. Note that the totalPrice in invoices should be the total for current service/product so it should be equal to: productQuantity * productPrice. If the contract can be payed in rates divide the invoices in these rates with apropriate description, price and dueDate(if there aren’t info about the dueDate of rates leave null). The field rates should contain the bool value if the contract can be paid in rates based on contract info(don’t confuse with subscription). The key stageNr should be the number of stage based on the contract info, also it should be not null in invoices only if the current contract offer the posibility to made the payment by stages(rates). Also if the contract can be payed in stages, and the invoices are for stage adjuste invoice description. Notes should be an Array of strings where are specified some notes regarding the agreement (like taxes for delaying the payment, and so one). Double check the data in invoices, because this data will be used to fulfill a real invoice.
{
   "companies":{
      "from":{
         "id":1,
         "name":"Service Provider Inc.",
         "entity_type":"Corporation",
         "email":"contact@serviceprovider.com",
         "phone":"+1234567890",
         "address":"123 Service St, Business City, BC",
         "IBAN": "RO49AAAA1B31007593840000",
         "bank_details":null 
      },
      "to":{
         "id":2,
         "name":"Client Corp.",
         "entity_type":"Corporation",
         "email":"info@clientcorp.com",
         "phone":"+0987654321",
         "address":"456 Client Ave, Client Town, CT",
         "IBAN":null,
         "bank_details":"Bank of Services, Account No: 123456789, Sort Code: 12-34-56"
      }
   },
   "contract":{
      "id":1,
      "from_company_id":1,
      "to_company_id":2,
      "currency":"USD",
      "language_code":"EN",
      "contract_date":"2024-09-29",
      "contract_start_date":"2024-10-01",
      "contract_due_date":"2025-10-01",
      "total":1500.00,
      "limited":false,
  "isSubscription":false,
  "rates":false,
   },
   "services":[
      {
         "id":1,
         "contract_id":1,
         "description":"Web Development Services",
         "quantity":1,
         "price":1500.00
      }
   ],
   "bank_details":{
      "company_id":1,
      "bank_details":"Bank of Services, Account No: 123456789, Sort Code: 12-34-56"
   },
   "notes":[
      {
         "id":1,
         "contract_id":1,
         "note":"Payment due within 30 days of invoice."
      }
   ],
   "invoices":[
      {
         "stageNr": null,
         "CreatedAt":"2024-09-29",
         "dueDate":"2025-10-01",
         "productDescription":"Web Development Services",
         "productQuantity":1,
         "productPrice":1500.00,
         "totalPrice":1500.00
      }
   ]
}'''