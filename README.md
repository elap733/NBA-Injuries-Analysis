# NBA Injury Analysis

This README provides an overview of the NBA Injury Analysis project contained within this repository. This project consists of web-scraping (from multiple sources), data cleaning, data processing (merging datasets, feature engineering), and the creation of visualizations to generate insights. 

## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Methodology](#methodology)
  * [Scraping](#scraping)
  * [Cleaning](#cleaning)
  * [Processing](#processing)
* [Analysis](#analysis)
  * [Analysis of Injury Trends](#analysis-of-injury-trends)
  * [Analysis of Other Factors](#analysis-of-other-factors)
* [Conclusion](#conclusion)
* [Repositiory Structure](#repository_structure)

## Motivation	
The outcome of the 2018/2019 NBA season was largely shaped by a rash of devastating injuries to star players, including Kevin Durant, Klay Thompson, DeMarcus Cousins, and Victor Oladipo. In recent years there **_seems_** to be an increasing number of high profile players experiencing serious injuries (ACL tears, achilles ruptures, lower leg fractures), in turn causing them to miss significant playing time, often to the detriment of their team's success.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/injury.png)
*Fig.1: (L) Kevin Durant's achilles tear; (R) Klay Thompson's torn MCL. Both events occurred in the 2018/2019 NBA Finals*

## Objective
The objective of this project was to determine if serious injuries **_are_** really on the rise in the NBA, and while doing so, explore the nature of NBA injuries during the past decade. 

## Methodology

The flowchart below provides an overview of this project's workflow. In the sections which follow, I provide further explanation of the scraping, cleaning, and processing steps that I executed.

<p align="center">
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/workflow.png" width="600"/>
</p>

### Scraping

Using Python's _BeautifulSoup_ package I created four scripts to automate data scraping from the following data sources:

#### Data Sources 

1. **NBA Injury Data** (_missed game events_ data and _inactive list events_ data)

   I scraped NBA injury data (2010-2019) from the website [Prosports Transactions](http://prosportstransactions.com/). This site maintains an open-source archive of sports "transactions", including "the most complete database of pro basketball transactions available". For the purposes of this analysis, two "transaction" types are particularly relevant:
   * **"Missed games due to injury/personal reasons"**
      * This transaction (event) occurs when a player - who is currently on their team's active roster - misses a scheduled game. These missed game events are typically short duration (1-3 games). 
   * **"Movement to/from injured/inactive list (IL)"**
      * This transaction (event) occurs when a team places a player on their inactive roster. Teams typically move a player to the inactive roster if the player is expected to be out due to an injury for an extended period of time. This allows another (healthy) player to assume the injured player's spot on the active roster.
   
   A "transaction" event in this database provides the following information (see screenshot below):
   *  'Date' - Date of missed game/ movement to IL 
   *  'Team' - The player's team
   *  'Acquired' - The name of the player returning to lineup
   *  'Relinquished' - The name of the player missing a game or placed on the IL
   *  'Notes' - A description of the event/injury

<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/prosports_transactions_sheetshot.jpg"> 

*Fig.2: Screenshot of search results from Prosports Transactions*

​		My scraped injury datasets included more than 14,000 "inactive list events" and more than 11,000 "missed game events".

2. **NBA Schedule Data**

   I also scraped team schedules (2010-2019) from the website [Basketball Reference](http://basketballreference.com/). This data allowed me to:
   * Determine how many games a player actually missed due to injury
   * Determine when the missed game occurred (i.e. the season  -  regular, post, or offseason)
   * Determine the number of back-to-back game sets that occurred in each season (a potential factor in injury trends)
   
3. **NBA Player Statistics/Bio Data**

   I also scraped player statistics (1994-2019) from the website [Basketball Reference](http://basketballreference.com/). This scraped dataset of more than 19,000 entries allowed me to:
   * Examine correlations between player age, usage (minutes played) and injury events
   * Constrain my analysis to players with a minimum amount of playing time.
     * In this analysis I used a threshold of 10 minutes played per game average (i.e. a player must have averaged at least 10 minutes per game during the season in which the injury event occurred)
     * By doing this I was able to focus my analysis on the most relevant segment of the player population - starters and first string reserve players.
       * An additional reason for eliminating second and third-string reserve players is that these players tend to frequently move between the NBA and it's development league (the G-league). During my exploration of NBA inactive list events I found that these G-league transfers actually require a team to place the player on it's inactive list. Unfortunately the transaction "note" for this particular subset of inactive list transactions does not indicate that this is the reason (it only states "placed on IL"). If these players are included in the dataset then their G-league transfers will be wrongly counted as injury events

[Link to code for data scraping](https://github.com/elap733/NBA-Injuries-Analysis/tree/master/src/d01_scrapes)

[Link to raw datasets](https://github.com/elap733/NBA-Injuries-Analysis/tree/master/data/01_raw)

### Cleaning 

After scraping missed game events, inactive list events, schedules, and player stats, I cleaned each of these datasets. 

_Cleaning steps_:

- Dropping unnecessary columns
- Dropping rows with missing data
- Formatting injury dates
- Formatting season "name" in a consistent fashion
  - My  convention: a season is referred to by the year in which the season started (ex. the 2018/2019 season began in 2018 so I refer to it as the "2018" season)
- Formatting team names in a consistent fashion
  - Consistent team name format was critical for merging/linking datasets.
  - Inconsistencies that needed to be handled:
    - Some datasets used team name abbreviations (e.g. OKC), others used mascots name (e.g. Thunder). My  convention: team name = full city name + mascot (e.g. Oklahoma City Thunder)
    - Several teams have changed names and cities over the past decade. Some, like the Charlotte Hornets, have changed names and cities multiple times. 
- Formatting player names in a consistent fashion
  - Consistent player name format/spelling was also critical for merging/linking datasets. 
  - Inconsistencies that needed to be handled:
    - _Basketball Reference_ uses special characters (accents) - _Prosports Transactions_ does not.
    - _Prosports Transactions_ includes suffixes (Jr., Sr., III) - _Basketball Reference_ does not.
    - Some players have multiple aliases (name spellings) . _Prosports Transactions_ includes all aliases/spellings with each transaction, _Basketball Reference_ uses just a single  name spelling for each player.

[Link to code for data cleaning]( https://github.com/elap733/NBA-Injuries-Analysis/tree/master/src/d01_scrapes )

#### Processing 

After cleaning I executed the following processing steps to prepare the data for analysis:

_Processing of Player Stats data_:

- For every NBA player calculate the following for each season in which they played:
  - Total minutes played in prior seasons
  - Total games played in prior seasons

_Processing of NBA Schedules data_:

- For each game, identify the season in which it occurred (regular or post) 
- Calculate the number of back-to-back game sets each season

_Processing of Inactive List_ and _Missed Game Events_ data:

- For each event calculate the number games missed due to that event
  - This was the important, but also most complicated processing step. It required processed NBA schedule data as an additional input.
- Process transaction "notes" to facilitate injury analysis
  - I filtered transaction "notes" using a "key word" dictionary. This allowed me to sort out which events were due to injury, which events were due to rest, which events were due to sickness, which were due to other personal reasons (e.g. funeral, birth), which events were due to suspension, etc.
  - For those events due to actual injury, I further identified the injured body part (e.g. shin, ankle, knee, shoulder) and body region (e.g. lower leg, upper leg , torso).

_Merging processed Inactive List / Missed Game Events data with Player Stats data_:

- Merge datasets on "player name" and "year" columns

[Link to code for processing data]( https://github.com/elap733/NBA-Injuries-Analysis/tree/master/src/d03_process  )

## Analysis  

This analysis focuses on players averaging more than 10 minutes per game in a given season. For the purposes of this analysis,  "serious injuries" are defined as those causing a player to miss 15 or more games.

### Analysis of Injury Trends

While this project is not the first to use [Prosport Transactions](http://prosportstransactions.com/) data to explore injury trends, it is unique in that it **ties both NBA schedule data and player stats to transactions. In particular, the merging of injury transactions and schedule data allowed me to determine the number of games missed due to injury, rather than simply looking at the number of "transactions" that occurred**. The latter is an imperfect metric for tracking injuries because it treats all injuries as equal (a sore hamstring != a torn achilles). Consider the plots below:

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_plot_injury_events.png)
*Fig.3: Count of **injury events (transactions)** each season. [Code to recreate plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_bar_all_injuries_events.py)<br/>[Note: Excludes "non-injury" events including missed games due to personal reasons, rest, sickness; Excludes injuries affecting players averaging less than 10 minutes per game].*


Figure 3, a count of injury events each season, gives the impression that the NBA's injury posture is better today (the 2017 and 2018 seasons) than it was in the recent past (2010-2013). Figure 4 however, which shows the count of missed games each season due to injury, presents a very different story, as the 2017 and 2018 seasons appear to have the highest missed games totals in the past 9 years.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_all_injuries_c2018.png)
*Fig.4: Count of **missed games** each season. [Figure notes: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game].[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_bar_missed_games_all_injuries_c2018.py)*

Likewise, Figures 5  provides evidence that the last two seasons have experienced an increase in the number of games missed due to _serious_ injury  (injury duration > 15 games) relative to the prior 7 seasons. 

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_serious_injuries_c2018.png)
*Fig.5: Count of **missed games due to serious injuries** each season. [Figure notes: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game].[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_bar_missed_games_serious_injuries.py)*

One can argue that from the perspective of both teams and fans, its not the number of injury events that really matters, but rather the number of games missed.

While these plots provide evidence to support my original hypothesis, further data exploration is necessary to  understand why this behavior is occurring. This could be a real trend that should give teams and players cause for concern, or this "trend" may simply be due to the randomness of injuries. For instance, a serious injury at the start of the season will result in more missed games than an injury that occurs near the end of the season, simply because of timing.

#### Injury Types - All Injury Durations

The next thing we can look at is the type of injuries that have been occurring and see if there any interesting trends in recent years. 

Figure 6 is a word cloud representation of the injury "notes" provided with each injury transaction. 

<p align="center">
   <img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/word_cloud.png">
   *Fig.6: Word cloud of injury "notes" built from 2010-2019 NBA seasons transaction data.[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_word_cloud.py)*
</p>

There were many unique text strings in the injury notes and as such it was necessary to process the text prior to analysis. For each note I extracted an injury "key word" (a specific body part), and then further group these "key words" into categories (body regions). Figure 7 below displays a stacked bar chart that breaks down missed games by injured "body region". For instance, "lower leg" encompasses shin, calf, tibia, ankle, and achilles injuries. It's clear that knee and lower leg injuries are the primary driver of missed games across all seasons, 2017 and 2018 included. In general, the proportion of injuries appears relatively constant across all seasons.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/stacked_bar_missed_games_all_injuries.png)
<<<<<<< HEAD
*Fig.7: Count of **missed games (all injury durations)** each season, broken down by **affected body region**. [Figure notes: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game].[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_bar_missed_games_all_injuries.py)*
=======

*Fig.7: Count of **missed games (all injury durations)** each season, broken down by **affected body region**. [Figure notes: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game].*
>>>>>>> cd577216a36dcb7ad5205054084384ed5903c071

We can look at injuries in finer granularity by examining which specific body parts have been getting injured the most.  In Figure 8 below, I map the count of missed games to specific body parts for the 2018 season. Circle size is proportional to the number of missed games.

<p align="center">
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/body_map_all_injuries2018.png">
<<<<<<< HEAD
*Fig.8: Mapping of 2018-2019 missed games to specific body parts. Circle size is proportional to number of missed games. [Figure notes: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_bar_missed_games_all_injuries.py) *
=======
>>>>>>> cd577216a36dcb7ad5205054084384ed5903c071
</p>

*Fig.8: Mapping of 2018-2019 missed games to specific body parts. Circle size is proportional to number of missed games. [Figure notes: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*



#### Injury Types - Serious Injuries

Alternatively we can limit our analysis to serious injuries (more than 15 games missed). 

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/stacked_bar_missed_games_serious_injuries.png)
*Fig.9: Count of **missed games due to serious injuries** each season, broken down by **affected body region**. [Figure notes: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_bar_missed_games_serious_injuries.py)*

<p align="center">
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/body_map_serious_injuries2018.png">
</p>
<<<<<<< HEAD
*Fig.10: Mapping of 2018-2019 missed games due to serious injury to specific body parts. Circle size is proportional to number of missed games.[Figure notes: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].[Link to code to create plot]( https://github.com/elap733/NBA-Injuries-Analysis/blob/master/src/d04_visualization/plot_body_map_serious_injuries.py)*
=======

*Fig.10: Mapping of 2018-2019 missed games due to serious injury to specific body parts. Circle size is proportional to number of missed games.[Figure notes: excluded events related to personal reasons, rest, sickness; included only players averaging 10 minutes per game].*
>>>>>>> cd577216a36dcb7ad5205054084384ed5903c071


In Figure 9 and Figure 10 above, we see that ankle, knee, and foot account for the majority of serious injuries - a relatively consistent trend across seasons. 

### Analysis of Other Factors

In order to investigate why players are missing more games in recent years, there are a number of external factors we may want to analyze. Here I look at the following factors:

- _Games missed for rest each season_ - intuitively one might expect that more rest days should reduce injuries; less rest days should contribute to more injuries
- _Player age/usage_ - how did the age distribution of players in 2017/2018 compare to prior seasons? how did the distribution of career minutes of players in 2017/2018 compare to those in prior seasons?
- _Schedule (number of back to back sets)_ - If players are playing more back-to-back games this could result in more injuries
- _Timing of injuries_ - Is when injuries occur during a season changing?

#### Rest 

We can look at the number of games players are missing for rest each season and see how that has changed over time. In Figure 11 we see a dramatic increase in games missed due to rest in 2015, 2016, and 2017, relative to prior seasons. 

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_missed_games_rest.png)

*Fig.11: Missed games where 'rest' is cited as the reason. [Note: Only includes players averaging 10 minutes per game].*

Interestingly there appears to be an unbelievable result - zero games were missed for rest in 2018. I closely inspected the data and confirmed that 'rest' is not listed on any of the transaction notes. Yet [media reports](https://www.nbcsports.com/philadelphia/nba-insider-tom-haberstroh/kawhi-leonards-regular-season-rest-could-topple-warriors-dynasty) suggest that players did indeed miss games for rest in 2018 - just like any other season. I believe this result reflects a [change](https://www.espn.com/nba/story/_/id/20851002/nba-board-governors-votes-pass-legislation-draft-lottery-reform-guidelines-resting-healthy-players) in how NBA teams are reporting (or not reporting) rest days. The increase in games missed for rest in 2015 and 2016 was widely panned by fans and the [media](https://www.cbssports.com/nba/news/everything-you-need-to-know-about-the-nbas-rest-controversy-including-solutions/). Fans were understandably unhappy to show up to games see their favorite players play sit on the bench despite being healthy. The absence of reported rest games in 2018 may be the result of NBA teams "disguising" rest games to avoid further fan and media backlash. Rather than noting a missed game was due to rest, teams may be choosing to attribute the missed game to some minor "injury".

While the number of games missed for rested in the 2018 season was certainly non-zero, I do wonder if the NBA's revised rest policy has actually driven down that number relative to prior seasons

The 2018 NBA season withstanding, my initial suspicion - that increased injuries may be due to players getting fewer games off for rest - does not seem to be supported by the data. The 2017 season had both a high number of games missed due to injury and games missed for rest. 

#### Player Usage

One possible explanation for the increase injuries may be that player demographics have changed over time. Is the average player age increasing? Did players in 2017 and 2018 come into the start of the season with more "wear and tear" (career minutes) than in prior seasons (2010-2016)?  Let's investigate these questions in the plots below.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/distplot_age_all.png)

*Fig.12: Distribution plot comparing player ages in the 2010-2016 seasons(blue curve) and 2017-2018 seasons (red curve). [Note: Only includes players averaging 10 minutes per game].*

Fig 12 compares the distribution of player ages (all players averaging 10 MPPG in a given season) in the 2010-2016 seasons and the 2017-2018 seasons. The distributions appear fairly similar, however we do see some subtle differences particularly in the 35-40 year demographic, and evidence that the 2010-2016 seasons may have actually had an older player population than the 2017-2018 seasons.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/distplot_min_all.png)

*Fig.13: Distribution plot comparing career minutes played entering each of the 2010-2016 seasons (blue curve) and each of the 2017-2018 seasons (red curve). [Note: Only includes players averaging 10 minutes per game].*

Fig 13 compares the distribution of all players' career minutes entering a given season. The distributions closely overlap, though the 2010-2016 seasons do seemed to be skewed ever so slightly to the right(higher career minutes), consistent with the age trends in Fig. 12

We can also look at the demographics of injured player, to see if there are any interesting trends there.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/distplot_age_inj.png)

*Fig.14: Distribution plot comparing age of _injured players_ in the 2010-2016 seasons(blue curve) and 2017-2018 seasons (red curve). [Note: Only includes players averaging 10 minutes per game].*

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/distplot_min_inj.png)

*Fig.15: Distribution plot comparing career minutes played entering each of the 2010-2016 seasons (blue curve) and each of the 2017-2018 seasons (red curve) for _injured players_. [Note: Only includes players averaging 10 minutes per game].*

The difference in demographics of _injured players_ in 2017-2018 and prior seasons (2010-2016) appears more pronounced. Injured players in the 2017-2018 seasons tended to be younger and have fewer career minutes than injured players in the 2010-2016 seasons. An older player population does not seem to be the driving force for the spike in injuries.

#### Schedule

The NBA's schedule can be grueling, particularly during back-to-back sets (two or more consecutive games played on consecutive calendar days). Has the number of back-to-back sets increased in recent years? Figure 16 shows the number of back-to-back sets each season.

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/bar_back_to_backs.png)

*Fig.16:  Back-to-back sets each season. [Note A back-to-back set consists of two or more consecutive games that occur on consecutive calendar days].*

Rather than increasing, it's clear that the number of back-to-back sets have been decreasing. I looked into this further and it appears that [the NBA made a concerted effort to reduce back-to-backs in 2015](https://nba.nbcsports.com/2018/08/10/nba-schedule-reduces-back-to-backs-provides-some-mid-season-homecomings/) after player and team complaints. Rather than reduce the number of games played during the regular season, the NBA increased the number of calendar days in the regular season. In order to do this however they've steadily shortened the NBA preseason in order to move the start of the regular season from late October/early November to mid-October. 

#### Timing of Serious Injuries

Figure 17 shows a heatmap of serious injuries occurrences over the course of the last nine seasons. 

![Fig](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/results/01_plots/calendar_heat_map_serious_injury.png)

*Fig.17: Heat map of games missed to serious injury events over the course of the season.  [Figure notes: excluded events related to personal reasons, rest, sickness; only includes players averaging 10 minutes per game; only includes injuries with injury durations greater than 15 games; 2011 season was a strike shortened season that began in December]*

Note that this plot shows the number of games missed due to serious injury events that occurred in in a given month- NOT the number of games missed that month. For instance if a player tore his ACL in November and was out for the rest of the season, all of those missed games would be counted toward November's total. Two additional notes/caveats when interpreting this plot: (1) April/May will inherently appear to have fewer serious injuries than other months simply because teams may have less than 10 games left in the season at that point;(2) the 2011 season was a strike shortened season that began in December rather than October/November.

Intuitively I expected more serious injures to occur later in the season as players wear down, Figure 17 however suggests that in recent years, the most serious injuries are occurring early in the season.  Could this trend be related to shortened preseasons and an earlier start to the season? A shortened preseason may be hindering player conditioning, placing them in higher risk for injury at the start of the regular season. 


## Conclusions

This exploratory data analysis of NBA injuries revealed that missed games and serious injuries have increased in recent years. After diving deep in to the data, it difficult though to conclusively say whether this increase is a real trend that should be cause for concern, or if its just an artifact of injury randomness.  The increased number of missed games due to serious injuries at the _start_ of the season is a particularly interesting trend, that could be related to the NBA's shortened pre-seasons slates in recent years. Additionally I found that the NBA revised rest policy, seems to be affecting how team's are reporting player rest days. If this policy change is actually deterring teams from resting players (this data is not available) then this could also be a driver for increased injuries.

## Repository Structure

### Folder Structure
All scripts and data files can be found the appropriate directory below.
<img src="https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/folder_structure.png" width="400"/>


