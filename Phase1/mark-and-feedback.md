# Feedback

* For the forum to be used interactively among instructors, I think you should not limit hiding topics among students only.
* Since group membership is used to make discussions private to a certain group, your user story should include how Max can assign other group members to the group. If a user can freely join a group, then groups cannot be used for making discussion private.
* Instead of granting TA status, which seems like another feature, I think this can be handled by creating a group that only TAs are invited to join. So, maybe the topic creator can grant some privileges to certain group members.
* Actually, your groups sounds a lot similar to Role-Based Access Control. It is used by many popular web applications such as Drupal, OpenStack, etc. It would be a good idea to look at how they implements role-based access control to get idead during implementation stage. Basically, instead of assigning users to groups, it assigns roles to users, and roles represents privileges a user can do.
* MVP description seems very thorough and allowing users to define groups separate from administration of university seems like a very good idea for broader usage scenarios. However, you should handle how an instructor can correctly determine message owner identity if the forum is to be used for class envrionments.
* DAO is actually missing from CRC cards you have shown, even though you mention it.
* How is topic different from board? (I am just confused because it is not described clearly above)
* Many of the scenarios you have played out seems incomplete. For example for 2nd scenario, it is about registering for a user account. But you are comparing if user provided username equals primary key of a AuthenticatedUser data in AuthenticationDAO. It sounds like you are checking if duplicate username already exists in DAO but I do not think it completely describes registration procedure.
* Overall, I suggest having separate DAO for User, Board, and Group later. It is to make classes depend less on each other.
* Since DAO was missing from CRC cards, it is hard to follow your scenarios. For example, how does Max create a group? How does Max invite users?

# Mark

* User Stories (19/20)
* MVP (14/15)
* CRC Cards (9/15)
* All other parts, full mark.
* Total: 67/75
