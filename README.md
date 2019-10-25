# NBA-Injuries-Analysis
This README provides an overview of the NBA-Injury-Analyses project contained within this repository. This project consists of web-scraping (from multiple sources), intensive data cleaning, data processing (merging datasets, feature engineering), and the creation of visualizations to generate useful insights. 

## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Data Sources](#data-sources)
* [What Makes This NBA Injury Analysis Unique](#what-makes-this-nba-injury-analysis-unique)
* [Results](#results)
* [Conclusion](#conclusion)
* [Repositiory Structure](#repository_structure)
## Motivation	
The outcome of the 2018/2019 NBA season was largely shaped by a rash of devasting injuries to star players (Kevin Durant, Klay Thompson, DeMarcus Cousins, and Victor Oladipo to name a few). In recent years there **_seems_** to have been an increasing number of high profile players experiencing serious injuries (ACL tears, achilles ruptures, lower leg fractures), in turn causing them to miss significant playing time, often to the detriment of their team's success.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/injury.png)
*Fig.1: (L) Kevin Durant's achilles tear; (R) Klay Thompson's torn MCL in the 2018/2019 NBA Finals*

## Objective
The objective of this project was to determine if serious injuries **_are_** really on the rise in the NBA, and in doing so, explore the nature of NBA injuries during the past decade. For the purposes of this analysis, I nominally define "serious injuries" as those causing a player to miss 15 or more games.

## Data Sources
1. **NBA Injury Data**

   I scraped NBA injury data from the website [Prosports Transactions](http://prosportstransactions.com/). This site maintains an open-source archive of sports "transactions", including "the most complete database of pro basketball transactions available". For the purposes of this analysis, two complementary "transaction" types were particularly useful: 
   * **"Missed games due to injury/personal reasons"**
      * This transaction (event) occurs when a player - who is currently on their team's active roster - misses a scheduled game. These missed game events are typically short duration (1-3 games). 
   * **"Movement to/from injured/inactive list (IL)"**
      * This transaction (event) occurs when a team places a player on their inactive roster. Teams typically move a player to the inactive roster if the player is expected to be out for an extended period of time. This allows another (healthy) player to assume the injured player's spot on the active roster.
   
   A "transaction" event in this database provides the following information (see screenshot below):
   *  'Date' - Date of missed game/ movement to IL 
   *  'Team' - The player's team
   *  'Acquired' - The name of the player returning to lineup
   *  'Relinquished' - The name of the player missing a game or placed on the IL
   *  'Notes' - A description of the event/injury
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/prosports_transactions_sheetshot.jpg"> 

*Fig.2: Screenshot of search results from Prosports Transactions*
   
2. **NBA Schedule Data**

   I scraped team schedules (2010-2019) from the website [Basketball Reference](http://basketballreference.com/). This data allowed me to:
   * *Determine how many games a player actually missed due to injury*
   * *Determine when the missed game occurred (game number and season - regular, post, or offseason)*
   
3. **NBA Player Statistics/Bio Data**

   I also scraped player statistics from the website [Basketball Reference](http://basketballreference.com/), allowing me to:
   * Examine correlations between player age and usage (games played, minutes played) and injury events
   * Constrain analysis to players with a minimum amount of playing times (I chose a 10 minutes per game average); this eliminates noise due to reserve/transient players.

## What makes _this_ NBA injury analysis unique?

This project is not the first to use [Prosport Transactions](http://prosportstransactions.com/) data to explore injury trends. It is however the unique in that it **ties both NBA schedule data and player stats/bio to transactions. The merging of injury transactions and schedule data allowed me to determine the number of games missed due to injury, rather than simply looking at the number of "transactions" that occurred**. The latter is a rather naive metric for tracking injuries because it treats all injuries as equal (a sore hamstring != a torn achilles)). Consider the plots below:

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_plot_injury_events.png)
*Fig.3: Count of **injury events (transactions)** each season. [Note: Excludes "non-injury" events including missed games due to personal reasons, rest, sickness; Excludes injuries affecting players averaging less than 10 minutes per game].*


Figure 3, a count of injury events each season, gives the impression that the NBA's injury posture is better today (the 2017 and 2018 seasons) than it was in the recent past (2010-2013). Figure 4, a count of missed games each season due to injury, however presents a very different story, as the 2017 and 2018 seasons appear to have the highest missed games totals in the past 9 seasons.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_all_injuries.png)
*Fig.4: Count of **missed games** each season. [Note: Excludes "non-injury" events including missed games due to personal reasons, rest, sickness; Excludes injuries affecting players averaging less than 10 minutes per game].*

From a team/player/fan's perspective its not the number of injury events that really matters, its the number of games missed. 

## Results 
### Injury Trends
#### Missed Games

Figures 5  provides evidence that the last two seasons have experienced an increase in the number of games missed due to injuries relative to the prior 7 seasons. 

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_all_injuries_c2018.png)
*Fig.5: Count of **missed games** each season. [Note: Excludes "non-injury" events including missed games due to personal reasons, rest, sickness; Excludes injuries affecting players averaging less than 10 minutes per game].*

Likewise, Figures 6  provides evidence that the last two seasons have experienced an increase in the number of games missed due to _serious_ injury  (injury duration > 15 games) relative to the prior 7 seasons. 

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_serious_injuries_c2018.png)
*Fig.6: Count of **missed games due to serious injuries** each season. [Note: Excludes "non-injury" events including missed games due to personal reasons, rest, sickness; Excludes injuries affecting players averaging less than 10 minutes per game].*

While these plots provide evidence to support my original hypothesis, further data exploration is necessary to  understand why this behavior is occuring. It may simply be due to randonmess of injuries (a serious injury at the start of the season will result in more missed games than an injury near the end of the season) or it could a real trend that might give the teams and players cause for concern.

#### Injury Types

The next thing we can look at is the type of injuries that are occuring. Figure 7 is a word cloud representation of the injury "notes" provided with each injury transaction. 

<p align="center">
   <img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/word_cloud.png">
   
   *Fig.6: Word cloud of injury "notes" built from 2010-2019 NBA seasons transaction data*
</p>

There were literally hundreds of variations of injury notes and as such it was necessary to process the text prior to analysis. For each note I extracted an injury "key word" (a specific body part), and then further group these "key words" into categories (body regions). Figure 7 below displays a stacked bar chart that breaks down missed games by injured "body region". For instance, "lower leg" encompasses shin, calf, tibia, ankle, and achilles injuries. It's clear that knee and lower leg injuries are the primary driver of missed games across all seasons, 2017 and 2018 included.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/stacked_bar_missed_games_all_injuries.png)
*Fig.7: Count of **missed games (all injury durations)** each season, broken down by **affected body region**. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*

We can look at this in finer granuality by breaking down body regions in to body parts.  In Figure 8 below, I visually map the count of missed games to specific body parts. Circle size is proportional to the number of missed games.

<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/hor_bar_all_injuries2018.png" width="400"/><img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/body_map_all_injuries2018.png" width="400"/>
   
*Fig.8: Mapping of 2018-2019 missed games to specific body parts. Circle size is proportional to number of missed games. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*


If we limit our analysis to serious injuries (Figure 9 and Figure 10 below), we see that knee and ankle injuries are the top serious injuries.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/stacked_bar_missed_games_serious_injuries.png)
*Fig.9: Count of **missed games due to serious injuries** each season, broken down by **affected body region**. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*

<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/hor_bar_serious_injuries2018.png" width="400"/><img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/body_map_serious_injuries2018.png" width="400"/> 
*Fig.10: Mapping of 2018-2019 missed games to specific body parts. Circle size is proportional to number of missed games.[Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*


### Suprising Observations and Trends

 

**Rest Days**

Players may miss games or move temporarily to the inactive list simply for rest. In recent years we see rest days becoming more prevalent (Figure 12). Intuitively I expected more rest might lead to fewer injuries, but that does not seem to be the case. Rather it may be that players are needing to rest more because of increased injuries. Further investigation is needed, particularly to understand the lack of 2018 rest days reporting.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_rest.png)

*Fig.12: Missed games where 'rest' is cited as the reason. [Note:Included only players averaging 10 minutes per game].*

**Temporal Dependence of Injury Events**

Intuitively I expected there to be more injuries later in the season as players wear down, Figure 13 however suggests that the rate of injury is actually fairly constant over the course of the season.

<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/ridge_plot_all_injuries.png" width="400"/>

*Fig.13: Count of injury events over the course of an 81+ game season. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game]*

**Correlations To Player Usage and Age**

Finally, I expected to see some positive correlation betweeen player age or player usage (total minutes played in prior seasons) with missed games. The correlation matrix below suggests that this is not actually the case.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/correlation_plots.png)

*Fig.14: Correlatin plot of player age, cummulative minutes player over prior seasons, and missed games due to injury. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game]*

## Conclusions

This exploratory data analysis of NBA injuries revealed that serious injuries may in fact be on the rise. Additional analysis is needed to better understand the factors driving this change, and to investigate the surprising observations described in the section above.

## Repository Structure

### Work Flow
The figure below shows the workflow of scraping, cleaning, and processing that I executed prior to creating visualizations.
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/workflow.png" width="600"/>

### Folder Structure
All scripts and data files can be found the appropriate directory below.
![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/folder_structure.png)


