---
layout: post
title: "Common Misunderstandings of Functional Programming"
categories: blog
tags: fp languages scala haskell
---

I have been working in the industry for 2 years, and seen and read about a number of others' opinions regarding
some programming concepts, especially in functional programming area(FP). It turns out that there are some 
concepts that are not supposed to be confused, however becoming widely accepted in a wrong interpretation.
Hence here is an aggregation of those misunderstandings and I will be trying to clarify a bit after identifying them.


## Immutability != FP

It's true that functional programming mostly relies on immutability, and some early functional programming language
implementations explicitly utilized that. But it's not true that having builtin immutable data and encouraging
programming in immutable style make the language or the code "functional".

On the other hand, modern FP doesn't require you always program immutably as well. Conceptually, immutability 
is used to preserve the property of referencial transparency, which is a term I am very hesitant to use, but not
necessary for all the case. For instance, in haskell, `ST` monad is used to provide a local mutation context 
within which data can be mutated, that is transparent to the outside world. That means so called referencial
transparency actually has a contextual implication. More on this term, please reference 
[Referential Transparency](#referential-transparency).

## Lambda != FP

It's often heard that "Java/C# have already been functional programming languages since lambda is supported". Once
again, though lambda expression is the essential building block of a fplang construct, but it's not true to consider
the languages to be functional and the programmers that use the feature once a while a "functional programmers".

In essense, it's not necessary for, in this example, Java to have lambda expressions. For instance, in Java 8, now
we are allowed to write code that uses classic combinators like `map`, `filter` over a sequential collection:

```java
List<Integer> intList = // from somewhere else

IntStream intListPlus1 = intList.stream().mapToInt(i -> i + 1)
```

But if we look at the interface of `mapToInt`(or its brothers), we can find out it is [defined][stream-map] as:


```java
<R> Stream<R> map(Function<? super T,? extends R> mapper)
```

The corresponding [interface][function]:

```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);
}

```

Essentially lambda expression in Java is just a simple way of writing implementation of single function interfaces.
This is a very typical object oriented technique called *injection*, through an interface. Though the form is 
a lambda expression, the essence of object orientation still doesn't help in terms of designing programs in a functional
way.


## FP does not look like natural languages

It's especially frequently found among scala programmers, who consider the form of functional programming is close
to natural languages, e.g. English. This misunderstanding comes from the syntactical feature of the scala language 
itself.

For example, in `scalatest`, one can write a test case like this to make it read naturally in English([quote][scalatest]):

```scala
  "A Stack" should "pop values in last-in-first-out order" in {
    val stack = new Stack[Int]
    stack.push(1)
    stack.push(2)
    stack.pop() should be (2)
    stack.pop() should be (1)
  }
```

It's very superficial. A FP language most likely is based on lambda calculi or combinatory logic, which are both mathematical
models of computation. By design, FP is intended to be a more mathematically precise computational description, instead
of something like natural language approximation.

## Syntactical sugar != FP

It seems factual that functional programming languages provide much more syntactical sugar than those are not. For instance,
Haskell and Scala support:

1. pattern matching
1. monadic comprehension(do-notation and for comprehension repectively)
1. flexible and customizable syntax

However, NONE of these are necessarily FP specific, though they are rare to see in any other types of languages.
A counter example of this would be [Rust][rust], which is an imparative language with pattern matching.


## Referential Transparency

Referential transparency(RT) is a very ambiguous and controversal concept which is very easy for people to misunderstand
(or might not be able to be understood) but it's too innocent looking. There are a number of excellent StackOverflow 
answers that talk about it, e.g. [don't say RT][rtso1] and [RT explained philosophically][rtso2], that kind of give the
feeling of unprecision and bias of the most accepted interpretation of this term.

Though this term is very ambiguous, as most people use it to mean([wiki][wikirt]):

> An expression is said to be referentially transparent if it can be replaced with its corresponding value without
> changing the program's behavior.

I will be interpreting this term using this definition. However, it's still common for people to take this concept
in following wrong ways.


### RT is not a language level property

It's very common for so-called functional programmers to talk about referential transparency and they might make it
sound that RT is only or mostly a FP feature and it's very difficult for you to identify and implement code that can
be considered RT easily in, say, imperative languages like C. 

It's false to say "C is not referentially transparent".

### RT is a app wide concept

contextual


[stream-map]: https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#map-java.util.function.Function-
[function]: http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/java/util/function/Function.java
[scalatest]: http://www.scalatest.org/quick_start
[rtso1]: http://stackoverflow.com/questions/4865616/purity-vs-referential-transparency
[rtso2]: http://stackoverflow.com/questions/210835/what-is-referential-transparency/11740176#11740176
[rust]: https://www.rust-lang.org/en-US/
[wikirt]: https://en.wikipedia.org/wiki/Referential_transparency
