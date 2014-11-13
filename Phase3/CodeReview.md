# Code Reviews

The table below indicates which team member reviewed which other team member's code.

| Reviewer | Coder |
| -------- | ----- |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| ***REMOVED*** |  ***REMOVED*** |
| GitHub username 6 |  GitHub username 7 |
| GitHub username 7 |  GitHub username 1 |


-----

## Reviewer : Sample reviewer

NOTE: This is an example of a good format for a code review - It is very short, yet very informative (assuming you actually include links). You don't have to follow this format, but it can give you an idea of what we want to see - Short description of highlights, and links to isses/commits/pull-requests that allow us to get more details.

 * I found several minor bugs (_links to issues_), and managed to fix a few of them (_links to commits or pull-requests_).
 * I suggested an improvement to the design of _component X_ (for more details, _link to issue_), as well as some additional useful features (_links to issues_).
 * I thought that the implementation of _component Y_ was very elegant - 
The use of _interface Z_ (_link to source file_) made it really easy to add _component Y_ to the rest of the system.

You can see all of my comments by searching for issues with the label _code-review-MyGitHubUsername_ (_link to search results_).


-----

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

## Reviewer : GitHub username 6

-----

## Reviewer : GitHub username 7

