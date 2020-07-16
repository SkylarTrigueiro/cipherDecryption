# Cipher Decryption

## Overview
In this project I am building a cipher decrypter for simple cyphers in the english language. An example of a simple cipher would be map of the form:

a -> b, b -> c, c -> d, ... z -> a

so that the message "abc" is transformed into "bcd". I will be doing this by expaning on a project from the udemy course "Data Science: Natural Language Processing (NLP) in Python", which initially built a genetic bigram language model (more on that in the sections that follow). I will be expanding on this by extending it to a genetic trigram model.

## Data
The data that the model is trained by reading the book "Moby-Dick; or, The Whale" by Herman Melville (link, https://www.gutenberg.org/ebooks/2701). To test algorithm, I encoded a passage from the book "The Adventures of Sherlock Holmes", by Arthur Conan Doyle (link: https://www.gutenberg.org/ebooks/1661) and had the model attempt to decrypt the cipher.

## Model
The model I'm working on is the genetic trigram language model. The following provides a brief explanation behind how the algorithms work and why an improvemnt was needed. 

### Genetic Algorithm
This model works by creating an initial guess cipher, the parent, such as 

a -> b, b -> c, c -> d, ... z -> a

and then creating new ciphers by swapping letters in this mapping, the children, and then picking the best cipher with the highest log-likelihood to create more children.

### Bigram Model

For any given word of length N, we can view the probability of any two in that word as

<a href="https://www.codecogs.com/eqnedit.php?latex=pr(x_1x_2)&space;=&space;pr(x_2|x_1)pr(x_1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?pr(x_1x_2)&space;=&space;pr(x_2|x_1)pr(x_1)" title="pr(x_1x_2) = pr(x_2|x_1)pr(x_1)" /></a>

or alternatively

<a href="https://www.codecogs.com/eqnedit.php?latex=log(pr(x_1x_2))&space;=&space;log(pr(x_2|x_1))&space;&plus;&space;log(pr(x_1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log(pr(x_1x_2))&space;=&space;log(pr(x_2|x_1))&space;&plus;&space;log(pr(x_1))" title="log(pr(x_1x_2)) = log(pr(x_2|x_1)) + log(pr(x_1))" /></a>