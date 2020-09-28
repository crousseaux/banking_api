Banking API
=======

## Installation Instructions

1. Clone the project.
    ```shell
    $ https://github.com/crousseaux/banking_api.git
    ```
1. `cd` into the project directory
    ```shell
    $ cd banking_api
    ```
1. Create a new virtual environment using Python 3.7 and activate it.
    ```shell
    $ python3 -m venv env
    $ source env/bin/activate
    ```
1. Install dependencies from requirements.txt:
    ```shell
    (env)$ pip install -r requirements.txt
    ```
1. Migrate the database.
    ```shell
    (env)$ python manage.py migrate
    ```
1. *(Optional)* Populate the database with a handful of companies, users, wallets and cards 

    ```shell
    (env)$ python manage.py populate_db
    ```
1. Run the local server via:
    ```shell
    (env)$ python manage.py runserver
    ```

### Done!
The browsable api will be available at <a href="http://localhost:8000/wallets" target="_blank">http://localhost:8000/wallets</a>

## Live Demo
[Test Environment]()

## Usage
#### ```[GET] /wallets``` 
Description:  View all wallets  
**HTTP headers:** none  

#### ```[GET] /wallets/<wallet_id>```
Description: View a specific wallets  
**HTTP headers:** none  

#### ```[POST] /wallets``` 
Description:  Create new wallet  
**HTTP headers:** specify User-Id and Company-Id (positive integers)  
**Body:**  
currency: currency of the wallet. It has to be the id of the currency record  
company_id: which company this wallet will be connected to  
balance (optional, default 100): how much should be on the wallet when it gets instantiated  
example:  
``` { "currency_id": 2, "company_id": 2, "balance": 1000 } ```

#### ```[GET] /cards``` 
Description: View all cards   
**HTTP headers:** none  

#### ```[GET] /cards/<card_id>``` 
Description: View a specific card  
**HTTP headers:** none

#### ```[POST] /cards``` 
Description:  Create new card  
**HTTP headers:** specify User-Id and Company-Id (positive integers)  
**Body:**  
wallet_id: wallet connected to the card, id of the record  
currency_id: currency of the card, if of the record  
balance (optional, default 20): how much should be on the card when it gets instantiated  
example:  
``` { "wallet_id": 5, "currency_id": 1, "user_id": 1 } ```

#### ```[GET] /transfers```
Description: View all transfers  
**HTTP headers:** none  

#### ```[GET] /transfers/<transfer_id>```
Description: View a specific transfer  
**HTTP headers:** none  

#### ```[POST] /transfers``` 
Description:  Create new card  
**HTTP headers:** specify User-Id and Company-Id (positive integers)  
**Body:**  
amount: positive decimal to transfer  
origin_entity_id: entity id to transfer from (entities id can be found in list of wallets or cards)  
target_entity_id: entity id to transfer to (entities id can be found in list of wallets or cards)  
example:  
``` { "amount": 10, "origin_entity_id": 1, "target_entity_id": 10, "user_id": 1 } ```

#### ```[GET] /users/<user_id>```
Description: View a specific user details  
**HTTP headers:** none  

#### ```[GET] /users/<user_id>/cards```
Description: View all cards of a specific user  
**HTTP headers:** none  

#### ```[GET] /users/<user_id>/wallets```
Description: View all wallets of a specific user  
**HTTP headers:** none  

#### ```[POST] /cards/<card_id>/block```
Description: block a card 
**HTTP headers:** specify User-Id and Company-Id (positive integers)    
**Body:**: empty  

#### ```[POST] /cards/<card_id>/unblock```
Description: unblock a card 
**HTTP headers:** specify User-Id and Company-Id (positive integers)    
**Body:**: empty  