**Welch's t-test**  
Welch’s *t*-test was used to assess mean differences in LIWC scores. Unlike the standard *t*-test, it does not assume equal variances, making it more appropriate for our unbalanced group sizes. We used `scipy` to compute the *t*-statistic and *p*-value.

The test statistic is defined as:

$$
t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\tfrac{s_1^2}{n_1} + \tfrac{s_2^2}{n_2}}}
$$

Here, $\bar{X}_i$ is the group mean, $s_i^2$ the variance, and $n_i$ the sample size for group *i*.  
The numerator captures the mean difference, while the denominator adjusts for unequal variances and sample sizes, yielding a standardized effect.  
The resulting *p*-value quantifies the probability of observing such a difference under the null hypothesis of no group difference.  
Welch’s *t*-test enables the identification of specific LIWC categories where women with ADHD might differ significantly from other groups.

---

**Benjamini–Hochberg FDR**  
With 64 LIWC categories tested, multiple comparisons increase the chance of false positives: if each test is run at $\alpha = 0.05$, then by chance alone about $0.05 \times 64 = 3.2$ dimensions could appear significant even if no true effect exists.  
We therefore applied the Benjamini–Hochberg FDR correction, implemented via `statsmodels`.

In this procedure, ranked *p*-values $p_{(1)}, \dots, p_{(m)}$ are compared against:

$$
p_{(k)} \leq \frac{k}{m}\alpha
$$

where *m* is the number of tests. The largest *k* satisfying this condition defines the rejection threshold.  
Intuitively, the method scales significance cutoffs to the number and rank of tests, ensuring that, on average, no more than $\alpha$ of declared discoveries are false positives.  
The corrected *p*-values are reported as *q*-values.

---

**JZS Bayes Factors ($\mathrm{BF}_{10}$)**  
To complement frequentist tests, we incorporated Bayesian inference using JZS Bayes Factors, implemented with `pingouin`.

Bayesian inference, grounded in Bayes’ theorem, quantifies how much more likely the observed data are under the alternative hypothesis ($H_{1}$: group difference exists) than under the null ($H_{0}$: no difference).  
The Bayes Factor is defined as:

$$
\mathrm{BF}_{10} = 
\frac{ 
\int_0^\infty (1 + N g r^2)^{-1/2} 
\left(1 + \frac{t^2}{\nu(1 + N g r^2)}\right)^{-(\nu+1)/2} 
(2\pi)^{-1/2} g^{-3/2} e^{-1/(2g)} \, dg 
}{
\left(1 + \frac{t^2}{\nu}\right)^{-(\nu+1)/2}
}
$$

where *t* is the test statistic, $\nu$ the degrees of freedom, *N* the sample size, and *g* the scale parameter.  
$\mathrm{BF}_{10} > 1$ supports $H_{1}$, while values $< 1$ support $H_{0}$.  

According to Jeffreys’ scale:  
- 1–3 → weak evidence  
- 3–10 → moderate  
- 10–30 → strong  
- 30–100 → very strong  
- &gt;100 → extreme evidence  

For example, $\mathrm{BF}_{10} = 10$ indicates that the data are 10 times more likely under $H_{1}$ than under $H_{0}$.  
Bayes Factors are widely used in psychology and linguistics because they provide a graded measure of evidence rather than a binary outcome.  
They are particularly valuable for small or unbalanced samples, where *p*-values can be unstable.  
In this study, they complemented Welch’s *t*-tests by clarifying the strength of evidence for group differences in LIWC dimensions, especially when *p*-values were marginal.

---

**Cohen’s d**  
Cohen’s *d* is a standardized measure of effect size that quantifies the magnitude of group differences independently of sample size.  
Unlike *p*-values, which only indicate statistical significance, effect sizes capture practical importance. It is defined as:

$$
d = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{ \frac{(n_1 - 1) s_1^2 + (n_2 - 1) s_2^2}{n_1 + n_2 - 2}}}
$$

where $\bar{X}_1, \bar{X}_2$ are group means, $s_1, s_2$ the standard deviations, and $n_1, n_2$ the group sizes.  
Intuitively, *d* expresses the mean difference in units of pooled standard deviation (e.g., *d* = 0.5 means the groups differ by half a standard deviation).  
Conventional benchmarks classify $|d|>0.2$ as small, $|d|>0.5$ as medium, and $|d|>0.8$ as large [Holmes, 2023].  

To assess stability, we computed 95% confidence intervals (CIs) for *d* via nonparametric bootstrapping with 2000 resamples.  
Cohen’s *d* is widely used in psychology, linguistics, and related fields because it allows comparison across studies regardless of scale or sample size.  
In our context, it was especially important given group imbalances and small ADHD subsamples, where *p*-values may be unstable.  
Whereas Bayes Factors ($\mathrm{BF}_{10}$) quantify the strength of evidence for or against a group difference, Cohen’s *d* indicates the magnitude of that difference; together they provide complementary perspectives on both the reliability and the practical importance of effects.

---

**Power Analysis**  
A post-hoc power analysis was conducted with `statsmodels` to estimate the minimum sample size required for each LIWC dimension, based on the observed effect sizes from each comparison, assuming 80% power at $\alpha = 0.05$.  
For a 2-sample *t*-test, the per-group sample size is given by:

$$
n = \frac{2}{d^2}\, f(\alpha, \text{power})
$$

where *d* is Cohen’s effect size and $f(\alpha, \text{power})$ is determined from the critical *t*-value and the noncentral *t* distribution.  
This approach yields a dimension-specific estimate of how many participants would be required to detect each effect with adequate power.
