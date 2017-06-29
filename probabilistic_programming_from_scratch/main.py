import itertools
import random
import matplotlib.pyplot as plt

### Probabilistic Programming From Scratch ###

## A simple algorithm for Bayesian inference ##

# Let's take a specific data analysis problem: a simple A/B test for a website.
# Suppose our site has two layouts.
# During our test, 4% of visitors to layout A convert (i.e., buy something, sign up for the mailing list, whatever), and 5% to layout B convert.
# Clearly, layout B is better, so we should use that layout, right?
# But what if I tell you it was a very small test?

n_visitors_a = 100  # number of visitors shown layout A
n_conv_a = 4        # number of visitors shown layout A who converted

n_visitors_b = 40
n_conv_b = 2

# Are we sure B is better?
# What if it costs a shipload of money to change the layout if we're wrong?
# Are we sure enough?
# If not, how much data do we need to be sure?
# We can use a simple algorithm for Bayesian inference to quantify how confident we are with our decision that layout B is better.
# Specifically, we're going to use an inference algorithm called Approximate Bayesian Computation (ABC):

def posterior_sampler(data, prior_sampler, simulate):
    """
    Yield samples from the posterior by Approximate Bayesian Computation.
    """
    for p in prior_sampler:
        if simulate(p) == data:
            yield p
# https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
# https://docs.python.org/3/reference/expressions.html?#yield-expressions

# The function above turns the prior distribution into the posterior.
# Samples from the prior distribution are our best guesses of the values of the unknown parameter of our system.
# Samples from the posterior distribution are the guesses of the same parameters made after the experiment, in the light of the data we have gathered.
# Once you have the posterior, you can answer concrete questions about the implications of the data, such as how likely it is that layout B is better.
# Abstracted away in that little posterior_sampler() generator function is an extremely lightweight probabilistic programming system.


## Using the sampler to finish our A/B test ##

# Let's use it to finish our A/B test, starting with layout A.
# We need to prepare three arguments: data, prior_sampler and simulate.
# We already have the data for our A/B test.
# Let's now write a function that simulates the conversion of n_visitors visitors to a website with known probability p:

def simulate_conversion(p, n_visitors):
    """
    Return number of visitors who convert, given conversion fraction p.
    """
    outcomes = (random.random() < p for i in range(n_visitors))
    return sum(outcomes)

# Here is what happens when we run this function a few times to simulate 100 visitors converting with probability 0.1:
print(simulate_conversion(0.1, 100), simulate_conversion(0.1, 100), simulate_conversion(0.1, 100))
print()

# Effectively, this function runs a fake A/B test in which we already know the conversion fraction.

# Finally, we need prior_sampler.
# This should be a generator that yields a large (potentially infinite) number of guesses for the conversion fraction of a layout.

def uniform_prior_sampler():
    """
    Yield random numbers in interval (0, 1).
    """
    while True:
        yield random.random()

# Now let's write a function that will allow us to see a few samples from this generator.

def take(n, iterable):
    """
    Return first n items of the iterable as a list.
    """
    return list(itertools.islice(iterable, n))

# We can use the take() function to draw three samples from our so-called 'uniform' prior sample like so:

print(take(3, uniform_prior_sampler()))
print()

# Now we're ready to run posterior_sampler() to create an object that will yield up smaples from the posterior distribution for layout A's conversion fraction:

posterior_a_sampler = posterior_sampler(
    data=n_conv_a,
    prior_sampler=uniform_prior_sampler(),
    simulate=lambda p: simulate_conversion(p, n_visitors_a)
)

# The lambda function bakes in the number of visitors for layout A into the simulate argument.
# This is known as 'partial evaluation' and can also be accomplished using functools.partial.

# To get a few samples from the posterior, we can use take() again:

print(take(3, posterior_a_sampler))
print()

# These are three guesses for the unknown conversion fraction of layout A, each of which is reasonably close to 4% (we had 4 conversions from 100 visitors).

# We can use the results above to build up a picture of their distribution by getting thousands of samples from posterior_sampler() and plotting a histogram:

a_samples = take(10000, posterior_a_sampler)
abbins = [i/200.0 for i in range(50)]  # 50 bins between 0 and 0.25
plt.hist(a_samples, bins=abbins, normed=True)  # normed=True gives a probability density function
plt.xlim(0, max(abbins));
plt.show()

# Run the program to display the plot, and it will display the posterior distribution for the conversion fraction of layout A.
# The above plot is a full picture of our knowledge after the experiment.

# The posterior distribution is the object we use to answer concrete questions about our knowledge after an experiment.
# We can, for example, use this one to say how likely it is that layout A's conversion fraction is greater than 10%.
# We can do this by measuring the fraction of a_samples for which that is true:

print(sum(a > 0.1 for a in a_samples)/len(a_samples))
print()

# Again, we're using the fact that the sum of an iterable of booleans is equal to the number of true elements.
# The above code tells us that there's a ~2% chance that layout A's conversion fraction is greater than 10%.
# By the same token, we know that there is a ~98% chance that it's less than 10%.


## Completing the A/B test ##

# To complete the A/B test, we also need the posterior for layout B.
# Let's suppose that layout B is not brand new.
# We do have a rough idea of its conversion fraction before we conduct the experiment.
# Perhaps we think it's 6%, plus or minus a couple of per cent.
# In this case, uniform_prior_sampler is not appropriate, but something like this would work well:

def normal_prior_sampler(mu=0.06, sigma=0.02):
    """
    Yield stream of samples from N(mu, sigma) in interval (0, 1).
    """
    while True:
        x = random.normalvariate(mu, sigma)
        if 0 <= x <= 1:
            yield x

# Mathematically, this function samples from a normal distribution with a known mean and standard deviation, and support in the interval (0, 1).
# Conceptually, though, it's easier to plot a histogram, and compare this prior to the uniform prior we used for layout A.

plt.hist(take(100000, uniform_prior_sampler()), bins=abbins, label='A', normed=True)
plt.hist(take(100000, normal_prior_sampler()), bins=abbins, label='B', alpha=0.5, normed=True)
plt.title('Prior Distributions')
plt.xlim(0, max(abbins))
plt.legend();
plt.show();

# The guesses for layout B are concentrated around 6%, which captures our prior knowledge.
# Now that we have the prior sampler for layout B, we can make its posterior sampler and take some samples:

posterior_b_sampler = posterior_sampler(
    data=n_conv_b,
    prior_sampler=normal_prior_sampler(),
    simulate=lambda p: simulate_conversion(p, n_visitors_b)
)
b_samples = take(10000, posterior_b_sampler)

# Let's visualize the two sets of posterior samples directly:

plt.hist(a_samples, bins=abbins, label='A', normed=True)
plt.hist(b_samples, bins=abbins, label='B', alpha=0.5, normed=True)
plt.title('Posterior Distributions')
plt.xlim(0, max(abbins));
plt.legend();
plt.show();

# Note the histogram for layout B is to the right of that for layout A.
# This is telling us that layout B is probably better than layout A.
# And we're finally in a position to answer the original question: how confident can we be that layout B is better?

# In this simple case, we can do this by making pairwise comparisons between the two lists of estimates and measuring the fraction of pairs for which the estimated conversion fraction of B is bigger than that for A:

print(sum(b > a for a, b in zip(a_samples, b_samples))/len(a_samples))
print()

# And that's that!
# Given the data and our prior beliefs, we are 66% sure that layout B is better than layout A.
