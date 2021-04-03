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


## Introduction

Unfortunately, I am a small man. As a result, in physical confrontations, it is clear that in most circumstances things would not go well. Naturally, my first instinct would be to run as fast as possible in the opposite direction of any would-be attacker, but, I don't run so good, so likely they would catch up with me anyway. Now I'm in the same situation as before, except hot, sweaty, and out of breath. Trust me, no one wants to see that.

As a result, while building up my cardio engine to race away from potential danger, I need an alternative strategy. Building such an engine might take a while too since running is basically just slamming your knees into concrete one after the other, not really my idea of a fun time. Therefore, I have done some analysis! I have looked into what makes the best fighter in an effort to mold myself into such a precense to terryify opponents, scaring them away. Also, it's a nice investigation to see what sort of natural benefits are brought by different body types. We always see Fighters' Reach and Height differences before a fight, but do they really mean anything? Well, it's time to find out.


## Past Literature

There are many different philosphies when it comes to fighting. [Bruce Lee](https://en.wikipedia.org/wiki/Bruce_Lee) often said to 'be like water', indicating the necessity of being fluid, adaptable, flexible to anything that is presented to you. From this was born [Jeet Kune Do](https://en.wikipedia.org/wiki/Jeet_Kune_Do), widely considered one of the first attempts at mixing the martial arts. [Conor McGregor](https://en.wikipedia.org/wiki/Conor_McGregor) further emphasised this movement focussed aspect of fighting, even hiring his own movement coach, [Ido Portal](https://en.wikipedia.org/wiki/The_Ido_Portal_Method). There are [interviews](https://www.youtube.com/watch?v=eATllx9jdRM) with McGregor belittling (no surprise there) larger fighters being ['stiff as a board'](https://www.youtube.com/watch?v=sFkoF0IzXeg) and 'addicting to strength and conditioning'. Here a fighter must be nimble and have control over his movements. This echoes a man many consider [the greatest ever](https://en.wikipedia.org/wiki/Muhammad_Ali), 'float like a butterfly, sting like a bee'.

A classic counter to this is simply to get more jacked. Pack on the muscle and build the appearance of someone who stops trains for a living and crushes rocks with his biceps on 'chill' Sunday morning. This is definitely one way to go, and looking at [Francis Ngannou](https://en.wikipedia.org/wiki/Francis_Ngannou), the current heavyweight world champion, this might not be a bad idea. [Here is a video](https://www.youtube.com/watch?v=K76etdV24-Q) of him lifting Shaq in case you needed a bit more evidence than just looking at his Greek God Bod. However, this would come with immediate backlash, we need only go back to [Isreal Adesanya's](https://en.wikipedia.org/wiki/Israel_Adesanya) fight against [Paulo Costa](https://en.wikipedia.org/wiki/Paulo_Costa_(fighter)), another Greek God bodybuilder turned MMA Fighter. Adesanya constantly referenced before the fight the importance of [technique over muscles](https://talksport.com/sport/mma/768538/israel-adesanya-paulo-costa-hump-ufc-253-ko/). The outcome speaks for itself, 2nd Round KO and a win for Adesanya.

Clearly there is some debate here and no one really knows what the 'ultimate' fighter would look like. Therefore, this will be an investigation into exactly that, and what the statistics say about what really matters in the fight game.

One of the first things that you come across when looking at fighters are stats about their physique. More specifically, their Reach and Height. It is natural for one to think that the further a person's reach is the better. They can hit you and you can't touch them. However, [Chael Sonnen](https://en.wikipedia.org/wiki/Chael_Sonnen), former UFC fighter and general authority on all things fighting, has often said that reach and distance only matters when you know how to use it and the only fighters who know how to use it are Jon Jones and Isreal Adesanya, [2:05](https://youtu.be/62hQxjIutmA?t=120). This would indicate that in the vast majority of settings, Reach really doesn't matter, and any advantage gained would be offset but being the same weight (fighters have the same weight limit, so a smaller fighter can have more additional muscle in excess of normal and still come in at a legal weight). This is one of the first things that we will investigate.

Further to this, a common adage in fighting is that ['styles make fights'](styles make fights clothing). There are a multitude of different styles that a fighter can take on. In boxing alone you can fight Ortodox, Southpaw, or even a mix of the two. On top of this, in the UFC, fighters come from all sorts of backgrounds, Wrestling, muay Thai, Jiu Jitsu. So what really is the best on to go for? This is what the [UFC](https://en.wikipedia.org/wiki/UFC_1) was initially set up to answer, collecting the crème de la crème from a variety of disciplines and squaring them off. After a night of intense action and ferocious competition it was concluded, Jiu Jitsu is the best of the best. So....problem solved, let's go home. Well not so fast. As the wise leader of the fighter people, Chael Sonnen, [says](https://www.youtube.com/watch?v=WR_vt2ftIGQ) that's a thing of the past. Fighters nowadays are skilled in all aspects, it's no longer good enough to come in as a striking specialist or a one trick pony grappler. Even the man many say is the greatest of all time, [Khabib Nurmagomedov](https://en.wikipedia.org/wiki/Khabib_Nurmagomedov), renowned for his unparalelled wrestling skills, is still a master striker, who can forget [that](https://www.youtube.com/watch?v=8ftcIKvL4Ic) overhand right cracking McGregor at his own game. Given this, it results in an interesting question, is there really one sport that beats out the others, or are jack-of-all-trades the real kings?
