# Downloader Bot

[GitHub](https://github.com/FriendlyOneDev/downloader-bot)

This is my first truly personal project—and I'm really happy with how it turned out. Why? Because it's something people actually use!  
I'm also proud of its structure, it's easy to follow along due to modularity. And this project's structure I came up, as opposed to boot.dev's course where they tell you that this and that should be separate.

In Telegram group chats, a lot of meme links are from TikTok or Instagram. But those platforms are either designed to keep you hooked or are just plain annoying to use without an app or account. That's where Downloader Bot comes in.

We used to rely on an existing bot that handled this, but it occasionally sent ads—which was incredibly annoying. So I made my own!

Some time ago, I bought a cheap laptop to practice Linux and host small projects. Well, it's now doing just that: quietly running this bot 24/7 from inside a closet.

The bot is starting to spread across my friend group's chats. At the time of writing this (7 days after I added tracking stats), it's already in 9 chats and has processed 62 links.

The flow is fairly simple. The bot uses regex to detect TikTok or Instagram links (I'm also considering adding support for Reddit and YouTube). It extracts the link, determines which service it's from, then uses the appropriate downloader.

After downloading, it groups the media, sends it to the chat, and deletes the temporary files - a nice, clean loop. If any errors occur during this process, they're caught and I’m personally notified about them via Telegram.

[You can add it too if you want.](https://t.me/friendly_downloader_bot)

![bot_stats](/images/bot_stats.png)
