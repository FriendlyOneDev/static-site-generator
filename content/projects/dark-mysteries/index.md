# Dark Mysteries

[GitHub](https://github.com/FriendlyOneDev/dark-mysteries)

This is a project we built during a 3 day hackathon from July 25th to 28th, 2025.

It was my first collaborative project - we were a team of three: one frontender and two backenders (I was one of the backend devs). We actually created a working website and deployed it on [Render](https://dark-mysteries.onrender.com/).  

_Note: the site may take a while to load due to Render's free tier, and it may be out of tokens depending on when you're reading this 😅._

The idea behind the site is inspired by old mystery games, where players ask yes/no questions to uncover the hidden story. The twist? You get to play with an LLM acting as the narrator.

We split the work into three parts:

- **My role:** I handled WebSocket and LLM integration, and also pitched in on server-side tasks whenever I had spare time.  
- [My backend friend](https://github.com/NataMontari): Built the server side using FastAPI.  
- [My frontend friend](https://github.com/BUTURUM): Took care of the frontend using Node and Vite. He also helped us untangle our git structure and maintain it's health, as he was the most experienced with GitHub.

![homepage](/images/homepage.png)
![story](/images/story.png)
![chat](/images/chat.png)

Also, you see those "<<<<<<< Updated upstream ======= >>>>>>> Stashed changes" in the upper left corner? That was a last minute push before the hackathon deadline, just to add "how to play functionality". In the spirit of hackathon we decided to not touch the project after the deadline. 
