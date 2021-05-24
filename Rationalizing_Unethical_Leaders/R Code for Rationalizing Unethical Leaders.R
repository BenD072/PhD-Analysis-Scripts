### Libraries
library(hrbrthemes)
library(tidyverse)
library(tidyr)
library(ggpubr)
library(rstatix)
library(car)
library(psych)
library(nFactors)
library(lavaan)
library(Hmisc)
library(plyr)
library(relaimpo)

FILE_NAME = ''

data <- read.csv(FILE_NAME)


# Hypothesis 5 - Change in prototypicality, group-serving, and charisma over time will correlate with change in perception of unethicalness over time

###### Correlations WITH controlling for riot ########
# Can't include control variables with rmcorr, so need to manually obtain the residuals by first running regression. Correlating the residuals from regression models between
# X1 and X2/X3 (the control variables) and Y and X2/X3 is statistically the same as running a partial correlation. For example, to run a partial correlation between group Serve (X1)
# and FalseInformationEthicsScore (Y) controlling for riotEthicsScore (X2), would need the residuals from regressions between group serve and riot, and from falseinfoethics and riot.

# Get the residuals and add to dataframe
df <- dplyr::select(data, GSUSA, ProtoUSA, TmpFalseEthicsScoreW1, TmpNepEthicsScoreW1, TmpPowEthicsScoreW1, GSUSAW3, ProtoUSW3, FalseEthicsScoreW3,
                    NepEthicsScoreW3, PowerEthicsScoreW3, RiotEthicsScoreW3, TmpRiotChangeW3)

df <- drop_na(df)

# Group Serve Measures
m1 <- lm(GSUSA ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)  # X1 and X2/X3
m2 <- lm(GSUSAW3 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)
df$GSW1Resid <- residuals(m1)
df$GSW3Resid <- residuals(m2)

# Prototypicality Measures 
m1 <- lm(ProtoUSA ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)  # X1 and X2/X3
m2 <- lm(ProtoUSW3 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)
df$ProtW1Resid <- residuals(m1)
df$ProtW3Resid <- residuals(m2)

# False Information
m1 <- lm(TmpFalseEthicsScoreW1 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)  # Y and X2/X3
m2 <- lm(FalseEthicsScoreW3 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)
df$FalseW1Resid <- residuals(m1)
df$FalseW3Resid <- residuals(m2)

# Nepotism 
m1 <- lm(TmpNepEthicsScoreW1 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)  # Y and X2/X3
m2 <- lm(NepEthicsScoreW3 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)
df$NepotismW1Resid <- residuals(m1)
df$NeptosmW3Resid <- residuals(m2)

# Abuse of Power 
m1 <- lm(TmpPowEthicsScoreW1 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)  # Y and X2/X3
m2 <- lm(PowerEthicsScoreW3 ~ TmpRiotChangeW3 + RiotEthicsScoreW3, data=df)
df$PowerW1Resid <- residuals(m1)
df$PowerW3Resid <- residuals(m2)

# Run the RMCorr Analysis using residuals
df <- tibble::rowid_to_column(df, "ID")
df$ID <- factor(df$ID)  # Make sure ID is a factor
df_long_gs <- df %>% 
  gather(key = "Measure", value = "GS", c(GSW1Resid, GSW3Resid))

df_long_proto <- df %>% 
  gather(key="Measure", value = "proto", c(ProtW1Resid, ProtW3Resid))

df_long_falseinfo <- df %>% 
  gather(key="Measure", value="FalseInfo", c(FalseW1Resid, FalseW3Resid))

df_long_nepotism <- df %>% 
  gather(key="Measure", value="Nepotism", c(NepotismW1Resid, NeptosmW3Resid))

df_long_power <- df %>% 
  gather(key="Measure", value="Power", c(PowerW1Resid, PowerW3Resid))

df_long <- dplyr::select(df_long_gs, ID, Measure, GS)
df_long$Proto <- df_long_proto$proto
df_long$FalseInfo <- df_long_falseinfo$FalseInfo
df_long$Nepotism <- df_long_nepotism$Nepotism
df_long$power <- df_long_power$Power

library(rmcorr)

# False info correlations 
rmcorr(ID, GS, FalseInfo, df_long)
rmcorr(ID, Proto, FalseInfo, df_long)


# Nepotism 
rmcorr(ID, GS, Nepotism, df_long)
rmcorr(ID, Proto, Nepotism, df_long)

# Abuse of Power 
rmcorr(ID, GS, power, df_long)
rmcorr(ID, Proto, power, df_long)

# Intercorrelations 
rmcorr(ID, GS, Proto, df_long)
rmcorr(ID, Nepotism, FalseInfo, df_long)
rmcorr(ID, power, FalseInfo, df_long)
rmcorr(ID, Nepotism, power, df_long)

# Demonstrating that partial correlation and correlating residuals provide the same coefficient 
library(ppcor)
pcor.test(df$GSUSA, df$FalseEthicsScoreW3, df[,c("TmpRiotChangeW3","RiotEthicsScoreW3")])  # Partial
cor.test(df$GSW1Resid, df$FalseW3Resid, method = "pearson")  # Residual - both give same reuslt (slightly different p and t values however)


###### Cross Lagged Model #######

model <- '
GSUSAW3 ~ GSUSA + TmpFalseEthicsScoreW1 + TmpNepEthicsScoreW1 + RiotEthicsScoreW3 + TmpRiotChangeW3
FalseEthicsScoreW3 ~ TmpFalseEthicsScoreW1 + GSUSA + RiotEthicsScoreW3 + TmpRiotChangeW3 
NepEthicsScoreW3 ~ TmpNepEthicsScoreW1 + GSUSA + RiotEthicsScoreW3 + TmpRiotChangeW3 

# Controls for riot influence 

GSUSA ~ RiotEthicsScoreW3 + TmpRiotChangeW3
TmpFalseEthicsScoreW1 ~ RiotEthicsScoreW3 + TmpRiotChangeW3
TmpNepEthicsScoreW1 ~ RiotEthicsScoreW3 + TmpRiotChangeW3

# Correlations 
TmpFalseEthicsScoreW1 ~~ TmpNepEthicsScoreW1
FalseEthicsScoreW3 ~~ NepEthicsScoreW3

'

fit <- sem(model, data = data)
summary(fit, fit.measures = TRUE)

