from account.models import Account
from account.exceptions import AccountNotFoundException 

def get_object(account_id): 
		try:
			account=Account.objects.get(pk=account_id)			
		except Account.DoesNotExist:
			raise AccountNotFoundException
		return account 