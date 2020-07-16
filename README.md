# Cipher Decryption

## Overview
In this project I am building a cipher decrypter for simple cyphers in the english language. An example of a simple cipher would be map of the form:

{a:b, b:c, c:d, ..., z:a}

so that the message "abc" is transformed into "bcd". I will be doing this by expaning on a project from the udemy course "Data Science: Natural Language Processing (NLP) in Python", which initially built a genetic bigram language model (more on that in the sections that follow). I will be expanding on this by extending it to a genetic trigram model.

## Data
The data that the model is trained by reading the book "Moby-Dick; or, The Whale" by Herman Melville (link, https://www.gutenberg.org/ebooks/2701). To test algorithm, I encoded a passage from the book "The Adventures of Sherlock Holmes", by Arthur Conan Doyle (link: https://www.gutenberg.org/ebooks/1661) and had the model attempt to decrypt the cipher.

## Model
The model I'm working on is the genetic trigram language model. The following provides a brief explanation behind how the algorithms work and why an improvemnt was needed. 

### Genetic Algorithm
This model works by creating an initial guess cipher, the parent, such as 

{a:b, b:c, c:d, ..., z:a}

and then creating new ciphers by swapping letters in this mapping, the children, and then picking the best cipher with the highest log-likelihood to create more children.

### Bigram Model

For any given word of length N, we can model the probability of any two consecutive letters occurring in that word as

<a href="https://www.codecogs.com/eqnedit.php?latex=pr(x_1x_2)&space;=&space;pr(x_2|x_1)pr(x_1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?pr(x_1x_2)&space;=&space;pr(x_2|x_1)pr(x_1)" title="pr(x_1x_2) = pr(x_2|x_1)pr(x_1)" /></a>

or equivalently

<a href="https://www.codecogs.com/eqnedit.php?latex=log(pr(x_1x_2))&space;=&space;log(pr(x_2|x_1))&space;&plus;&space;log(pr(x_1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log(pr(x_1x_2))&space;=&space;log(pr(x_2|x_1))&space;&plus;&space;log(pr(x_1))" title="log(pr(x_1x_2)) = log(pr(x_2|x_1)) + log(pr(x_1))" /></a>

Which works well and will lead to a mostly correct solution. I found that the model converged to a cipher that mapped two letters incorrectly and gave this cipher a higher score than the correct cipher leading to words like 'just' to be mapped to 'qust' because 'qu' has a higher probability than 'ju' based on its training. Even with the incorrect map, the decoded passage is still readable and I believe most people would be able to figure out where the error in the mapping is without much difficulty. However, we could do better.


### Trigram Model

For any given word of length N, we can model the probability of any three consecutive letters in that word as

<a href="https://www.codecogs.com/eqnedit.php?latex=pr(x_1x_2x_3)&space;=&space;pr(x_3|x_1x_2)pr(x_2|x_1)pr(x_1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?pr(x_1x_2x_3)&space;=&space;pr(x_3|x_1x_2)pr(x_2|x_1)pr(x_1)" title="pr(x_1x_2x_3) = pr(x_3|x_1x_2)pr(x_2|x_1)pr(x_1)" /></a>

or equivalently

<a href="https://www.codecogs.com/eqnedit.php?latex=log(pr(x_1x_2x_3))&space;=&space;log(pr(x_3|x_1x_2))&space;&plus;&space;log(pr(x_2|x_1))&space;&plus;&space;log(pr(x_1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log(pr(x_1x_2x_3))&space;=&space;log(pr(x_3|x_1x_2))&space;&plus;&space;log(pr(x_2|x_1))&space;&plus;&space;log(pr(x_1))" title="log(pr(x_1x_2x_3)) = log(pr(x_3|x_1x_2)) + log(pr(x_2|x_1)) + log(pr(x_1))" /></a>

with this update to the model, the model converged to the correct mapping and gave the correct solution the highest score of all possible mappings. 

## Further Improvements

In most runs of this code I found that the solution was ultimately reached in much less than the fixed 1000 iterations in 9 out of 10 runs. However, in the 1 out of 10 case, the model got stuck on some mapping and failed to improve by the end of the fixed 1000 iterations. Ideally, I would like to create some convergence test so that the user doesn't have to rerun the code in the event the incorrect solution is reached. 