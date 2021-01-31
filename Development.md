# Model and Analysis for this viral campaign

**Base:** **Directed** **graph** of the Instagram network, blue nodes represent the users and the grey arcs represent the following links (from “followed” to “following”).

**Objective**: ensure the success and the virality of this campaign, make it reach as many people as possible. 

## **1. Overall Approach**:

1. Measure **final score** of influence of each users  
2. Find the **most influential users** (TOP-5)
3. simulating a propagation with the independent cascade model where the initial infected nodes are the most influential users
4. Compared most influential users cascade model with randomly selected users cascade model (i.e. model where the initial infected users are randomly selected)

## **2. KPIs**

- **Visibility(t)** = total number of views on posts published up to time t 
- **Engagement(t)** = total number of likes and comments on posts published up to time t 
- **Virality(t)** = total number of reposts of posts published up to time t 

## **3. Final Scores of Influences**

Every campaign needs engagement to survive and thrive, and the reaction of users are essential, then we measure the engagement and reaction of this campaign.

For the measure of influences between users, we will use the betweenness centrality. It shows which nodes are ‘bridges’ between nodes and is the most useful for finding the individuals who influence the flow around the network and are essential to transmit information. 

Above all, we could analysis the graph based on 3 indexs:

- Betweeness centrality index
- **Engagement** **index**: based on views, likes, comments, reposts on posts made by the user
- **Reaction** **index**: based on link clicks, donations and house purchase attempts

### (1) Engagement index

 The first level of engagement is measured as follows 

![engagement_index](https://raw.githubusercontent.com/ViralMarketing/ViralMarketing/88e69f12699fb7987c5737a44b8683fee8f00a33/assets/svg/engagement_index.svg?token=AK3FBFH53DMSPF4U3OIWRY3ACZUGE)

<u>A good influencer is not only someone who writes posts generating engagement, his posts must also inspire others into writing engaging posts.</u>

![engagement_total](https://raw.githubusercontent.com/ViralMarketing/ViralMarketing/88e69f12699fb7987c5737a44b8683fee8f00a33/assets/svg/engagement_total.svg?token=AK3FBFE4JH66BHEBUXERINDACZUFE)

Engagement Value = *P*(0) + 0.1*P*(1) + 0.01*P*(2) + …
Where P(n) refers to the engagement values from the n-th time reposts (repost of order n). 
When there is a repost, we add the parameter 0.1 𝑛 

### (2) Reaction index

As for the Reaction index, we consider the behavior of clicking page links, donations and buying house.  

- 𝑅𝑒𝑎𝑐𝑡𝑖𝑜𝑛 𝑣𝑎𝑙𝑢𝑒 = 0  if the post does not generate any link clicks 
- 𝑅𝑒𝑎𝑐𝑡𝑖𝑜𝑛 𝑣𝑎𝑙𝑢𝑒 = 1  if the post generates link clicks but no other reactions link clicks 
- 𝑅𝑒𝑎𝑐𝑡𝑖𝑜𝑛 𝑣𝑎𝑙𝑢𝑒 = 1 + 2 + 10 × ln (𝑁/10 + 1) if the post generates donations and N is the donation value 

Behavior of **clicking** and **donations** show their interests of the campaign, so we give them the value with 1 and 2. And the donations can be regarded as some bonus points, which is independent with the behavior of donations. 

### (3) Final Score Index

Finally, we can measure the **Influence index** of a node: 

![finalZ_total_score](https://raw.githubusercontent.com/ViralMarketing/ViralMarketing/88e69f12699fb7987c5737a44b8683fee8f00a33/assets/svg/total_score.svg?token=AK3FBFFMNKLYESIUECFLWVDACZUHS)

### 4. Propagation simulation

1. Pick 5 most infleuntial candidates with the highest scores as the initial cascade to propagate

2. In one propagating iteration, each newly infected user could infected its followers with a specfic probability  (i.e infection rate)

3. After this iteration, users who already influence others won’t be considered in the whole propagation.

4. Consider the newly infected users, go to 2

   The iterations starts at 09/11 and ends at 16/11, totally 7 days.

### (1) Influence probability  (i.e infection rate)

We use this as their absolute ability to infect their followers. Where reposts refer to the patients infected successfully, and likes refer to the intimate contact. 

![absolutely ability](https://raw.githubusercontent.com/ViralMarketing/ViralMarketing/88e69f12699fb7987c5737a44b8683fee8f00a33/assets/svg/abs_ability.svg?token=AK3FBFE7YJHMEUZP5Z4JJMTACZUKW)

As for their relative propagation ability, we use the last two elements calculated in the score. 

![relative ability](https://raw.githubusercontent.com/ViralMarketing/ViralMarketing/88e69f12699fb7987c5737a44b8683fee8f00a33/assets/svg/re_ability.svg?token=AK3FBFHY2H6MA5EB2SFATPTACZUNO)

So, their real probability to infect their followers is: 

![real probability](https://raw.githubusercontent.com/ViralMarketing/ViralMarketing/88e69f12699fb7987c5737a44b8683fee8f00a33/assets/svg/probabbility.svg?token=AK3FBFARZVKTLNWIG7LIWPTACZUOS)

### (2) Comparative Experiment

Next, we compare the infecting numbers of our 5 best candidates with 5 randomly selected users, in our directed graph, to verify if our score could be used to measure the influence of each user. 

