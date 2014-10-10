Our crc cards can be viewed here:

http://imgur.com/3rxIFLy

## Scenarios:
					
As Max, I want to post a message to a specific board so that I can participate in discussions.					
					
* Max writes a message in a specific topic's input box and clicks 'post'					
* The DAO creates a message with metadata and an associated board					
* DAO displays message grouped with messages from the same board					
					
As Max, I want to be able to register so that I can create and login into an account.			
					
* Max inputs a username and password.					
* AuthDAO adds an AuthenticatedUser entry.					
* Max logs in with username and password					
* AuthDAO checks input with AuthenticatedUser mapping (username = primary key)					
					
As Max, I want to join groups, such as courses or teams, so that I can participate in specific discussions.					
* Max creates a group
* DAO stores the group privately
* Max can then invite users to come into the group exclusively
* Max can create boards where only a certain group can chat on
					
As Max, I want to filter and sort topics based on subscription so that I can view relevant topics at a glance.					
* User clicks a 'filter' or 'sort' button					
* DAO checks user's subscriptions, and displays all boards that have been subscribed to		
