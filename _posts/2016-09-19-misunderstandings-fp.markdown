---
layout: post
title: "Common Misunderstandings of Functional Programming"
categories: blog
tags: fp languages scala haskell
---

I have been working in the industry for 2 years, and seen and read about a number of others' opinions regarding
some programming concepts, especially in functional programming area(FP). It turns out that there are some 
concepts that are not supposed to be confused, however becoming widely accepted in a wrong interpretation.
Hence I would like to aggregate some of ones I've identified here.


## Immutability != FP

It's true that functional programming mostly relies on immutability and some early functional programming language
implementations explicitly utilized that. But it's not true that having builtin immutable data and encouraging
programming in immutable style make the language or the code "functional". Owning an elementary building block
doesn't make essential difference.

On the other hand, modern FP doesn't require you always programming immutably as well.


## Lambda != FP

It's oftenly heard that "Java/C# have already been functional programming languages since lambda is supported". Once
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
way. To make my point, for instance, it's not a pleasant 


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

However, functional programming languages don't get close to natural languages intentionally, but rather more oftenly
defined according to some mathematically properties.


## Referential Transparency

It's very common for so-called functional programmers to talk about referential transparency or RT in short and 
very often in the conversation, these people might make it sound that RT is only or mostly a FP feature and it's
very difficult for you to identify and implement code that can be considered RT easily in, say, imperative languages
like C.

While it's true where functional


[stream-map]: https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#map-java.util.function.Function-
[function]: http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/java/util/function/Function.java
[scalatest]: http://www.scalatest.org/quick_start
