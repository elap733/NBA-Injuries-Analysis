# NBA-Injuries-Analysis
This README provides an overview of the NBA-Injury-Analyses project contained within this repository. This project consists of web-scraping (from multiple sources), intensive data cleaning, data processing (merging datasets, feature engineering), and the creation of visualizations to generate useful insights. 

## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Data Sources](#data-sources)
* [What Makes This NBA Injury Analysis Unique?](#what-makes-this-nba-injury-analysis-unique?)
* [Results](#results)
* [Conclusion](#conclusion)
* [Detailed Jupyter Notebooks](#detailed_jupyter_notebooks)
### Motivation	
The outcome of the 2018/2019 NBA season was largely shaped by a rash of devasting injuries to star players (Kevin Durant, Klay Thompson, DeMarcus Cousins, and Victor Oladipo to name a few). In recent years there **_seems_** to be an increasing number of high profile players experiencing serious injuries (ACL tears, achilles ruptures, lower leg fractures), which in turn cause them to miss significant playing time, often to the detriment of their team's success.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/injury.png)
*Fig.1: (L) Kevin Durant's achilles tear; (R) Klay Thompson's torn MCL in the 2018/2019 NBA Finals*

### Objective
The objective of this project was to determine if serious injuries **_are_** really on this rise in the NBA, and in doing so, explore the nature of NBA injuries during past decade. For the purposes of this analysis I nominally define "serious injuries" as those causing a player to miss 15 or more games.

### Data Sources
1. **NBA Injury Data**

   NBA injury data was scraped from the website [Prosport Transactions](http://prosportstransactions.com/). This site maintains an open-source archive of sports transactions, including "the most complete database of pro basketball transactions available". For the purposes of this analysis two complementary transactions types were particularily useful: 
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

   
2. **NBA Schedule Data**

   Team schedules(2010-2019) were scraped from the website [Basketball Reference](http://basketballreference.com/), allowing me to:
   * *Determine how many games a player actually missed due to injury*
   * *Determine when the missed game occured (game number and season - regular, post, or offseason) (regular, post, or offseason)*
   
3. **NBA Player Statistics/Bio Data**

   Player statistics was also scraped from the website [Basketball Reference](http://basketballreference.com/), allowing me to:
   * Examine correlations between player age, games played, and minutes per game with injury events
   * Constrain analysis to players with a minimum amount of playing times (10 minutes per game average); this eliminates noise due to reserve/transient players.

<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/serious_injury_body_map_2018.png"  width="400" height="400">

### What Makes This NBA Injury Analysis Unique?

While I do not claim that this project is the first to use [Prosport Transactions](http://prosportstransactions.com/) data for the purposes of analyzing injury trends; I believe that it significantly advances these analyses by **tying both NBA schedule data and player stats/bio to transactions**, after careful cleaning and processing. 

**The merging of transactions and schedule data allows one to determine the number of games missed due to injury, rather than simply looking at the number of "transactions" that occured**. The latter is a poor metric for tracking injuries because it treats all injuries as equal (eg. a sore hamstring == a torn achilles)).After identifying the number of games missed due to each injury, one can identify separate serious injuries from minor.

Additionally, the merging of transactions with player stats/bio data allows to one look at injury trends as they relate to player age and usage.

### Results 

### Conclusions 

### Detailed Jupyter Notebooks




## Sources
To run this project, install it locally using npm:
