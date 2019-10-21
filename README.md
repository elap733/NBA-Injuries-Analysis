# NBA-Injuries-Analysis
This README provides an overview of the NBA-Injury-Analyses project; a project to web-scrape, clean, process, and visualize National Basketball League injury data.  

## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Data Sources](#data-sources)
* [What Makes This NBA Injury Analysis Unique?](#what-makes-this-nba-injury-analysis-unique?)
* [Results](#results)
* [Conclusion](#conclusion)
* [Detailed Jupyter Notebooks](#detailed_jupyter_notebooks)
### Motivation	
The outcome of the 2018/2019 NBA season was largely shaped by a rash of devasting injuries to star players (see pictures below). In recent years there **_seems_** to be an increasing number of high profile players experiencing serious injuries (ACL tear, Achilles, fractured bones), which in turn cause them to miss significant playing time, often detrimentally impacting their team's success.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/injury.png)
*Fig.1: (L) Kevin Durant's achilles tear; (R) Klay Thompson's torn MCL in the 2018/2019 NBA Finals*

### Objective
The objective of this project was to determine if serious injuries **_are_** really on this rise in the NBA, and in doing so, explore the nature of NBA injuries during past decade. For the purposes of this analysis I nominally define "serious injuries" as those causing a player to miss 15 or more games.

### Data Sources
1. **Injury Data**

   NBA injury data was scraped from the website [Prosport Transactions](http://prosportstransactions.com/). This site maintains an open-source archive of sports transactions, including "the most complete database of pro basketball transactions available". For the purposes of this analysis two transactions types were particularily useful: 
   * **Movement to/from injured/inactive list (IL)**
   * **Missed games due to injury/personal reasons**
   
   An "transaction" event in this database looks like the following:
  
  
2. **NBA Schedule Data**

   Team schedules(2010-2019) were scraped from the website [Basketball Reference](http://basketballreference.com/) in order to:
   * **Determine how many games a player missed due to injury**
   * **When an injury occured (season type (regular, post, or offseason) and game number)**
   
3. **NBA Player Statistics/Bio Data**

   Player statistics (games played, minutes played) and bio (age, position) was also scraped from the website [Basketball Reference](http://basketballreference.com/).


### What Makes This NBA Injury Analysis Unique?

While I do not claim that this project is the first to use [Prosport Transactions](http://prosportstransactions.com/) data for the purposes of analyzing injury trends; I believe that it significantly advances these analyses by **tying both NBA schedule data and player stats/bio to transactions**, after careful cleaning and processing. 

**The merging of transactions and schedule data allows one to determine the number of games missed due to injury, rather than simply looking at the number of "transactions" that occured**. The latter is a poor metric for tracking injuries because it treats all injuries as equal (eg. a sore hamstring == a torn achilles)).After identifying the number of games missed due to each injury, one can identify separate serious injuries from minor.

Additionally, the merging of transactions with player stats/bio data allows to one look at injury trends as they relate to player age and usage.

### Results 

### Conclusions 

### Detailed Jupyter Notebooks




## Sources
To run this project, install it locally using npm:
