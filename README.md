# Obsidian Orphans - managing orphaned image attachments

When copy and pasting web pages or when importing Evernote notes, image attachments are brought into my Obsidian vault. I have set a specific folder to contain these attachments, away from the notes themselves (so avoid clutter in my folder view).

However, when cleaning up these imported notes and particularly when deleting irrelevant images from a note, the image attachment files themselves are not deleted and hence remain as probable orphans in my attachments folder. These take up disk space unnecessarily and also use up my Obsidian Sync space quota too.

So this project is to write a tool that I can run to:
1. report on image files in my attachments folder that are **not** referenced in any notes files in my vault.
2. move orphans to another folder if I choose to (a sort of recycle bin in case I want to review and keep them).
3. delete orphans (perhaps only from the recycle bin and if having been there for some time).

So (1) will be the first milestone release, (2) the second and (3) the third.