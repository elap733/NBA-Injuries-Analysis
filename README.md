# NBA-Injuries-Analysis
This README provides an overview of the NBA-Injury-Analyses project; a project to web-scrape, clean, process, and visualize National Basketball League injury data.  

## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Results](#results)
* [EDA Process](#eda-process)

### Motivation	
The outcome of the 2018/2019 NBA season was largely shaped by a rash of devasting injuries to star players (_see pictures below_). In recent years there **_seems_** to be an increasing number of high profile players experiencing serious injuries (ACL tear, Achilles, fractured bones), which in turn cause them to miss significant playing time, often detrimentally impacting their team's success.

![Ouch](https://github.com/elap733/NBA-Injuries-Analysis/blob/master/references/02_images/injury.png)
*Fig.1: (L) Kevin Durant's achilles tear; (R) Klay Thompson's torn MCL in the 2018/2019 NBA Finals*

### Objective
The objective of this project was to determine if serious injuries **_are_** really on this rise in the NBA, and in doing so, explore the nature of NBA injuries during past decade. For the purposes of this analysis we nominally define "serious injuries" as those causing a player to miss 15 or more games.

### Data Sources
1. Injury Data

   NBA injury data was scraped from the website [_Prosport Transactions_ ](http://prosportstransactions.com/). This site maintains an open-source archive of sports transactions, including "the most complete database of pro basketball transactions available". For the purposes of this analysis two transactions types were particularily useful: 
   * **Movement to/from injured/inactive list (IL)**
   * **Missed games due to injury/personal reasons**
  An "transaction" event in this database looks like the following:
  
  
2. NBA Schedule Data

   Team schedules(2010-2019) were scraped from the website [ Basketball Reference ] (http://basketballreference.com/) in order to:
   * **Determine how many games a player missed due to injury**
   * **When an injury occured (season type (regular, post, or offseason) and game number)**
3. NBA Player Statistics/Bio Data
Player statistics (games played, minutes played) and bio (age, position) was also scraped from the website [ Basketball Reference ] (http://basketballreference.com/).


### What Makes This NBA Injury Analysis Unique

While this project does not claim to be the first use of [_Prosport Transactions_ ](http://prosportstransactions.com/) data for the purposes of analyzing injury trends; it is unique in **that it ties both NBA schedule data and player stats/bio to these transactions**. 

**The merging of transactions and schedule data allows one to determine the number of games missed due to injury, rather than simply looking at the number of "transactions" occured (a naive metric that treats all injuries as equal (eg. a sore hamstring == a torn achilles)).** After identifying the number of games missed due to each injury, one can identify separate serious injuries from minor.

Additioanlly, the merging of transactions with player stats/bio data allows to one look at injury trends as they relate to player age and usage.


### Approach
Primary Data sources - prosportstransactions
Schedule

### Differentiation From Other NBA Injury Analyses




### Objective
### Results
	
## EDA Overview
To run this project, install it locally using npm:

## Sources
To run this project, install it locally using npm:
