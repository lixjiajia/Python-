#Jiajia Li

import requests
import doctest
def dict_to_query(input_dict):
    '''(dict) -> str
    Returns a string containing the keys and values of the dictionary with the format
    'key=value', and ampersands ('&') separating each.
    
    >>> dict_to_query({'email': 'jonathan.campbell@mcgill.ca', 'token': 'ABC'})
    'email=jonathan.campbell@mcgill.ca&token=ABC'
    >>> dict_to_query({1: 'papaya', 2: 'ABC'})
    '1=papaya&2=ABC'
    >>> dict_to_query({'email': 'jia.j.li@mcgill.ca', 'token': 'tony'})
    'email=jia.j.li@mcgill.ca&token=tony'
    '''
    new_str=''
    for key, value in input_dict.items():
        new_str+=str(key) + '=' + str(value)
        new_str+='&'
    new_str=new_str[:-1]
    return new_str
        
class Account:
    ''' A class that represents an account
    Attributes: email, token, balance, request_log
    '''
    API_URL = 'https://coinsbot202.herokuapp.com/api/'
    def __init__(self, email, token):
        '''
        (str, str)-> Nonetype
        Creates an object of type Account. Raise an AssertionError if the types of the
        inputs are incorrect or if the email does not end in 'mcgill.ca'. 
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.balance
        -1
        
        >>> inv_acc = Account("jonathan.campbell@yahoo.ca", "ABC")
        Traceback (most recent call last):
        AssertionError: jonathan.campbell@yahoo.ca does not end in "mcgill.ca"
        
        >>> str_acc = Account(55, "ABC")
        Traceback (most recent call last):
        AssertionError: Email or token is not in string format

        '''
        
        self.email = email
        self.token = token
        self.balance = -1
        self.request_log = []
        
        if type(email)!=str or type(token)!=str:
            raise AssertionError('Email or token is not in string format')

        elif email[-9:]!='mcgill.ca':
            raise AssertionError(email + ' does not end in "mcgill.ca"')        
        
        
    def __str__(self):
        '''() -> str
        Returns a string of the format 'EMAIL has balance BALANCE' where EMAIL and
        BALANCE refer to the appropriate instance attributes.
        
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> print(my_acct)
        jonathan.campbell@mcgill.ca has balance -1
        
        >>> acc = Account("jia.j.li@mcgill.ca", 'CsKhzt6y7LbEa9c0')
        >>> print(acc)
        jia.j.li@mcgill.ca has balance -1
        
        >>> acc2 = Account("jia.j.li@yahoo.ca", 'CsKhzt6y7LbEa9c0')
        Traceback (most recent call last):
        AssertionError: jia.j.li@yahoo.ca does not end in "mcgill.ca"
        
        '''
        return self.email + ' has balance ' + str(self.balance)
    
    def call_api(self, endpoint, request_dict):
        ''' (str, dict) -> dict
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        Traceback (most recent call last):
        AssertionError: The token in the API request did not match the token that was sent over Slack.
        
        >>> new_acct= Account('jia.j.li@mail.mcgill.ca', 'CsKhzt6y7LbEa9c0')
        >>> new_acct.call_api('balance', {'email': new_acct.email})
        {'message': 4111, 'status': 'OK'}
        
        >>> acc= Account('jia.j.li@mail.mcgill.ca', '43')
        >>> acc.call_api('balance', {'email': acc.email})
        Traceback (most recent call last):
        AssertionError: The token in the API request did not match the token that was sent over Slack.

        '''
        if type(endpoint)!=str:
            raise AssertionError('Type of endpoint input is not str')
        elif type(request_dict)!=dict:
            raise AssertionError('Type of request dictionary input is not dict')
        else:
            request_dict['token']=self.token
            request_url = Account.API_URL + endpoint+ '?' + dict_to_query(request_dict)
            result = requests.get(url=request_url).json()
            if result['status']!='OK':
                raise AssertionError(result['message'])
            else:
                return result
            
    def retrieve_balance(self):
        '''
        () -> int
        Calls the API to retrieve the balance for the current user email.
        Updates the balance attribute of the current user to
        the given value (after converting to integer), and returns the integer.
        
        >>> my_acct = Account("jonathan.campbell@mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        Traceback (most recent call last):
        AssertionError: The token in the API request did not match the token that was sent over Slack.
        
        >>> new_acct = Account('jia.j.li@mail.mcgill.ca', 'CsKhzt6y7LbEa9c0')
        >>> new_acct.retrieve_balance()
        4111
        >>> print(new_acct)
        jia.j.li@mail.mcgill.ca has balance 2886
        
        >>> new_acct = Account('jia.j.li@mail.mcgill.ca', 'b1')
        >>> new_acct.retrieve_balance()
        Traceback (most recent call last):
        AssertionError: The token in the API request did not match the token that was sent over Slack.
        
        '''
        balance_dict=self.call_api('balance', {'email': self.email})
        self.balance= balance_dict['message']
        return self.balance
        
    def transfer(self, coin_amt, email):
        ''' (int, str) -> int
        Calls the API to transfer the given amount to coins from the current
        user to the specified user. Returns the value for the key 'message' in the result dictionary.
        >>> my_acct = Account('jia.j.li@mail.mcgill.ca', 'CsKhzt6y7LbEa9c0')
        >>> my_acct.retrieve_balance()
        4111
        >>> my_acct.transfer(25, "alexa.infelise@mail.mcgill.ca")
        'You have transferred 25 coins of your balance of 4111 coins to alexa.infelise@mail.mcgill.ca. Your balance is now 2861.'
        
        >>> acc = Account('mock@mcgill.ca', 'ABC')
        >>> acc.retrieve_balance()
        250
        >>> acc.transfer(300, "alexa.infelise@mail.mcgill.ca")
        Traceback (most recent call last):
        AssertionError: Not enough in current user's balance.
        
        >>> acct = Account('jia.j.li@mail.mcgill.ca', 'CsKhzt6y7LbEa9c0')
        >>> acct.transfer(25, "alexa.infelise@gmail.ca")
        Traceback (most recent call last):
        AssertionError: deposit email is invalid.
        '''
        
        
        if type(coin_amt)!=int:
            raise AssertionError('Coin amount must be an integer.')
        elif coin_amt < 25:
            raise AssertionError('coin amount must be at least 25.')
        elif coin_amt > self.retrieve_balance():
            raise AssertionError('Not enough in current user\'s balance.')
        elif email == self.email:
            raise AssertionError('transfer email must be different from the current user\'s.')
        elif self.retrieve_balance == -1:
            raise AssertionError('Balance is -1.')
        elif type(email)!=str or email[-9:]!='mcgill.ca':
            raise AssertionError('deposit email is invalid.')
        else:
            transfer_dict = self.call_api('transfer', {'withdrawal_email': self.email, 'deposit_email': email, 'amount': coin_amt})
            return transfer_dict['message']


