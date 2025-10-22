**Principal Component Analysis (PCA)**  

PCA is a widely used statistical technique for dimensionality reduction.  
It transforms the original set of correlated features into a smaller number of uncorrelated components, while preserving as much variance in the data as possible.  
In this study, PCA was applied once to the full set of 64 standardized LIWC dimensions (zero mean, unit variance).  
This global fitting ensured that the same latent components (and their corresponding feature loadings) were used consistently across all group comparisons, making results directly comparable.  
Consequently, the component loadings and the proportion of variance explained by each component are identical for every comparison.

The first five principal components were extracted, together explaining a substantial proportion of the variance in participants’ linguistic profiles (**Table 1**).  
For each participant, PCA yielded scores along these components, which were then used for group comparisons.  
To evaluate whether the PCs themselves differentiated between groups, we performed Welch’s *t*-tests on the scores of each of the first five PCs.  
Since five separate tests were conducted, we applied the FDR correction to control for false positives.  
The results of this procedure provide the percentage of variance explained by each PC (PC1–PC5), as well as the *t*-statistics, raw *p*-values, and FDR-adjusted *q*-values for group comparisons.

**Table 2** presents the top contributing LIWC dimensions for PC1, which explained the largest share of variance.  
The loadings indicate how strongly each category correlates with the component, where higher absolute values mean that variation in that category contributes more to PC1.  
In this case, PC1 is dominated by function words (particularly pronouns), cognitive mechanism terms, and social process words, suggesting it captures a broad structural–cognitive dimension of language use.

| **PC** | **Explained Variance (%)** |
|:-------|:---------------------------:|
| PC1 | 14.9% |
| PC2 | 8.1% |
| PC3 | 6.9% |
| PC4 | 6.2% |
| PC5 | 5.3% |
| **Total** | **41.4%** |

#### Table 1. Explained Variance of PC1–PC5



| **Dimension** | **Loading** |
|:--------------|:-----------:|
| ipron   | 0.275 |
| funct   | 0.274 |
| pronoun | 0.274 |
| nonfl   | 0.241 |
| shehe   | 0.238 |
| article | 0.237 |
| social  | 0.230 |
| you     | 0.224 |
| ppron   | 0.221 |
| cogmech | 0.220 |

#### Table 2. Top 10 Feature Loadings on PC1

---
**ℓ₁-Regularized Logistic Regression**  

Logistic regression is a supervised learning method that models the probability of group membership as a function of predictor variables.  
In this study, the predictors are standardized LIWC category proportions, and the response variable indicates group assignment.  
To address the high dimensionality and correlations among predictors, we applied ℓ₁ regularization (Lasso penalty), which shrinks coefficients to zero and thus selects a subset of the most informative features.

Regularization strength ($C$) was tuned within a `Pipeline` to avoid data leakage (scaling inside CV folds) using:

```python
LogisticRegressionCV(
    solver='saga',
    scoring='roc_auc',
    class_weight='balanced',
    Cs=np.logspace(-4, 4, 20),
    cv=5
)
```
If any class contained fewer than five samples, inner cross-validation used three folds.
Since the focus of this study is interpretability rather than classification, we report selected features and coefficients, while predictive performance is presented only as a safeguard against overfitting.
While univariate analyses test each dimension separately and PCA captures latent structures, logistic regression identifies the categories most influential when considered jointly.

To account for sample sensitivity in modest N, we conducted stratified bootstrapping (100 resamples), recording for each LIWC category its:

- **Selection proportion**: frequency of non-zero coefficients
- **Mean coefficient**: average non-zero value
- **Sign consistency**: proportion of non-zero coefficients with the same sign

Features that are both frequently selected and sign-consistent are considered the most reliable.
All coefficients are interpreted as associations rather than causal effects.