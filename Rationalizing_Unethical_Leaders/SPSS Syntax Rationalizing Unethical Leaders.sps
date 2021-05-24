* Encoding: UTF-8.

/* Preliminary Analysis - Test for differences between each unethical behaviour and if new behaviours change perceptions of Trump. /*
    
GLM FalseEthicsScoreW1 NepEthicsScoreW1 PowerEthicsScoreW1
  /WSFACTOR=Behavior 3 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Behavior) COMPARE ADJ(BONFERRONI)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Behavior.

GLM TmpFalseEthicsScoreW1 TmpNepEthicsScoreW1 TmpPowEthicsScoreW1
  /WSFACTOR=Behavior 3 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Behavior) COMPARE ADJ(BONFERRONI)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Behavior.


T-TEST
  /TESTVAL=4
  /MISSING=ANALYSIS
  /VARIABLES=TmpPardChangeW3 TmpConcedeChangeW3 TmpOverturnChangeW3 TmpRiotChangeW3
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).


GLM FalseEthicsScoreW3 NepEthicsScoreW3 PowerEthicsScoreW3 RiotEthicsScoreW3
  /WSFACTOR=Behavior 4 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Behavior) COMPARE ADJ(BONFERRONI)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Behavior.

/* Hypothesis 1 - Repeated Measures ANOVA to test for difference between neutral transgression condition and Trump transgression condition.

GLM FalseEthicsScoreW1 TmpFalseEthicsScoreW1
  /WSFACTOR=Target 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Target) 
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Target.

GLM NepEthicsScoreW1 TmpNepEthicsScoreW1
  /WSFACTOR=Target 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Target) 
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Target.

GLM PowerEthicsScoreW1 TmpPowEthicsScoreW1
  /WSFACTOR=Target 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Target) 
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Target.

/* Hypothesis 2 - Regression predicting Trump transgression at Wave 2 from Identity Advancement, Prototypicality, and neutral transgression score /*
    
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN 
  /DEPENDENT TmpFalseEthicsScoreW1
  /METHOD=ENTER GSUSA ProtoUSA FalseEthicsScoreW1.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN 
  /DEPENDENT TmpNepEthicsScoreW1
  /METHOD=ENTER GSUSA ProtoUSA NepEthicsScoreW1.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN 
  /DEPENDENT TmpPowEthicsScoreW1
  /METHOD=ENTER GSUSA ProtoUSA PowerEthicsScoreW1.


/* Hypothesis 3 - ANCOVA to test for change in perceptions of unethicalness from pre to post leadership exit /*
    
GLM TmpFalseEthicsScoreW1 FalseEthicsScoreW3 WITH TmpRiotChangeW3 RiotEthicsScoreW3
  /WSFACTOR=Time 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Time) WITH(TmpRiotChangeW3=MEAN RiotEthicsScoreW3=MEAN)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Time 
  /DESIGN=TmpRiotChangeW3 RiotEthicsScoreW3.



GLM TmpNepEthicsScoreW1 NepEthicsScoreW3 WITH TmpRiotChangeW3 RiotEthicsScoreW3
  /WSFACTOR=Time 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Time) WITH(TmpRiotChangeW3=MEAN RiotEthicsScoreW3=MEAN)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Time 
  /DESIGN=TmpRiotChangeW3 RiotEthicsScoreW3.


GLM TmpPowEthicsScoreW1 PowerEthicsScoreW3 WITH TmpRiotChangeW3 RiotEthicsScoreW3
  /WSFACTOR=Time 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Time) WITH(TmpRiotChangeW3=MEAN RiotEthicsScoreW3=MEAN)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Time 
  /DESIGN=TmpRiotChangeW3 RiotEthicsScoreW3.

/* Hypothesis 4 - ANCOVA to test for change in perceptions of idenitty advancement and prototypicality from pre to post leadership exit /*
    

GLM GSUSA GSUSAW3 WITH TmpRiotChangeW3 RiotEthicsScoreW3
  /WSFACTOR=Time 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Time) WITH(TmpRiotChangeW3=MEAN RiotEthicsScoreW3=MEAN)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Time 
  /DESIGN=TmpRiotChangeW3 RiotEthicsScoreW3.



GLM ProtoUSA ProtoUSW3 WITH TmpRiotChangeW3 RiotEthicsScoreW3
  /WSFACTOR=Time 2 Polynomial 
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Time) WITH(TmpRiotChangeW3=MEAN RiotEthicsScoreW3=MEAN)
  /PRINT=ETASQ 
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=Time 
  /DESIGN=TmpRiotChangeW3 RiotEthicsScoreW3.


/* Hypothesis 5 was address in R - please see R script file /*
