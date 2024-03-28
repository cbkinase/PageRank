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

# Model

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


# The Flow Formulation

- Treat links as votes.
- A page is more important if it has more links
  - Incoming or outgoing links?


We will use incoming links (in-links).

But are all in-links equal? They shouldn't be, since links from important pages count more.

A simple recursive formulation:

- Each link's vote is proportional to the importance of it source page
- If page $j$ with importance $r_j$ has $n$ out-links, each link gets $r_j / n$ votes
- Page $j$'s own importance is the sum of the votes on its in-links

## Example 1
Let's consider an example where we have a page $j$ with one in-link from page $i$ and one in-link from page $k$, where page $i$ has 3 total out-links and page $k$ has 4 total out-links.

![TODO: alt text](https://i.gyazo.com/57c2a82bc25f3381a6e00a8d35e33852.png)

The importance of page $j$ therefore is

$$ r_j = \frac{r_i}{3} + \frac{r_k}{4} $$

Furthermore, given that page $j$ has 3 out-links, each out-link will vote with a weight of $r_j / 3$.

More generally, we can define the "rank" $r_j$ for a page $j$ by saying that

$$ r_j = \sum_{i \rightarrow j} \frac{r_i}{d_i} $$

where $d_i$ is the out-degree of node $i$, and $i \rightarrow j$ denotes all of the pages $i$ that point to $j$.

This gives us a series of "flow" equations. Let's explore this in the following example

## Example 2

![TODO: alt text](https://i.gyazo.com/3d03917f7b4aa3eeedd0a00af782cc19.png)

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

# The Matrix Formulation

> Unfortunately, no one can be told what the Matrix is. You have to see it for yourself.
>
> &mdash; <i>Morpheus</i>

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

# Power Iteration and the Random Walk Interpretation

Suppose there are $N$ web pages

First, initialize

$$ r^{(0)} = [\frac{1}{N}, \ldots,  \frac{1}{N}]^T $$

Then, iterate

$$ r^{(t+1)} = M \cdot r^{(t)} $$

Stop when

$$|r^{(t+1)} - r^{(t)}|_1 < \epsilon$$

Where $|x|₁ = Σ_{1 ≤ i ≤ N} |xᵢ|$ is the $\boldsymbol{L_1}$ norm, though any vector norm may be used.


Equivalently, this may be written as

$$ r_j^{(t+1)} = \sum_{i \rightarrow j} \frac{r^{(t)}_i} {d_i} $$

where $d_i$ is the out-degree of node $i$, and $i \rightarrow j$ denotes all of the pages $i$ that point to $j$.

This is known as the <b>power iteration</b> method, and it is particularly effective for large sparse matrices like those of $M$.

It is guaranteed that for particular kinds of graphs:

- There is a unique result for $r$
- This result will be reached eventually regardless of what we choose for $r^{(0)}$

But how can we prove that is relevant for our graph and that it will converge?

## The Random Walk Interpretation

We treat PageRank scores as the probability distribution of a random walker in a graph.
- At any time $t$, a web surfer is on some page $i$
- At time $t + 1$, the surfer follows an out-link from $i$ at random with uniform probability
- Surfer ends up on some page $j$ linked from $i$
- Process repeats indefinitely

Let $p(t)$ be a vector whose coordinate at $i$ is the probability that the surfer is at page $i$ at time $t$
- $p(t)$ is a probability distribution over all pages

### The Stationary Distribution

In a Markov chain with a row stochastic transition matrix $P$, the <b>stationary distribution</b> refers to some vector $\psi$ such that $\psi \cdot P = \psi$.

Intuition: where is the surfer at time $t + 1$?

Follow a link uniformly at random:

$$p(t + 1) = M \cdot p(t)$$

If the random walk reaches a steady state such that:

$$p(t + 1) = M \cdot p(t) = p(t)$$

Then $p(t)$ is a stationary distribution of a random walk.

Notice that this is essentially the same formulation as our matrix interpretation &mdash; our original rank vector $r$ satisfies $r = M \cdot r$.

$r$ is therefore a stationary distribution for the random walk.

# Issues, and the Google Formulation

Up until now, we have dealt with two key equations: the flow equations and the equivalent matrix formulation of the problem.

$$ r_j^{(t+1)} = \sum_{i \rightarrow j} \frac{r^{(t)}_i} {d_i} \space \xLeftrightarrow{} \space r^{(t+1)} = M \cdot r^{(t)} $$

However, there are three key questions we must ask ourselves about these equations if they are to be useful as a general PageRank algorithm.

- Does it converge?
- Does it converge to what we want?
- Are the results reasonable?

Let's explore some key faults in our current formulation of PageRank:
1) Some pages have no out-links (<b>dead-ends</b>) and <b>cause importance to be leaked out</b>
2) If out-links from web pages form a small group, a random walker can get trapped in a small part of the graph
   - These <b>spider traps</b> can occur when all out-links are within a group. Eventually, they <b>will absorb all of the importance</b>
   - This is fairly intuitive from the random walk interpretation: if I can't leave a certain page/set of pages, of course I will spend all of my time there once I arrive

So, with the current formulation, sometimes the result will not converge, and sometimes it will converge to a value that is nonsensical.

### The Google Solution: Random Teleports

At each time step, the surfer has two options:
1) With probability $\beta$, follow a random out-link
   - Common values for $\beta$ are in the range 0.8 to 0.9
2) With probability $1 - \beta$, jump to some random page

This allows surfers to escape from a spider trap within a few time steps.

However, we are still left with the problem of dead ends.

![TODO: alt text](https://i.gyazo.com/099ed2f3db4cbddd33d6688f2f7aa23a.png)

In this example, if we calculate the adjacency matrix $M$ we get


$$ M = \begin{bmatrix}
       ^1/_2 & ^1/_2 & 0 \\
       ^1/_2 & 0     & 0 \\
       0     & ^1/_2 & 0
     \end{bmatrix} $$

But since node M is a dead end, the column for node $m$ no longer sums to 1. Our matrix is not column stochastic, and importance continually "leaks" out of $m$ until $r$ eventually reaches 0 for every page.

In this case, the solution is to <b>always</b> teleport to a random page when a dead end is reached.

![TODO: alt text](https://i.gyazo.com/270a219cc86c59c6a45033e226b7df30.png)

Resulting in a column stochastic matrix $M$

$$ M = \begin{bmatrix}
       ^1/_2 & ^1/_2 & ^1/_3 \\
       ^1/_2 & 0     & ^1/_3 \\
       0     & ^1/_2 & ^1/_3
     \end{bmatrix} $$

#### Why Teleports Solve the Problem

Let's consider the theory of Markov chains:

- We have a set of states $X$
- Transition matrix $P$ where

$$P_{ij} = P\left(X_t = i \middle | X_{t-1} = j\right)$$

- $\pi$ specifying the stationary probability distribution of being at each state $x \in X$
- Goal is to find $\pi$ such that $\pi = P \pi$

A key result in the theory of Markov chains:

As long as $P$ is stochastic, irreducible, and aperiodic, <b>any</b> start vector will converge to a unique positive stationary vector.

We have already seen how introducing teleports allows all of the columns to sum to 1 (thus making it stochastic), so let's explore these other two properties.

A chain is <b>periodic</b> if there is a predictable cycle: that is, there exists some $k > 1$ such that the interval between two visits to some state $s$ is always a multiple of $k$.

![TODO: alt text](https://i.gyazo.com/21caa9a1f211e57e6ee979063bba95b5.png)

Above, we see a periodic graph &mdash; after 3 steps we will always return to the same node. But notice that by adding teleports, there is no such guarantee. For example, even just by allowing self-teleportation, it is possible to break the loop by spending additional time at the current node, as seen below.

![TODO: alt text](https://i.gyazo.com/621aefa8bd871fcc5035c49c4c03f170.png)

Now, let us consider irreducibility. A matrix $M$ is <b>irreducible</b> if there is a non-zero probability of going from any one state to another. Of course, it is easy to see how this is solved by allowing random jumps: at time $t + 1$, there is a probability of $\frac{1 - \beta}{N}$ (where $N$ is the number of web pages) that I can go to <i>any</i> random page.

And this, precisely, is Google's solution: make $M$ stochastic, irreducible, and aperiodic by allowing random teleportation (and guaranteeing it on dead-ends).

At each step, the web surfer has two options:
- With probability $\beta$, follow a random out-link
- With probability $1 - \beta$, jump to some random page

We can rewrite the PageRank equation as

$$ r_j = \sum_{i \rightarrow j} \beta \space \frac{r_i} {d_i} + (1 - \beta) \frac{1}{N} $$

Although the above formulation assumes no dead-ends. We simply follow a random teleport link with probability 1 from dead ends.

Or, in the matrix formulation, we can define the "Google Matrix" $A$

$$ A = \beta M + (1 - \beta) \frac{1}{N} \boldsymbol{e} \cdot \boldsymbol{e^T} $$

Where $\boldsymbol{e}$ is a vector of all 1s.

Given that $A$ is stochastic, aperiodic, and irreducible, we know that

$$ r^{(t+1)} = A \cdot r^{(t)} $$

will converge by power iteration.

# How we Really Compute PageRank

The key step in computing PageRank is our matrix-vector multiplication. This is trivial if $r^{(t+1)}$, $r^{(t)}$, and $A$ fit into main memory, but this is not the case with web-scale data. One of the issues here is that $A$ (compared with the $M$ in the original matrix formulation) is no longer a sparse matrix.

What's the problem with this? Let's do some quick calculations:

Suppose we have $N$ = 1 billion pages (very small compared to the real web) and we need 4 bytes per entry. For our vectors $r^{(t+1)}$ and $r^{(t)}$ we will need 2 billion entries, or approximately 8 GB. However, matrix $A$ has $N^2$ entries which would require $10^{18}$ bytes of RAM (in the exabytes)! This is not practical - we need a new way of thinking about the problem.

## The Sparse Matrix Formulation

In a page $j$ with $d_j$ out-links, we said that $M_{ij} = \frac{1}{d_j}$ when $j \rightarrow i$ and $M_{ij} = 0$ otherwise. But notice that random teleportation is equivalent to reducing the probability of following each out-link from $\frac{1}{d_j}$ to $\frac{\beta}{d_j}$.

Or, equivalently, taxing each page a fraction $1 - \beta$ of its score and evenly redistributing it.

Let's use this to rearrange our equation, assuming no dead-ends for now

$$ r = A \cdot r $$

where

$$ A_{ij} = \beta M_{ij} + \frac{1 - \beta}{N} $$

First, we must unpack the PageRank equation

$$ r_i = \sum_{j=1}^{N} A_{ij} \cdot r_j $$

Substituting the value for $A_{ij}$ from above, we get

$$ r_i = \sum_{j=1}^{N} \space [\beta M_{ij} + \frac{1 - \beta}{N}] \cdot r_j $$

Applying the distributive property to the summation

$$ r_i = \sum_{j=1}^{N} \beta M_{ij} \cdot r_j +  \sum_{j=1}^{N}  \frac{1 - \beta}{N} \cdot r_j $$

Since $\Sigma r_j$ = 1, we can simplify further

$$ r_i = \sum_{j=1}^{N} \beta M_{ij} \cdot r_j +  \frac{1 - \beta}{N} $$

Rearranging into the more explicit matrix formulation, we get

$$ r = \beta M \cdot r + [\frac{1 - \beta}{N}]_N $$

Where $[\frac{1 - \beta}{N}]_N$ denotes a vector of length $N$ with all entries $\frac{1 - \beta}{N}$

The benefit of this is that we never need to materialize the dense matrix $A$ &mdash; we can simply work with the sparse matrix $M$.

So in each iteration, first we compute

$$ r^{new} = \beta M \cdot r^{old} $$

And add a constant value $\frac{1 - \beta}{N}$ to each entry in $r^{new}$.

Note that if $M$ contains dead-ends, then $\Sigma_i r^{new}_i < 1$ and we must renormalize $r^{new}$ so that it sums to 1.

## PageRank: the Complete Algorithm

Given an input graph $G$ and parameter $\beta$, where $G$ may have spider traps or dead-ends, we will produce an output PageRank vector $r$

First, set

$$ r^{(0)}_j = \frac{1}{N}, \space \space t= 1 $$

Do

$$ \forall j: r_j'^{\space (t)} = \sum_{i \rightarrow j} \beta \frac{r^{(t-1)}_i}{d_i} $$

or, if the in-degree of $j$ is 0

$$ r'^{\space (t)}_j = 0 $$

Re-insert leaked PageRank that has been lost to dead ends

$$ \forall j: r^{(t)}_j = r'^{\space (t)}_j + \frac{1 - S}{N} $$

where $S = \Sigma_j r'^{\space (t)}_j$, and $1 - S$ represents the "leaked" PageRank

Then, set

$$ t = t + 1 $$

Repeat until

$$ \Sigma_j | r_j^{(t)} - r_j^{(t - 1)} | > \epsilon  $$

Where $\epsilon$ is some small number of our choosing.

This algorithm is robust, regardless of spider traps or dead-ends. And we might be tempted to say we are done here, but we still have one more concern. We are still assuming that $M$, $r^{old}$, and $r^{new}$ can all fit into RAM, which is not the case.

# Computing PageRank on Big Graphs

We turn to a different encoding scheme for our sparse matrix using only nonzero entries: for every source node, we store its degree and a pointer to/identifier of the destination node.

This will yield a table of the form

| Source node 	| Degree 	| Destination nodes     	|
|-------------	|--------	|-----------------------	|
| 0           	| 3      	| 1, 5, 7               	|
| 1           	| 5      	| 17, 64, 113, 117, 245 	|
| 2           	| 2      	| 13, 23                	|

For now, let us assume that we have enough RAM to fit $r^{new}$, although not enough for $M$ or $r^{old}$.


# Explanation & implementation to be continued...
