# NFL_wintotal_analysis
This project that runs in 135 lines of code creates a polynomial regression to determine the correlation between preseason win-totals and pace adjusted game score for NFL games. This project only uses data from the 2020 season in order to make its analysis. The data was scraped from various betting databases and from ESPN play-by-play.

The Y variable for this project is novel and differs from most used to predict NFL outcomes. It is net points per drive. By dividing the score by the amount of drivers, this adjusts for pace and thus is more predictive than pure score. There between two teams where one wins wins by 14 in 7 drivers than between two teams where one wins by 21 in 21 drives.

The r squared of 0.1606 is mild, yet shows some correlation.
