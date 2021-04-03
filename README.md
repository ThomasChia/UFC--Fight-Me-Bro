# UFC--Ready-to-Rumble
Scraping and analysing UFC data to see what actually matters when two people clash inside and go to war.


Things to look at:
- Age difference between winners and losers - histogram
- Reach difference between winners and losers
- Height difference between winners and losers
- Stances with most wins and most wins as a percentage. Tricky as one stance might dominate, so need to fix this.
- Types of finishes (KO, Sub, etc.)
- Does past record affect win percentage, would imagine u-shaped, so more wins better until a certain point due to damage to body. Look at a fighters clock - how many fights do they have to win a world championship?
- More strikes make you more likely to win?
- Look to create an all time ranking
- Regression to have a look at the impact of reach on likelihood of winning
- Add in the machine learning models from betting.


## Table of contents
* [Introduction](#introduction)
* [Past Literature](#past-literature)
* [Data Collection and Cleaning](#data-collection-and-cleaning)
* [Data Inspection](#data-inspection)
* [The Reach Advantage](#the-reach-advantage)
* [Styles Make Fights](#styles-make-fights)


## Introduction

Unfortunately, I am a small man. As a result, in physical confrontations, it is clear that in most circumstances things would not go well. Naturally, my first instinct would be to run as fast as possible in the opposite direction of any would-be attacker, but, I don't run so good, so likely they would catch up with me anyway. Now I'm in the same situation as before, except hot, sweaty, and out of breath. Trust me, no one wants to see that.

As a result, while building up my cardio engine to race away from potential danger, I need an alternative strategy. Building such an engine might take a while too since running is basically just slamming your knees into concrete one after the other, not really my idea of a fun time. Therefore, I have done some analysis! I have looked into what makes the best fighter in an effort to mold myself into such a precense to terryify opponents, scaring them away. Also, it's a nice investigation to see what sort of natural benefits are brought by different body types. We always see Fighters' Reach and Height differences before a fight, but do they really mean anything? Well, it's time to find out.


## Past Literature

There are many different philosphies when it comes to fighting. [Bruce Lee](https://en.wikipedia.org/wiki/Bruce_Lee) often said to 'be like water', indicating the necessity of being fluid, adaptable, flexible to anything that is presented to you. From this was born [Jeet Kune Do](https://en.wikipedia.org/wiki/Jeet_Kune_Do), widely considered one of the first attempts at mixing the martial arts. [Conor McGregor](https://en.wikipedia.org/wiki/Conor_McGregor) further emphasised this movement focussed aspect of fighting, even hiring his own movement coach, [Ido Portal](https://en.wikipedia.org/wiki/The_Ido_Portal_Method). There are [interviews](https://www.youtube.com/watch?v=eATllx9jdRM) with McGregor belittling (no surprise there) larger fighters being ['stiff as a board'](https://www.youtube.com/watch?v=sFkoF0IzXeg) and 'addicting to strength and conditioning'. Here a fighter must be nimble and have control over his movements. This echoes a man many consider [the greatest ever](https://en.wikipedia.org/wiki/Muhammad_Ali), 'float like a butterfly, sting like a bee'.

A classic counter to this is simply to get more jacked. Pack on the muscle and build the appearance of someone who stops trains for a living and crushes rocks with his biceps on 'chill' Sunday morning. This is definitely one way to go, and looking at [Francis Ngannou](https://en.wikipedia.org/wiki/Francis_Ngannou), the current heavyweight world champion, this might not be a bad idea. [Here is a video](https://www.youtube.com/watch?v=K76etdV24-Q) of him lifting Shaq in case you needed a bit more evidence than just looking at his Greek God Bod. However, this would come with immediate backlash, we need only go back to [Isreal Adesanya's](https://en.wikipedia.org/wiki/Israel_Adesanya) fight against [Paulo Costa](https://en.wikipedia.org/wiki/Paulo_Costa_(fighter)), another Greek God bodybuilder turned MMA Fighter. Adesanya constantly referenced before the fight the importance of [technique over muscles](https://talksport.com/sport/mma/768538/israel-adesanya-paulo-costa-hump-ufc-253-ko/). The outcome speaks for itself, 2nd Round KO and a win for Adesanya.

Clearly there is some debate here and no one really knows what the 'ultimate' fighter would look like. Therefore, this will be an investigation into exactly that, and what the statistics say about what really matters in the fight game.

One of the first things that you come across when looking at fighters are stats about their physique. More specifically, their Reach and Height. It is natural for one to think that the further a person's reach is the better. They can hit you and you can't touch them. However, [Chael Sonnen](https://en.wikipedia.org/wiki/Chael_Sonnen), former UFC fighter and general authority on all things fighting, has often said that reach and distance only matters when you know how to use it and the only fighters who know how to use it are Jon Jones and Isreal Adesanya, [2:05](https://youtu.be/62hQxjIutmA?t=120). This would indicate that in the vast majority of settings, Reach really doesn't matter, and any advantage gained would be offset but being the same weight (fighters have the same weight limit, so a smaller fighter can have more additional muscle in excess of normal and still come in at a legal weight). This is one of the first things that we will investigate.

Further to this, a common adage in fighting is that ['styles make fights'](styles make fights clothing). There are a multitude of different styles that a fighter can take on. In boxing alone you can fight Ortodox, Southpaw, or even a mix of the two. On top of this, in the UFC, fighters come from all sorts of backgrounds, Wrestling, muay Thai, Jiu Jitsu. So what really is the best on to go for? This is what the [UFC](https://en.wikipedia.org/wiki/UFC_1) was initially set up to answer, collecting the crème de la crème from a variety of disciplines and squaring them off. After a night of intense action and ferocious competition it was concluded, Jiu Jitsu is the best of the best. So....problem solved, let's go home. Well not so fast. As the wise leader of the fighter people, Chael Sonnen, [says](https://www.youtube.com/watch?v=WR_vt2ftIGQ) that's a thing of the past. Fighters nowadays are skilled in all aspects, it's no longer good enough to come in as a striking specialist or a one trick pony grappler. Even the man many say is the greatest of all time, [Khabib Nurmagomedov](https://en.wikipedia.org/wiki/Khabib_Nurmagomedov), renowned for his unparalelled wrestling skills, is still a master striker, who can forget [that](https://www.youtube.com/watch?v=8ftcIKvL4Ic) overhand right cracking McGregor at his own game. Given this, it results in an interesting question, is there really one sport that beats out the others, or are jack-of-all-trades the real kings?

## Data Collection and Cleaning

The data for this work was taken from the [UFC Website](http://ufcstats.com/event-details/6597b611f1c32555) containing all of the fights up to the end of 2020 (mainly because a lot of this was done over my Christmas holidays!). We have further combined this with individual fighter data for features such as Weight and Height. This was collected again from the UFC Website, but this time from the [individual fighters database](http://ufcstats.com/statistics/fighters). Having data all in one place and easily collectible was very useful and the main reason why data from other organisations, such as [Bellator](http://www.bellator.com) was not included. This could be something to do in the future to further improve the analysis performed. Overall, the UFC is seen as the most competitive and elite fighting organisation in the world, with the UFC Champions often considered as the best in the business. Given this, I am comfortable that the sample of data that I have collected is representative of fighters because they are considered the best in the world and there is no clear sampling bias, where for example the UFC is only recruiting knock-out artists. They want those who win, regardless of how they do so.

That last line sounded cool, however, it might not be wholly true. [Dana White's Contender Series](https://en.wikipedia.org/wiki/Dana_White%27s_Contender_Series) is a competition where unsigned fighters would compete to impress UFC President, [Dana White](https://en.wikipedia.org/wiki/Dana_White). Naturally, a spectacular one punch finish is often more impressive than a five round grinding chess match. As a result, those getting contracts in this manner are more likely to come from a striking heavy background, holding sufficient power to knock out opponents quickly and easily. However, this is not the only method of gaining a contract and generally we see the best fighters with the best records rising up over time and being signed. Evidence for this would be the master grappler who drags you down and smashes you into submission, Khabib. He may not be flashy with walk-off KOs, but that didn't stop him being ranked **#1** on the [Pound-for-Pound list](https://www.ufc.com/rankings) until the day he retired (aka the best there is).

To get this data in a workable form, I applied various transformations. This would allow me to extract as much information as possible, allowing us to gain as much insight as possible into what goes into being the best fighter. One of the first things that I did was create a an [ELO ranking](https://en.wikipedia.org/wiki/Elo_rating_system) for athletes. This would help to encorporate more information about fighters' past performances into our analysis beyond just a static record of wins, losses, and draws. This would give a sense of the level of past opponents and the results against them. This was done in the standard way, increasing the winner's score and decreasing the losers. However, a potential expansion on this idea would be to look at a potential penalty for number of fights. Unlike traditional sports, fighters often leave matches worse than when they starts. This is due to the damage that is suffered when competing. As a result a win in your 5th fight might be worth more in terms of experience compared to a win in your 40th fight, where you are taking damage on an already battered body.

Building on this, an additional set of features that might be useful in analysing fighters would be how they have performed in the past. However, we are not talking about their outputs or winning or losing, but rather their inputs. How many kicks they threw, punches, and even takedowns. We do this in a similar way to constructing the ELO, with a dictionary of fighters initially starting at 0, adding this to each fight, and then computing a new score based on that fight's information and sorting this updated number in the dictionary for the fighter's next fight. This will help us to look at how a fighter likes to fight. We do not have information on their main style of fighting (wrestler, grappler, striker etc.) so this will help us to determine this.

An idea that recently crept in as a result of both [Chael Sonnen](https://www.youtube.com/watch?v=bZ3RcJbu3Bg) and [Joe Rogan](https://en.wikipedia.org/wiki/Joe_Rogan) talking about McGregor [not fighting in a year](https://www.youtube.com/watch?v=hKIlZWBT6j8) leading to his last defeat, was to look into optimal recovery times and how this decends into 'ring rust'. We have added a feature that looks at days spent between fights. Including this into regressions and individual feature analysis will help us to determine if being out of the ring for a whole year really was a cause of McGregor's [recent defeat](https://www.bbc.co.uk/sport/mixed-martial-arts/55770669) to [Dustin Poirier](https://en.wikipedia.org/wiki/Dustin_Poirier). We anticipate that this will be a quadratic relationship as some recovery is good (fighting two fights in a row is probably a bad idea unless you are called [Khazmat](https://en.wikipedia.org/wiki/Khamzat_Chimaev)), but this would then change to a negative as you lose a feel for the fight and all the pressure and emotions that brings with it.

All of these features were added and then a difference was taken between the fighter and their opponent. This differences helps to put the statistics into perspective for the individual fights, rather than comparing absolute figures. An expansion of this idea could be to normalize each of the figures by the number of fights, giving stats per fight. This would reduce the bias for a fight who has had more fights, such as [Donald Cerrone](https://en.wikipedia.org/wiki/Donald_Cerrone) compared to someone newer. Past fights was also included to remove any variation in results that this might cause.

Finally, a nice easy win for the data cleaning portion of this project. A simple join bring it all together, adding simple physical stats like Reach and Height. Love it.

## Data Inspection

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)


## The Reach Advantage



## Styles Make Fights


