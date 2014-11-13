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

Overall our team preferred Kanban over scrum. The main reason being how much more restricting scrums were, through sprint backlogs and the number of meetings. It was hard to get all 7 of us in one place for scrum meetings, due to conflicting schedules and other matters. In Kanban we were free to work at whatever pace each of us could handle, and while that left the group more open for procrastination it also allowed us to more easily work around our other courses. Kanban was also helpful in testing and monitoring progress of features, using the issues allowed us to flag branches ready for testing and merging rather than hoping everyone had their parts under control.

Despite this, we also found that Kanban may not have worked as well for Phase 2 as it did for Phase 3.  By the start of phase 3, our project had become very modular, and it was easy to divide the work into independent tasks to fit Kanban.  In phase 2, however, there was a lot of groundwork that needed to be done before we could start expanding into new features, so having daily meetings to explore how the infrastructure of our project was developing was extermely helpful, as we couldn't work independently on a large number of tasks.

All in all, for the reasons mentioned above, we preferred Kanban in the context of Phase 3, but Scrum was probably more effective in the context of Phase 2..
