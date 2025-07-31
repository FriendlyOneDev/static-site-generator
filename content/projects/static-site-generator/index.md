# Static Site Generator

[GitHub](https://github.com/FriendlyOneDev/static-site-generator)

This one is all about splitting huge project into smaller tasks, and then splitting those smaller tasks even further via OOP. This is also true for how this project operates.

It converts markdown files into valid html files. Including looking up markdown files in subdirectories to generate additional pages, like this one you're reading. 

It does it via following algorithm, continuesly splitting down each file and reassembling it at the end.

1. Split into Blocks 
2. Classify Block Types 
3. Convert to TextNodes (inline) 
4. Convert to HTMLNodes 
5. Assemble Final HTML 
6. Inject into Template

I don't know what to showcase here, there's nothing to screenshot, but you can see all of those files raw markdown files [here](https://github.com/FriendlyOneDev/static-site-generator/tree/main/content). 