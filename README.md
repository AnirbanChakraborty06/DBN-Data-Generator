# DBN-Data-Generator
A synthetic data generator based on Dynamic Bayesian Networks, apt for generating multivariate timeseries data.

# 1. Motivation
The motivation of this project comes from a series of real-world scenarios commonplace in Data Science domain. The scenarios are explained in a step-by-step manner.

## 1.1. A relatable scenario in ML-based enterprises
**_ML ABC_** is an enterprise that provides ML-based solutions like _Forecasting_, _Price Recommendation_, _Promotion Optimization_ etc. to businesses across industries like CPG, Retail, Healthcare, Energy etc. Below is a conversation that happens between development teams from **_ML ABC_** and the client.

![Image depicting a A Common Conversation Between Clients And Solution Providers](artifacts/images/A_Common_Conversation_Between_Clients_And_Solution_Providers.png)

<ins>**Does this scenario look familiar?**</ins> Let’s dive deeper into the source of such embarrassing scenarios.

## 1.2. What is it that ML ABC truly aim to build?
When organisations like **_ML ABC_** aim to build a solution like Promotion Optimization, they expect the solution to work across multiple industries – CPG, Healthcare, Energy etc. Or if they build it for a particular industry, like CPG, they expect it to perform across multiple businesses within CPG domain.

That is, <ins>**they want to build solutions that have generalizability across domains, or across businesses within a domain**</ins>.

## 1.3. Developing generizability requires extensive testing

![Image depicting variation across domains in data characteristics](artifacts/images/Variations_Across_Industries.png)

- CPG is relatively smooth with promotions and discounts being the driving factors.
- Healthcare has a slower adoption rate for newer products.
- Energy sector shows heavy shocks based on global events and supply issues.

<ins>**Solution strategies that aim to generalize across such variations must be tested over these variations first**</ins>.

## 1.4. Synthetic data generators create the necessary ecosystem.
Say, we have a synthetic data generator that incorporates CPG process dynamics as part of the generation process. <ins>**If an ML strategy, without a peek into the actual data generation process, can discover the patterns with good accuracy, it indeed is a sound strategy for CPG industry in general**</ins>.

Note, it is relatively easy to specify the characteristics of the process dynamics of an industry. Retrieving insights from the data generated out of a process is the harder bit. Hence, building a synthetic data generator that has CPG characteristics is possible with subject matter expertise.
