# NBA-Injuries-Analysis
This README provides an overview of the NBA-Injury-Analyses project contained within this repository. This project consists of web-scraping (from multiple sources), intensive data cleaning, data processing (merging datasets, feature engineering), and the creation of visualizations to generate useful insights. 

## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Data Sources](#data-sources)
* [What Makes This NBA Injury Analysis Unique?](#what-makes-this-nba-injury-analysis-unique?)
* [Results](#results)
* [Conclusion](#conclusion)
* [Repositiory Code Description](#repository_code_description)
### Motivation	
The outcome of the 2018/2019 NBA season was largely shaped by a rash of devasting injuries to star players (Kevin Durant, Klay Thompson, DeMarcus Cousins, and Victor Oladipo to name a few). In recent years there **_seems_** to be an increasing number of high profile players experiencing serious injuries (ACL tears, achilles ruptures, lower leg fractures), which in turn cause them to miss significant playing time, often to the detriment of their team's success.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/injury.png)
*Fig.1: (L) Kevin Durant's achilles tear; (R) Klay Thompson's torn MCL in the 2018/2019 NBA Finals*

### Objective
The objective of this project was to determine if serious injuries **_are_** really on this rise in the NBA, and in doing so, explore the nature of NBA injuries during the past decade. For the purposes of this analysis I nominally define "serious injuries" as those causing a player to miss 15 or more games.

### Data Sources
1. **NBA Injury Data**

   NBA injury data was scraped from the website [Prosports Transactions](http://prosportstransactions.com/). This site maintains an open-source archive of sports "transactions", including "the most complete database of pro basketball transactions available". For the purposes of this analysis two complementary "transaction" types were particularily useful: 
   * **"Missed games due to injury/personal reasons"**
      * This transaction type occurs when a player misses game while on their team's Active List (each team is only allowed to keep 11 players on its active list). These missed game events are typically short duration (1-3 games) 
   * **"Movement to/from injured/inactive list (IL)"**
      * This transaction type occurs when a player is placed on the Inactive List. Serious injuries typically result in a player being placed on their team's Inactive List; this allows another player to assume their spot on the Active List.
   
   An "transaction" event in this database provides the following information (see screenshot below):
   *  'Date' - Date of missed game/ movement to IL 
   *  'Team' - The player's team
   *  'Acquired' - The name of the player returning to lineup.
   *  'Relinquished' - The name of the player missing a game or placed on the IL.
   *  'Notes' - A description of the event and injury (sometimes).
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/prosports_transactions_sheetshot.jpg"> 
*Fig.2: Screenshot of search results from Prosports Transactions
   
2. **NBA Schedule Data**

   Team schedules(2010-2019) were scraped from the website [Basketball Reference](http://basketballreference.com/), allowing me to:
   * *Determine how many games a player actually missed due to injury*
   * *Determine when the missed game occured (game number and season - regular, post, or offseason) (regular, post, or offseason)*
   
3. **NBA Player Statistics/Bio Data**

   Player statistics was also scraped from the website [Basketball Reference](http://basketballreference.com/), allowing me to:
   * Examine correlations between player age and usage (games played, minutes played) and injury events
   * Constrain analysis to players with a minimum amount of playing times (I chose a 10 minutes per game average); this eliminates noise due to reserve/transient players.

### What makes _this_ NBA injury analysis unique?

This project is not the first to use [Prosport Transactions](http://prosportstransactions.com/) data to explore injury trends, it is however the first (I believe) to **tie both NBA schedule data and player stats/bio to transactions. The merging of injury transactions and schedule data, is not a simple effort, but by doing this it allows me to determine the number of games missed due to injury, rather than simply looking at the number of "transactions" that occured**. The latter is actually a very poor metric for tracking injuries because it treats all injuries as equal (eg. a sore hamstring != a torn achilles)). Consider the plots below:

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_plot_injury_events.png)
*Fig.3: Count of **injury events (transactions)** each season. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_all_injuries.png)
*Fig.3: Count of **missed games** each season. [Note: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*

**Looking only at Figure: 1 (injury events (transactions)) one might come to the conclusion that the NBA's injury posture is much better today (2017-2018) than it was in the past (2010-2012). If we actually look at the number of games missed (Figure 2) we  see the _opposite_ story is true.** Furthmore, by identifying the number of games missed due to each injury, we can also separate serious injuries from minor.

In addition to incorporating schedule data, this analysis also merges injury transactions with player stats/bio data allowing to one look at how injuries correlate with player age and usage.

### Results 
#### League-wide Injury Trends

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/stacked_bar_missed_games_all_injuries.png)

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/stacked_bar_missed_games_serious_injuries.png)

<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/body_map_all_injuries2018.png" width="400"/> <img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/body_map_serious_injuries2018.png" width="400"/>


#### Team Trends 
#### Correlations To Player Usage and Age



<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/serious_injury_body_map_2018.png"  width="400" height="400">
### Conclusions 

### Repository Code Description

## Sources
To run this project, install it locally using npm:
