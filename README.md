# CRICKET TRUMP CARD GAME #
### github.com/AlexMathew/Trump-Card-Game ###


*** To bring back some memories ***


## THE BACK STORY ##
In the late 90s..
I started following cricket because of playing trump card games with my cousins. Knowing players, and having a general picture of their level of performance, is how I started following players in the game. 

A while back, for reasons unknown, I started thinking about these again. I remembered a Sachin Tendulkar card that I had - it said "Matches played : 128". And if I played that card now, that'd be like, the biggest joke. So I started thinking - "what if we could have updated stats on the cards ?". And that's how this began.


## THE WORKING ##
To put it simply, extract the stats in real time from [Cricinfo](http://espncricinfo.com). 

The [Players database homepage](http://espncricinfo.com/ci/content/player/index.html) contains links to individual team pages. Each team page contains links to the pages of all the players currently active, or still under contract. These player pages contain the stats of that player.
The required regular expressions are used to extract information that appears in this pattern.
