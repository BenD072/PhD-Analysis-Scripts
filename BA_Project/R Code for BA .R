# Librairies will need to be installed before first use
install.packages("ggplot2")
install.packages("dplyr")
install.packages("hrbrthemes")
install.packages("tidyverse")
install.packages("tidyr")

# Libraries
library(ggplot2)
library(dplyr)
library(hrbrthemes)
library(tidyverse)
library(tidyr)

# 1) Boris Johnson trust
data <- read.csv("/Users/bendavies/Documents/Kent/Psychology/PhD/Nuffield/BA Project Files/AlteredBands All Surveys Split by Week csv.csv")

data <- data %>%  
  drop_na(PolTrustPercentTrust)

# make sure the date column is considered as such
data$Week <- as.Date(data$Date_Week, format = c("%d/%m/%Y"))

# Drop rows where N less than 100. 
data <- subset(data, N > 100)

# Aggregate Weeks with Multiple data points.
### 9/12/19 - BSE and UKC
survey1 <- subset(data, Date_Week == '09/12/2019', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'British Election Survey' & data$Date_Week == '09/12/2019', 6:8] <- vec
data[data$SurveyOrg == 'UKC Study' & data$Date_Week == '09/12/2019', 6:8] <- NA

### 24/02/2020 - MiC and UKC
survey1 <- subset(data, Date_Week == '24/02/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'More in Common' & data$Date_Week == '24/02/2020', 6:8] <- vec
data[data$SurveyOrg == 'More in Common' & data$Date_Week == '24/02/2020', 5] <- 1618
data[data$SurveyOrg == 'UKC Study' & data$Date_Week == '24/02/2020', 6:8] <- NA


# 23/03/2020 - Worldwide (Prolific and global) and C19.
survey1 <- subset(data, Date_Week == '23/03/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}
data[data$SurveyOrg == 'C19PRC' & data$Date_Week == '23/03/2020', 6:8] <- vec
data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Global)' & data$Date_Week == '23/03/2020', 6:8] <- NA
data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Prolific Representative)' & data$Date_Week == '23/03/2020', 6:8] <- NA

# 30/03/2020 - Distress and Worldwide
survey1 <- subset(data, Date_Week == '30/03/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}
data[data$SurveyOrg == 'COVIDistress' & data$Date_Week == '30/03/2020', 6:8] <- vec
data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Global)' & data$Date_Week == '30/03/2020', 6:8] <- NA

# 04/05/2020 - CLS and Nuff
survey1 <- subset(data, Date_Week == '04/05/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Centre for Longitudinal Studies' & data$Date_Week == '04/05/2020', 6:8] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '04/05/2020', 6:8] <- NA

# 11/05/2020 - CLS and Nuff.
survey1 <- subset(data, Date_Week == '11/05/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Centre for Longitudinal Studies' & data$Date_Week == '11/05/2020', 6:8] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '11/05/2020', 6:8] <- NA

### 22/06/2020 - MiC and UKC
survey1 <- subset(data, Date_Week == '22/06/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'More in Common' & data$Date_Week == '22/06/2020', 6:8] <- vec
data[data$SurveyOrg == 'More in Common' & data$Date_Week == '22/06/2020', 5] <- 2502
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '22/06/2020', 6:8] <- NA


# 13/07/2020 - NatCen and Nuff. 
survey1 <- subset(data, Date_Week == '13/07/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N, na.rm = T)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'NatCen' & data$Date_Week == '13/07/2020', 6:8] <- vec
data[data$SurveyOrg == 'NatCen' & data$Date_Week == '13/07/2020', 5] <- 2743
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '13/07/2020', 6:8] <- NA

# 27/07/2020 - C19 and Nuff. 
survey1 <- subset(data, Date_Week == '27/07/2020', select = c(N, PolTrustPercentTrust:PolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'C19PRC' & data$Date_Week == '27/07/2020', 6:8] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '27/07/2020', 6:8] <- NA

# transformation of the data to be able to create a figure with both trust and distrust on the same graph
# Add factor for before/after Cummings scandal date
data$prePostCummings <- 0
data$prePostCummings[data$Week > as.Date('2020-05-01')] <- 1

# Select key pieces of data for building the graph
test <- data %>%
  select(N, Week, PolTrustPercentTrust, PolTrustPercentDistrust, prePostCummings) %>%
  gather(key = "Measure", value = "value", -Week, -N, -prePostCummings)

test$value <- as.numeric(test$value)
test$prePostCummings[test$prePostCummings == 0] <- 'Pre-Cummings Event'  # Convert factors to word labels to be displayed on the graph
test$prePostCummings[test$prePostCummings == 1] <- 'Post-Cummings Event'
test$prePostCummings <- as.factor(test$prePostCummings)
test$Measure[test$Measure == 'PolTrustPercentTrust'] <- "Trust"
test$Measure[test$Measure == 'PolTrustPercentDistrust'] <- "Distrust"


test <- drop_na(test)

# code for the figure itself


test %>%
  ggplot(aes(x=Week, y=value)) +
  geom_line(aes(color = Measure, linetype = Measure), color= "black") +
  geom_point(shape=21, color="black", aes(size=N, fill=Measure)) +  # Data points for each survey, coloured by measure (trust vs. distrust)
  geom_smooth(data = subset(test, prePostCummings == 'Post-Cummings Event' & Measure == 'Trust'), aes(linetype = Measure), colour = 'purple', method = "lm", formula = y ~ x, se = F) +  # Add trend line for Trust data using the relevant linear formula for the post-Cummings period
  geom_smooth(data = subset(test, prePostCummings == 'Post-Cummings Event' & Measure == 'Distrust'), aes(linetype = Measure), colour = 'purple', method = "lm", formula = y ~ poly(x, 2), se = F) +  # Add trend line for Distrust data using polynominal formula for post-Cummings period
  geom_smooth(aes(linetype = Measure), , method = "lm", formula = y ~ poly(x, 4), colour="black") +  # Add overall trend lines
  coord_cartesian(ylim = c(0, 100), expand = TRUE, default = TRUE) +  # Set y axis limits
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  ggtitle("Change in political trust and distrust") +
  xlab(" ") +
  ylab("Percentage of respondents") +
  scale_fill_discrete(name = "Measure", labels = c("% who distrust", "% who trust")) +
  theme(plot.title = element_text(size=16),
        axis.title.y = element_text(size=14),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 12),
        ) + 
  geom_vline(xintercept = as.numeric(as.Date("2019-12-12")), linetype = "dashed") +  # Add event markers and their positions
  geom_vline(xintercept = as.numeric(as.Date("2020-03-05")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-26")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-05-25")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-06-15")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-07-04")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-09-14")), linetype = "dashed") +
  annotate("label", x = as.Date("2019-12-12"), y = 100, label = "General Election", size=3.5, alpha = 0.2, fill='grey') +
  annotate("label", x = as.Date("2020-03-05"), y = 90, label = "First UK COVID\ndeath", size=3.5, alpha = 0.2, fill='grey') +
  annotate("label", x = as.Date("2020-03-26"), y = 100, label = "Lockdown starts", size=3.5) +
  annotate("label", x = as.Date("2020-06-15"), y = 100, label = "Reopening of\nEnglish retail", size=3.5, alpha = 0.2, fill='grey') +
  annotate("label", x = as.Date("2020-05-25")-2, y = 75, label = "Dominic Cummings\nPress Conference", size=3.5) +
  annotate("label", x = as.Date("2020-07-04")+3, y = 90, label = "Reopening of pubs\nand restaurants", size=3.5, alpha = 0.2, fill='grey') +
  annotate("label", x = as.Date("2020-09-14")-2, y = 100, label = "New restrictions\n(Rule of 6)", size=3.5, alpha = 0.2, fill='grey') 


# Fit line equations. 
# Trust 
test2 <- test[test$Measure=="Trust",]
test2 <- test2[test2$Week > "2020-05-01",]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit3, fit4)  # Compare if addition of higher polynominal terms improves model fit

# Distrust 
test2 <- test[test$Measure=="Distrust",]
test2 <- test2[test2$Week > "2020-05-01",]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit4)




# WHEN SAVING THE FIGURE, export in 1150 x 600

#################################
## COVID Trust ##
###############################

# 1) COVID trust
data <- read.csv("/Users/bendavies/Documents/Kent/Psychology/PhD/Nuffield/BA Project Files/AlteredBands All Surveys Split by Week csv.csv")

data <- data %>%  
  drop_na(CovidPolTrustPercentTrust)

# make sure the date column is considered as such
data$Week <- as.Date(data$Date_Week, format = c("%d/%m/%Y"))

# Drop rows where N less than 100. 
data <- subset(data, N > 100)

# Aggregate Weeks with Multiple data points.
### 23/03/2020 - Worldwide (both)
survey1 <- subset(data, Date_Week == '23/03/2020', select = c(N, CovidPolTrustPercentTrust:CovidPolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Global)' & data$Date_Week == '23/03/2020', 9:11] <- vec
data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Global)' & data$Date_Week == '23/03/2020', 5] <- 4074
data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Prolific Representative)' & data$Date_Week == '23/03/2020', 9:11] <- NA

## 30/03/2020 - distress, worldwide, wellcome.
survey1 <- subset(data, Date_Week == '30/03/2020', select = c(N, CovidPolTrustPercentTrust:CovidPolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Global)' & data$Date_Week == '30/03/2020', 9:11] <- vec
data[data$SurveyOrg == 'Measuring Worldwide COVID-19 Attitudes (Global)' & data$Date_Week == '30/03/2020', 5] <- 3248
data[data$SurveyOrg == 'COVIDistress' & data$Date_Week == '30/03/2020', 9:11] <- NA
data[data$SurveyOrg == 'Wellcome COVID Monitor' & data$Date_Week == '30/03/2020', 9:11] <- NA

### 6th April - Distress and Wellcome
survey1 <- subset(data, Date_Week == '06/04/2020', select = c(N, CovidPolTrustPercentTrust:CovidPolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'COVIDistress' & data$Date_Week == '06/04/2020', 9:11] <- vec
data[data$SurveyOrg == 'COVIDistress' & data$Date_Week == '06/04/2020', 5] <- 451
data[data$SurveyOrg == 'Wellcome COVID Monitor' & data$Date_Week == '06/04/2020', 9:11] <- NA


### 13th April - Survation and Wellcome
survey1 <- subset(data, Date_Week == '13/04/2020', select = c(N, CovidPolTrustPercentTrust:CovidPolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Survation' & data$Date_Week == '13/04/2020', 9:11] <- vec
data[data$SurveyOrg == 'Survation' & data$Date_Week == '13/04/2020', 5] <- 3242
data[data$SurveyOrg == 'Wellcome COVID Monitor' & data$Date_Week == '13/04/2020', 9:11] <- NA

### 22nd June - Nuff and YouGov
survey1 <- subset(data, Date_Week == '22/06/2020', select = c(N, CovidPolTrustPercentTrust:CovidPolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '22/06/2020', 9:11] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '22/06/2020', 5] <- 1883
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '22/06/2020', 9:11] <- NA

### 7th September - Nuff and YouGov
survey1 <- subset(data, Date_Week == '07/09/2020', select = c(N, CovidPolTrustPercentTrust:CovidPolTrustPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '07/09/2020', 9:11] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '07/09/2020', 5] <- 1895
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '07/09/2020', 9:11] <- NA

# transformation of the data to be able to create a figure with both trust and distrust on the same graph (as above)
data$prePostCummings <- 0
data$prePostCummings[data$Week > as.Date('2020-05-01')] <- 1

test <- data %>%
  select(N, Week, CovidPolTrustPercentTrust, CovidPolTrustPercentDistrust, prePostCummings) %>%
  gather(key = "Measure", value = "value", -Week, -N, - prePostCummings)

test$value <- as.numeric(test$value)
test$prePostCummings[test$prePostCummings == 0] <- 'Pre-Cummings Event'
test$prePostCummings[test$prePostCummings == 1] <- 'Post-Cummings Event'
test$prePostCummings <- as.factor(test$prePostCummings)
test$Measure[test$Measure == 'CovidPolTrustPercentTrust'] <- "Trust"
test$Measure[test$Measure == 'CovidPolTrustPercentDistrust'] <- "Distrust"

test <- drop_na(test)

# code for the figure itself


test %>%
  ggplot(aes(x=Week, y=value)) +
  geom_line(aes(color = Measure, linetype = Measure), color= "black") +
  geom_point(shape=21, color="black", aes(size=N, fill=Measure)) +
  geom_smooth(data = subset(test, prePostCummings == 'Post-Cummings Event' & Measure == 'Trust'), aes(linetype = Measure), colour = 'purple', method = "lm", formula = y ~ x, se = F) +
  geom_smooth(data = subset(test, prePostCummings == 'Post-Cummings Event' & Measure == 'Distrust'), aes(linetype = Measure), colour = 'purple', method = "lm", formula = y ~ x, se = F) +
  geom_smooth(data = subset(test, Measure == 'Trust'), aes(linetype = Measure), , method = "lm", formula = y ~ x, colour="black") +
  geom_smooth(data = subset(test, Measure == 'Distrust'), aes(linetype = Measure), , method = "lm", formula = y ~ poly(x, 2), colour="black") +
  coord_cartesian(ylim = c(0, 100), expand = TRUE, default = TRUE) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  ggtitle("Change in COVID-19 related trust and distrust") +
  xlab(" ") +
  ylab("Percentage of respondents") +
  scale_fill_discrete(name = "Measure", labels = c("% who distrust", "% who trust")) +
  theme(plot.title = element_text(size=16),
        axis.title.y = element_text(size=14),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 12),
  ) + 
  geom_vline(xintercept = as.numeric(as.Date("2020-03-05")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-26")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-05-25")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-06-15")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-07-04")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-09-14")), linetype = "dashed") +
  annotate("text", x = as.Date("2020-02-01"), y = 100, label = " ", size=3.5) +
  annotate("label", x = as.Date("2020-03-05"), y = 90, label = "First UK COVID\ndeath", size=3.5, alpha = .02) +
  annotate("label", x = as.Date("2020-03-26"), y = 100, label = "Lockdown starts", size=3.5) +
  annotate("label", x = as.Date("2020-06-15"), y = 100, label = "Reopening of\nEnglish retail", size=3.5, alpha = .02) +
  annotate("label", x = as.Date("2020-05-25")-3, y = 75, label = "Dominic Cummings\nPress Conference", size=3.5) +
  annotate("label", x = as.Date("2020-07-04")+4, y = 90, label = "Reopening of pubs\nand restaurants", size=3.5, alpha = .02) +
  annotate("label", x = as.Date("2020-09-14")-2, y = 100, label = "New restrictions\n(Rule of 6)", size=3.5, alpha = .02) 

# Fit line equations
# Trust 
test2 <- test[test$Measure=="Trust",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit2)

# Distrust
test2 <- test[test$Measure=="Distrust",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit2)

#####################################
######## Boris Johnson Trust ###########
#########################################
data <- read.csv("/Users/bendavies/Documents/Kent/Psychology/PhD/Nuffield/BA Project Files/AlteredBands All Surveys Split by Week csv.csv")

data <- data %>%  
  drop_na(BorisJohnsonTrust)

# make sure the date column is considered as such
data$Week <- as.Date(data$Date_Week, format = c("%d/%m/%Y"))

# Drop rows where N less than 100. 
data <- subset(data, N > 100)

# Aggregate Weeks with Multiple data points.
### 24/02/2020 - UKC and YouGov and MiC
survey1 <- subset(data, Date_Week == '24/02/2020', select = c(N, BorisJohnsonTrust:BorisJohnsonNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'UKC Study' & data$Date_Week == '24/02/2020', 18:20] <- vec
data[data$SurveyOrg == 'UKC Study' & data$Date_Week == '24/02/2020', 5] <- 3276
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '24/02/2020', 18:20] <- NA
data[data$SurveyOrg == 'More in Common' & data$Date_Week == '24/02/2020', 18:20] <- NA

## 15th June - Nuff and YouGov
survey1 <- subset(data, Date_Week == '15/06/2020', select = c(N, BorisJohnsonTrust:BorisJohnsonNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '15/06/2020', 18:20] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '15/06/2020', 5] <- 2650
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '15/06/2020', 18:20] <- NA



# transformation of the data to be able to later create a figure with both trust and distrust on the same graph
data$prePostCummings <- 0
data$prePostCummings[data$Week > as.Date('2020-05-01')] <- 1

test <- data %>%
  select(N, Week, BorisJohnsonTrust, BorisJohnsonDistrust, prePostCummings) %>%
  gather(key = "Measure", value = "value", -Week, -N, -prePostCummings)

test$value <- as.numeric(test$value)
test$prePostCummings[test$prePostCummings == 0] <- 'Pre-Cummings Event'
test$prePostCummings[test$prePostCummings == 1] <- 'Post-Cummings Event'
test$prePostCummings <- as.factor(test$prePostCummings)
test$Measure[test$Measure == 'BorisJohnsonTrust'] <- "Trust"
test$Measure[test$Measure == 'BorisJohnsonDistrust'] <- "Distrust"

test <- drop_na(test)

# code for the figure itself


test %>%
  ggplot(aes(x=Week, y=value)) +
  geom_line(aes(color = Measure, linetype = Measure), color= "black") +
  geom_point(shape=21, color="black", aes(size=N, fill=Measure)) +
  geom_smooth(data = subset(test, prePostCummings == 'Post-Cummings Event' & Measure == 'Trust'), aes(linetype = Measure), colour = 'purple', method = "lm", formula = y ~ x, se = F) +
  geom_smooth(data = subset(test, prePostCummings == 'Post-Cummings Event' & Measure == 'Distrust'), aes(linetype = Measure), colour = 'purple', method = "lm", formula = y ~ poly(x, 2), se = F) +
  geom_smooth(data = subset(test, Measure == 'Trust'), aes(linetype = Measure), , method = "lm", formula = y ~ poly(x, 4), colour="black") +
  geom_smooth(data = subset(test, Measure == 'Distrust'), aes(linetype = Measure), , method = "lm", formula = y ~ poly(x, 2), colour="black") +
  coord_cartesian(ylim = c(0, 100), expand = TRUE, default = TRUE) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  ggtitle("Change in trust and distrust in Boris Johnson") +
  xlab(" ") +
  ylab("Percentage of respondents") +
  scale_fill_discrete(name = "Measure", labels = c("% who distrust", "% who trust")) +
  theme(plot.title = element_text(size=16),
        axis.title.y = element_text(size=14),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 12),
  ) + 
  geom_vline(xintercept = as.numeric(as.Date("2019-12-12")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-05")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-26")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-05-25")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-06-15")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-07-04")), linetype = "dashed") +
  geom_vline(xintercept = as.numeric(as.Date("2020-09-14")), linetype = "dashed") +
  annotate("label", x = as.Date("2019-12-12"), y = 100, label = "General Election", size=3.5, alpha = 0.2) +
  annotate("label", x = as.Date("2020-03-05"), y = 90, label = "First UK COVID\ndeath", size=3.5, alpha = 0.2) +
  annotate("label", x = as.Date("2020-03-26"), y = 100, label = "Lockdown starts", size=3.5) +
  annotate("label", x = as.Date("2020-06-15"), y = 100, label = "Reopening of\nEnglish retail", size=3.5, alpha = 0.2) +
  annotate("label", x = as.Date("2020-05-25")-3, y = 75, label = "Dominic Cummings\nPress Conference", size=3.5) +
  annotate("label", x = as.Date("2020-07-04")+4, y = 90, label = "Reopening of pubs\nand restaurants", size=3.5, alpha = 0.2) +
  annotate("label", x = as.Date("2020-09-14")-2, y = 100, label = "New restrictions\n(Rule of 6)", size=3.5, alpha = 0.2) 

# Fit line equations
# Trust 
test2 <- test[test$Measure=="Trust",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit4)

# Distrust 
test2 <- test[test$Measure=="Distrust",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit2)

#####################################################################################
######## Government Approval ###########################
#############################################################################
data <- read.csv("/Users/bendavies/Documents/Kent/Psychology/PhD/Nuffield/Files for Figures/AlteredBands All Surveys Split by Week csv.csv")

data <- data %>%  
  drop_na(GovApprovalPercentApprove)

# make sure the date column is considered as such
data$Week <- as.Date(data$Date_Week, format = c("%d/%m/%Y"))

# Drop rows where N less than 100. 
data <- subset(data, N > 100)



# Aggregate Weeks with Multiple data points.
### 9th March - YouGov and IPSOS
survey1 <- subset(data, Date_Week == '09/03/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '09/03/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '09/03/2020', 5] <- 2629
data[data$SurveyOrg == 'IPSOS MORI' & data$Date_Week == '09/03/2020', 12:14] <- NA

## 11th MAy - ComRes and YouGov
survey1 <- subset(data, Date_Week == '11/05/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '11/05/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '11/05/2020', 5] <- 3782
data[data$SurveyOrg == 'ComRes' & data$Date_Week == '11/05/2020', 12:14] <- NA

### 25th MAy - YouGov and SUrvation.
survey1 <- subset(data, Date_Week == '25/05/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '25/05/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '25/05/2020', 5] <- 2712
data[data$SurveyOrg == 'Survation' & data$Date_Week == '25/05/2020', 12:14] <- NA

## 1st June - Yougov and Survation
survey1 <- subset(data, Date_Week == '01/06/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '01/06/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '01/06/2020', 5] <- 2636
data[data$SurveyOrg == 'Survation' & data$Date_Week == '01/06/2020', 12:14] <- NA

### 8th June YouGov and Ipsos
survey1 <- subset(data, Date_Week == '08/06/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '08/06/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '08/06/2020', 5] <- 2725
data[data$SurveyOrg == 'IPSOS MORI' & data$Date_Week == '08/06/2020', 12:14] <- NA

### 29th June - Yougov and survation.
survey1 <- subset(data, Date_Week == '29/06/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '29/06/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '29/06/2020', 5] <- 2679
data[data$SurveyOrg == 'Survation' & data$Date_Week == '29/06/2020', 12:14] <- NA

### 6th July - YouGov and survation.
survey1 <- subset(data, Date_Week == '06/07/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '06/07/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '06/07/2020', 5] <- 3660
data[data$SurveyOrg == 'Survation' & data$Date_Week == '06/07/2020', 12:14] <- NA

### 13th July - ComRes and YouGov.
survey1 <- subset(data, Date_Week == '13/07/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '13/07/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '13/07/2020', 5] <- 3758
data[data$SurveyOrg == 'ComRes' & data$Date_Week == '13/07/2020', 12:14] <- NA

### 27th July - Ipsos yougov survation. 
survey1 <- subset(data, Date_Week == '27/07/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '27/07/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '27/07/2020', 5] <- 3689
data[data$SurveyOrg == 'Survation' & data$Date_Week == '27/07/2020', 12:14] <- NA
data[data$SurveyOrg == 'IPSOS MORI' & data$Date_Week == '27/07/2020', 12:14] <- NA

### 10th August - Comres and yougov
survey1 <- subset(data, Date_Week == '10/08/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '10/08/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '10/08/2020', 5] <- 3726
data[data$SurveyOrg == 'ComRes' & data$Date_Week == '10/08/2020', 12:14] <- NA

### 31st Aug Yougov and survation.
survey1 <- subset(data, Date_Week == '31/08/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '31/08/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '31/08/2020', 5] <- 2704
data[data$SurveyOrg == 'Survation' & data$Date_Week == '31/08/2020', 12:14] <- NA

### 14ths september - comres ipsos survation yougov.
survey1 <- subset(data, Date_Week == '14/09/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '14/09/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '14/09/2020', 5] <- 5296
data[data$SurveyOrg == 'Survation' & data$Date_Week == '14/09/2020', 12:14] <- NA
data[data$SurveyOrg == 'ComRes' & data$Date_Week == '14/09/2020', 12:14] <- NA
data[data$SurveyOrg == 'IPSOS MORI' & data$Date_Week == '14/09/2020', 12:14] <- NA

### 19th OCt YouGov and ipsos.
survey1 <- subset(data, Date_Week == '19/10/2020', select = c(N, GovApprovalPercentApprove:GovApprovalPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'YouGov' & data$Date_Week == '19/10/2020', 12:14] <- vec
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '19/10/2020', 5] <- 2672
data[data$SurveyOrg == 'IPSOS MORI' & data$Date_Week == '19/10/2020', 12:14] <- NA

# transformation of the data to be able to later create a figure with both trust and distrust on the same graph
test <- data %>%
  select(N, Week, GovApprovalPercentApprove, GovApprovalPercentDisapprove,) %>%
  gather(key = "Measure", value = "value", -Week, -N)

test$value <- as.numeric(test$value)
test$Measure[test$Measure == 'GovApprovalPercentApprove'] <- "Approve"
test$Measure[test$Measure == 'GovApprovalPercentDisapprove'] <- "Disapprove"

test <- drop_na(test)

# code for the figure itself


test %>%
  ggplot(aes(x=Week, y=value)) +
  geom_line(aes(color = Measure, linetype = Measure), color= "black") +
  geom_point(shape=21, color="black", aes(size=N, fill=Measure)) +
  geom_smooth(aes(linetype = Measure), colour="black") +
  coord_cartesian(ylim = c(0, 100), expand = TRUE, default = TRUE) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  ggtitle("Change in Government approval and disapproval") +
  xlab(" ") +
  ylab("Percentage of respondents") +
  scale_fill_discrete(name = "Measure", labels = c("% who approve", "% who disapprove")) +
  theme(plot.title = element_text(size=16),
        axis.title.y = element_text(size=14),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 12),
  ) + 
  geom_vline(xintercept = as.numeric(as.Date("2019-12-12")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-05")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-26")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-05-25")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-06-15")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-07-04")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-09-14")), linetype = "solid") +
  annotate("label", x = as.Date("2019-12-12"), y = 100, label = "General Election", size=3.5) +
  annotate("label", x = as.Date("2020-03-05")-2, y = 90, label = "First UK COVID\ndeath", size=3.5) +
  annotate("label", x = as.Date("2020-03-26")+2, y = 100, label = "Lockdown starts", size=3.5) +
  annotate("label", x = as.Date("2020-06-15")-1, y = 100, label = "Reopening of\nEnglish retail", size=3.5) +
  annotate("label", x = as.Date("2020-05-25")-6, y = 75, label = "Dominic Cummings\nPress Conference", size=3.5) +
  annotate("label", x = as.Date("2020-07-04")+8, y = 90, label = "Reopening of pubs\nand restaurants", size=3.5) +
  annotate("label", x = as.Date("2020-09-14")-2, y = 100, label = "New restrictions\n(Rule of 6)", size=3.5) 

# Fit line equations
test2 <- test[test$Measure=="Disapprove",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit3)
anova(fit2, fit3)
anova(fit3, fit4)


#############################################################################################
############### Community Belonging #############################################
#################################################################################
data <- read.csv("/Users/bendavies/Documents/Kent/Psychology/PhD/Nuffield/Files for Figures/AlteredBands All Surveys Split by Week csv.csv")

data <- data %>%  
  drop_na(CommunityConnectionPercentConnected)

# make sure the date column is considered as such
data$Week <- as.Date(data$Date_Week, format = c("%d/%m/%Y"))

# Drop rows where N less than 100. 
data <- subset(data, N > 100)

# Aggregate Weeks with Multiple data points.
### 24/02/2020 - UKC and YouGov
survey1 <- subset(data, Date_Week == '24/02/2020', select = c(N, BorisJohnsonTrust:BorisJohnsonNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'UKC Study' & data$Date_Week == '24/02/2020', 18:20] <- vec
data[data$SurveyOrg == 'UKC Study' & data$Date_Week == '24/02/2020', 5] <- 1762
data[data$SurveyOrg == 'YouGov' & data$Date_Week == '24/02/2020', 18:20] <- NA

## 22nd June - Nuff and UnderSoc
survey1 <- subset(data, Date_Week == '22/06/2020', select = c(N, CommunityConnectionPercentConnected:CommunityConnectionPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '22/06/2020', 15:17] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '22/06/2020', 5] <- 11690
data[data$SurveyOrg == 'Understanding Society' & data$Date_Week == '22/06/2020', 15:17] <- NA

### 29th June - Nuff and UnderSoc
survey1 <- subset(data, Date_Week == '29/06/2020', select = c(N, CommunityConnectionPercentConnected:CommunityConnectionPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '29/06/2020', 15:17] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '29/06/2020', 5] <- 2860
data[data$SurveyOrg == 'Understanding Society' & data$Date_Week == '29/06/2020', 15:17] <- NA

### 24th August - Nuff and social fabric
survey1 <- subset(data, Date_Week == '24/08/2020', select = c(N, CommunityConnectionPercentConnected:CommunityConnectionPercentNeutral))
survey1 <- drop_na(survey1)
survey1[,] <- lapply(survey1, function(x) as.numeric(x))

vec <- character()
for (i in 2:ncol(survey1)){
  xm <- weighted.mean(survey1[,i], survey1$N)
  vec <- append(vec, xm)
}

data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '24/08/2020', 15:17] <- vec
data[data$SurveyOrg == 'Social Cohesion in the Context of COVID-19 (Nuffield)' & data$Date_Week == '24/08/2020', 5] <- 1991
data[data$SurveyOrg == 'Social Fabric' & data$Date_Week == '24/08/2020', 15:17] <- NA

# transformation of the data to be able to later create a figure with both trust and distrust on the same graph
test <- data %>%
  select(N, Week, CommunityConnectionPercentConnected, CommunityConnectionPercentDisconnect) %>%
  gather(key = "Measure", value = "value", -Week, -N)

test$value <- as.numeric(test$value)
test$Measure[test$Measure == 'CommunityConnectionPercentConnected'] <- "B_Connected"
test$Measure[test$Measure == 'CommunityConnectionPercentDisconnect'] <- "A_Disconnected"

test <- drop_na(test)

# code for the figure itself


test %>%
  ggplot(aes(x=Week, y=value)) +
  geom_line(aes(color = Measure, linetype = Measure), color= "black") +
  geom_point(shape=21, color="black", aes(size=N, fill=Measure)) +
  geom_smooth(aes(linetype = Measure), colour="black") +
  coord_cartesian(ylim = c(0, 100), expand = TRUE, default = TRUE) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  ggtitle("Change in feelings of connection and disconnection from local communities") +
  xlab(" ") +
  ylab("Percentage of respondents") +
  scale_fill_discrete(name = "Measure", labels = c("% who feel disconnected", "% who feel connected")) +
  theme(plot.title = element_text(size=16),
        axis.title.y = element_text(size=14),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 12),
  ) + 
  geom_vline(xintercept = as.numeric(as.Date("2020-03-05")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-26")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-05-25")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-06-15")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-07-04")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-09-14")), linetype = "solid") +
  annotate("text", x = as.Date("2020-02-01")+5, y = 100, label = " ", size=3.5) +
  annotate("label", x = as.Date("2020-03-05"), y = 90, label = "First UK COVID\ndeath", size=3.5) +
  annotate("label", x = as.Date("2020-03-26"), y = 100, label = "Lockdown starts", size=3.5) +
  annotate("label", x = as.Date("2020-06-15"), y = 100, label = "Reopening of\nEnglish retail", size=3.5) +
  annotate("label", x = as.Date("2020-05-25")-3, y = 75, label = "Dominic Cummings\nPress Conference", size=3.5) +
  annotate("label", x = as.Date("2020-07-04")+4, y = 90, label = "Reopening of pubs\nand restaurants", size=3.5) +
  annotate("label", x = as.Date("2020-09-14")-2, y = 100, label = "New restrictions\n(Rule of 6)", size=3.5) 

# Fit line equations
test2 <- test[test$Measure=="Disconnected",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit4)
anova(fit2, fit4)
anova(fit3, fit4)
anova(fit1, fit2)

########################### UK and Local Division ##############################################
data <- read.csv("/Users/bendavies/Documents/Kent/Psychology/PhD/Nuffield/Files for Figures/AlteredBands All Surveys Split by Week csv.csv")

data <- data %>%  
  drop_na(UKDivided)

# make sure the date column is considered as such
data$Week <- as.Date(data$Date_Week, format = c("%d/%m/%Y"))

# Drop rows where N less than 100. 
data <- subset(data, N > 100)

# transformation of the data to be able to later create a figure with both trust and distrust on the same graph
test <- data %>%
  select(N, Week, UKDivided, UKUnited, LocalDivision, LocalUnited) %>%
  gather(key = "Measure", value = "value", -Week, -N)


test$value <- as.numeric(test$value)
test$Measure[test$Measure == 'UKDivided'] <- "Feel UK is more divided"
test$Measure[test$Measure == 'UKUnited'] <- "Feel UK is more united"
test$Measure[test$Measure == 'LocalDivision'] <- "Feel local area is more divided"
test$Measure[test$Measure == 'LocalUnited'] <- "Feel local area is more united"

test <- drop_na(test)


# code for the figure itself


test %>%
  ggplot(aes(x=Week, y=value)) +
  geom_line(aes(color = Measure, linetype = Measure), color= "black") +
  geom_point(shape=21, color="black", aes(size=N, fill=Measure)) +
  geom_smooth(aes(linetype = Measure, color = Measure)) +
  coord_cartesian(ylim = c(0, 100), expand = TRUE, default = TRUE) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  ggtitle("Change in feelings of division and unity among the UK and local communities") +
  xlab(" ") +
  ylab("Percentage of respondents") +
  scale_fill_discrete(name = "Measure", labels = c("% who feel local area is more divided", "% who feel local area is more united", "% who feel UK is more divided", 
                                                   "% who feel UK is more united")) +
  theme(plot.title = element_text(size=16),
        axis.title.y = element_text(size=14),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 12),
  ) + 
  geom_vline(xintercept = as.numeric(as.Date("2019-12-12")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-05")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-03-26")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-05-25")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-06-15")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-07-04")), linetype = "solid") +
  geom_vline(xintercept = as.numeric(as.Date("2020-09-14")), linetype = "solid") +
  annotate("label", x = as.Date("2019-12-12"), y = 100, label = "General Election", size=3.5) +
  annotate("label", x = as.Date("2020-03-05")-2, y = 90, label = "First UK COVID\ndeath", size=3.5) +
  annotate("label", x = as.Date("2020-03-26")+2, y = 100, label = "Lockdown starts", size=3.5) +
  annotate("label", x = as.Date("2020-06-15")-1, y = 100, label = "Reopening of\nEnglish retail", size=3.5) +
  annotate("label", x = as.Date("2020-05-25")-6, y = 75, label = "Dominic Cummings\nPress Conference", size=3.5) +
  annotate("label", x = as.Date("2020-07-04")+7, y = 90, label = "Reopening of pubs\nand restaurants", size=3.5) +
  annotate("label", x = as.Date("2020-09-14")-4, y = 100, label = "New restrictions\n(Rule of 6)", size=3.5) 

# Fit line equations
test2 <- test[test$Measure=="Feel UK is more united",]
test2 <- test2[test2$Week > '2020-05-01',]

fit1 <- lm(value ~ poly(Week, 1), data=test2)  # Linear
fit2 <- lm(value ~ poly(Week, 2), data=test2)  # Quadratic
fit3 <- lm(value ~ poly(Week, 3), data=test2) ## Cubic
fit4 <- lm(value ~ poly(Week, 4), data=test2) ## Quartic

summary(fit1)
summary(fit2)
summary(fit3)
summary(fit4)

anova(fit1, fit4)
anova(fit2, fit4)
anova(fit3, fit4)
anova(fit1, fit3)
