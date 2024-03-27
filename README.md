# PageRank

Early attempts to organize the web relied on human curation/categorization.
However, the web grew far too quickly for this to remain effective.

Now, we use the idea of "web search"
- Information retrieval: find relevant document from large set of documents

Tradition information retrieval did not have the same issues as the web though.
The web presents unique challenges, such as spam, untrusted documents, etc.

2 big challenges of web search:

1. With so many sources of information, who can you trust?
    - The trick: trustworthy pages may point to one another
2. What is the "best" answer to a query such as "newspaper"
    - No single right answer
    - The trick: pages that know about newspapers might all be pointing to many newspapers

## Model

First, let's model the web as a directed graph:
- Nodes: webpages
- Edges: hyperlinks


Proposition:

1. All web pages are not equally "important"
2. There is large diversity in the web-graph node connectivity

Hence, let us rank the pages by the link structure.

In the context of ranking webpages, there are numerous link analysis approaches:
- Page Rank
- Hubs and Authorities (HITS)
- Topic-Specific (Personalized) Page Rank
- Web Spam Detection Algorithms

We will initially (and primarily) concern ourselves with Page Rank.


## The "Flow" Formulation

### Idea
- Links as votes.
- A page is more important if it has more links
  - Incoming or outgoing links?


We will use incoming links (in-links).

But are all in-links equal? They shouldn't be, since links from important pages count more.

A simple recursive formulation:

- Each link's vote is proportional to the importance of it source page
- If page $j$ with importance $r_j$ has $n$ out-links, each link gets $r_j / n$ votes
- Page $j$'s own importance is the sum of the votes on its in-links

### Example 1
Let's consider an example where we have a page $j$ with one in-link from page $i$ and one in-link from page $k$, where page $i$ has 3 total out-links and page $k$ has 4 total out-links.

![alt](https://i.gyazo.com/57c2a82bc25f3381a6e00a8d35e33852.png)

The importance of page $j$ therefore is

$$ r_j = \frac{r_i}{3} + \frac{r_k}{4} $$

Furthermore, given that page $j$ has 3 out-links, each out-link will vote with a weight of $j / 3$.

More generally, we can define the "rank" $r_j$ for a page $j$ by saying that

$$ r_j = \sum_{i \rightarrow j} \frac{r_i}{d_i} $$

where $d_i$ is the out-degree of node $i$, and $i \rightarrow j$ denotes all of the pages $i$ that point to $j$.

This gives us a series of "flow" equations. Let's explore this in the following example

### Example 2

![alt](https://i.gyazo.com/3d03917f7b4aa3eeedd0a00af782cc19.png)

The resulting flow equations from this are

$$ r_y = \frac{r_y}{2} + \frac{r_a}{2} $$
$$ r_a = \frac{r_y}{2} + r_m $$
$$ r_m = \frac{r_a}{2} $$

However, we see there is no unique solution to this system of equations.
But by introducing the constraint that our Page Rank scores sum to 1, we can force uniqueness

$$ r_y + r_a + r_m = 1 $$

Giving us the unique solutions

$$ r_y = \frac{2}{5}, \space\space r_a = \frac{2}{5}, \space\space r_m = \frac{1}{5} $$

So, are we done? Not quite - this approach is only practical for very small graphs, which is certainly not the case with the web. This demands a new approach

## The Matrix Formulation

### Idea

Stochastic adjacency matrix $M$
- Let page $i$ have $d_i$ out-links
- If $i \rightarrow j$, then $M_{ji} = \frac{1}{d_i}$ else $M_{ji} = 0$
- $M$ is a <b>column stochastic matrix</b> - columns sum to <b>1</b>

Rank vector $r$: vector with an entry per page
- $r_i$ is the importance (Page Rank) score of page $i$
- $\Sigma_i r_i = 1$

We can rewrite the flow equations

$$ r_j = \sum_{i \rightarrow j} \frac{r_i}{d_i} $$

into this matrix-vector formulation

$$ r = M \cdot r $$

Note: $\boldsymbol{x}$ is an eigenvector with the corresponding eigenvalue $\boldsymbol{\lambda}$ if

$$ \boldsymbol{A} \boldsymbol{x} = \boldsymbol{\lambda} \boldsymbol{x}  $$

And so we see that this is essentially an eigenvalue problem
- The rank vector $r$ is an eigenvector of the web matrix $M$
- Furthermore, it is its principal eigenvector, with corresponding eigenvalue of 1

This changes the form of the problem from one of solving a system of equations into one of finding the eigenvector of $M$
- There exists a highly efficient way of computing $r$ for matrices like $M$: power iteration.

## Power Iteration and the Random Walk Interpretation

### Idea

Suppose there are $N$ web pages

First, initialize

$$ r^{(0)} = [\frac{1}{N}, \ldots,  \frac{1}{N}]^T $$

Then, iterate

$$ r^{(t+1)} = M \cdot r^{(t)} $$

Stop when

$$|r^{(t+1)} - r^{(t)}|_1 < \epsilon$$

Where $|x|_1 = \Sigma_{1 \le i \le N} |x_i|$ is the $\boldsymbol{L_1}$ norm. Can use any other vector norm: e.g., Euclidean.


Equivalently, this may be written as

$$ r_j^{(t+1)} = \sum_{i \rightarrow j} \frac{r^{(t)}_i} {d_i} $$

where $d_i$ is the out-degree of node $i$, and $i \rightarrow j$ denotes all of the pages $i$ that point to $j$.

It is guaranteed that for particular kinds of graphs:

- There is a unique result for $r$
- This result will be reached eventually regardless of what we choose for $r^{(0)}$

But how can we prove that is relevant for our graph and that it will converge?

### The Random Walk Interpretation

We treat PageRank scores as the probability distribution of a random walker in a graph.
- At any time $t$, a web surfer is on some page $i$
- At time $t + 1$, the surfer follows an out-link from $i$ at random with uniform probability
- Surfer ends up on some page $j$ linked from $i$
- Process repeats indefinitely


<b>... Explanation & Implementation to be continued ...</b>
