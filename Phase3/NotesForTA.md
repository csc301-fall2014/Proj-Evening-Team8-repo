Unfortunately, commit frequency and commit lines are a fairly poor indicator of individual contributions for this project.  Here are some specific cases where a member will be under or overrepresented in their commits:

**Creating the initial framework:** Creating the initial Django project results in a lot of auto-generated code, resulting in a high number of commit lines.  See [this commit](00a49a2bcfa6c2a6787ace71dd4740a84f1c4710).

**Migrations:** Whenever the database is modified, a new migrations .py file will be created, which contains a lot of auto-generated code meant for creating our SQLite databse.  Often, these migrations will need to be entirely regenerated to solve merging conflicts.  See [this commit](73ff0e13af964b1932e0bd77dc7c32df2461b0a1) as an example, where multiple migrations file are purged and a new one is created in its place.

**HTML templates:** HTML templates result in a significant number of line commits due to their bloated nature.  At the same time, however, these templates are often much easier to implement than their respective controllers.  The majority of thought and implementation time goes into the controllers and models in views.py and models.py, while the templates (.html files) have much less required work per line.

**Individual concerns regarding individual contribution:**

We were unfortunately not able to merge Izzy's branch with the master branch before the Phase 3 deadline, due to some structural changes in master causing some major conflicts.  Her work for Phase 3 can be found in [branch poll2](https://github.com/csc301-fall2014/Proj-Evening-Team8-repo/tree/poll2)
