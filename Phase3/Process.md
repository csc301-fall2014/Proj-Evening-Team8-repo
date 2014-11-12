**Columns:**

* Todo
* Implementing
* Testing

**WIP limits:**

We chose to use WIP limits on a per-person basis.  The reasoning for this is that our application is actually very modular - we realized that there are very few dependencies between the user stories we needed to implement for this phase, and that everyone could work mostly independently.

As a result, we decided that each person should have no more than two items assigned to them in the 'Implementing' and 'Testing' columns respectively, and that the Todo column would have no limit to the number of items (i.e. we created a list of items we wanted to see for this phase at the beginning, and each member could take one or two of those items at a time to implement).

**Github Issue usage:**

We created a relatively strict convention for using Github issues:

Each item on the Kanban would have a single issue that describes it, and all Kanban items have a 'feature' tag associated with them.  The column that said item belongs to can be identified by a second tag, either 'Todo', 'Implementing', or 'Testing'.  When an item has been deemed complete, the issue is closed.

Issues should be given a descriptive name.  More importantly, the branch associated with the issue should include the Issue ID in its name.

For example, the Kanban item for notifications (issue #37) started with a 'feature' tag indicating that it is indeed a Kanban item, and a 'Todo' tag, indicating that its currently in the 'Todo' column of the Kanban.  Dylan decided to implement this item, and so the tag was changed to 'Implementing', and then 'Testing' as development continued.  When the item was deemed complete, the issue was closed.  Note that all work for this item was done in the notifications37 branch, a name which is easily identifible and makes it easy to locate the corresponding issue.


**Comparison with Scrum:**