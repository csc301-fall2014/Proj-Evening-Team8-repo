# Code Reviews

The table below indicates which team member reviewed which other team member's code.

| Reviewer | Coder |
| -------- | ----- |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| GitHub username 7 |  GitHub username 1 |

------

## Reviewer : ***REMOVED***

 * I found a minor bug in table view CSS where the tables weren't wrapping properly. Spencer promptly fixed it in [this commit](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/commit/70358fdb284ec396d1fa0b3c7318d0bec62ad690).
 * I changed the name attribute of the submit type input in [this commit](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/commit/f27671831f6133e6be8ac6c3776ea9df4da3b863) and appended POST_ before the name to ensure that any POST requests sent from [tableview.html](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/blob/tagsintables59/messageboard/mainsite/templates/tableview.html) are interpreted by the view tableview in [views.py](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/blob/tagsintables59/messageboard/mainsite/views.py) correctly as it only checks if a name is present in the entire POST, which contains many other names referring to actual data inputs.
 * I think Spencer's implementation of messaging in [table view](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/blob/tagsintables59/messageboard/mainsite/templates/tableview.html) is really creative. He uses hidden inputs to allow users to simply press Enter and have the message sent to the server then have the page update and show the message.
 * Overall I am impressed with how Spencer follows PEP-8 throughout all his code. His work was simple, intuitive, easy to read, and made extending them with tags and filters easy in [this branch](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/tree/tagsintables59). His code also had no major bugs at all, showing that he had done some testing himself on top of the testing done by another member.

-----

## Reviewer : ***REMOVED***

* Alec's use of a Django form in edituserprofile.html and forms.py in [this commit](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/commit/a2e6263c868f7239d344f6889ee0d5d33fa116cd) allow for very readable code that has a very clear purpose
* On the topic of readability there is a lot of inconsistent white spacing in Alec's edituserprofile.html and userprofile.html which make quick scans of the code, additionally his commit messages, while funny, made my code review substantially more time consuming
* On [this commit](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/commit/2b818c542ddaae44605b89eb529b7ad0c50a710b) Alec implements accepting group invites. His code in general for invites is good but the commented out code and the lack of an HttpResponseRedirect after working with the POST request need fixes.
* Overall while some of his code is not optimal, it has all of the required functionality

-----

## Reviewer : ***REMOVED***

-----

## Reviewer : ***REMOVED***

 * Overall easy-to-read code, meaningful varialbe names. Maybe just a little bit of whitespace to seperate if elif else statements.
 * Didn't find any bugs, and was intuitive code. There was a little piece of unnecessary code I removed in views.py of [this code](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/tree/subadmins50). When using a Many To Many Relation, you only need to add to one side of it, although you have to remove from both sides.
 * I thought the way that Allen implemented the sub-admins for groups allows for a lot of extension. He didn't restrict the powers that they can have, so it would be simple to give or take away the privelages. For example, if a new group feature is added that only admins and sub-admins should have, it would take almost no code to allow them access to the feature.

-----

## Reviewer : ***REMOVED***

-----

## Reviewer : ***REMOVED***

* Code is well-formatted and readable, with meaningful names for variables and functions.
* Unfortunately, I found the implementation for polls to be fairly inflexible ([views.py](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/blob/poll2/messageboard/mainsite/views.py) lines 151-180).  The implementation allows for only 4 choices to the poll, no more no less, and results in rather bloated code.  Taking advantage of built-in relationship sets (poll.choices.all(), poll.choices.add() for example) would clean up the code quite a bit and make it much easier to create a flexible module.  This would be a good goal for the next phase.
* Izzy's implementation of deletion and editing of messages was very well done;  I don't think we made any changes to it after its early implementation.  Editing and deletion are both implemented on the topic view page ([commit 8aa1d6c](8aa1d6c4fd1763d3e1c7d52423353941c4bb631e)) in a very robust and intutive way.  Edit and delete buttons only appear to users who are eligible to perform these actions, which makes the process very clear and user-friendly.

-----

## Reviewer : GitHub username 7

