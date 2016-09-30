---
layout: page
title: TODO
nav: true
permalink: /todo/
---

A list of todo topics

* restriction in OO compared to FP regarding how code is modularized 
    
  OO amiguates the concepts of `definitions` and `properties`. a definition defined a representation, 
  while a property can naturally be derived from definition or other properties.
  
  OO makes both definition and properties a chunk of definition, while FP allows separation between
  these 2 concepts, which allows properties to be augmented afterwards by 3rd party

* scala insufficience
    
  type system

  scala type system is a partial ordered type system, compared to one of haskell. in scala type system, 
  generics are essentially all existential, meaning we can only verify whether a type is in a certain range
  at best. type equivalence is just a special case of type existence where the upper bound of a range happens
  to collapse with the lower bound. it flips the game board upside down and much enlarges the power of the 
  expressiveness of the language.
  
  however there are some type insufficience in scala type system compared to one of haskell. 
  
  1. lack of native rank n types
  
     this is due to type declaration restriction. it makes passing `forall` type of functions around impossible.
     
  
     in haskell, we can write something like
  
     ```haskell
     foo :: (forall a. a -> a) -> [x] -> [y] -> [(x, y)]
     ```
  
     if we turn on `RankNTypes` switch. in scala, hack is needed: 
     https://apocalisp.wordpress.com/2010/07/02/higher-rank-polymorphism-in-scala/   the trick is to hide generic
     into an object which might behave like a function. but not sufficient for those existing components of the language.
     still be nice if we have language support. for example: CanBuildFrom being an instance to build multiple builders
     produces the same kind of collection but of different element types requires a type cast.
  
  2. higher order types are not curried and composible
  
     this is very annoying if we ever want to do type level programming since unlike value level programming, we cannot
     apply generics multiple times in a roll, like:
  
     ```scala
     foo(1)("string")
  
     G[Int][String]  // this cannot work
     ```
  
     so to overcome that, we will need to do some very boring and unnecessary type level indirection, and it constrains
     the flexibility in type level programming.
  
     ```scala
     case class Fix[F[_]](unfix: F[Fix[F]])
  
     Fix[Map[String, _]](Map.empty) // this won't work
  
     // we have to do this
     type SMap[T] = Map[String, T]
     Fix[SMap](Map.empty)
     ```
  
     this is very tiring, and also problemetic if we don't know what it's in the position of key. that makes a huge difference
     compared to programming in type level in haskell.
  
     ```haskell
     type Flip f a b = f b a
     -- Map k v :~: Flip Map v k, for all k and v, where :~: means type equivalence in haskell
     ```
  
     more enoyable in haskell
  
  3. too hard to live with existential type
  
     existential type in scala with bounds are horrible. full of bugs prio to 2.12
  
     a number of issues related to the topic:
  
     [existential on F-bound](https://issues.scala-lang.org/browse/SI-8198)
     [existential on upper bound](https://issues.scala-lang.org/browse/SI-1786)
  
     work around: let compiler forget about existential type. say
  
     ```scala
     trait A
     trait G[E <: A] // how G[_] is interpreted varies in different occurrences
  
     // what we can do if we DON'T care what E is
     case class H(g: G[_ <: A])
     ```

  as a functional language
  
  functions are not curried. this is very annoying. it directly leads to the cost of point-free style in haskell not
  applicable in scala. also object oriented style makes the object in a special position of a functio as well.
  
  example, catamorphism is defined in haskell like this:
  
  ```haskell
  cata :: Functor f => (f a -> a) -> Fix f -> a
  cata f = f . fmap (cata f) . unfix
  
  newtype Fix f = { unfix :: f (Fix f) }
  ```
  
  the form is very close to mathematics definition, so very concise and easy to verify correctness.
  
  in scala
  
  ```scala
  def cata[F[_] : Functor, A](f: F[A] -> A, fix: Fix[F]): A = 
      f(implicitly[Functor[F]].fmap(fix.unfix, { fx => cata(f, fx) }))
  
  case class Fix[F[_]](unfix: F[Fix[F]])
  ```
  
  too much noice. also notice that in the haskell version of definition, the parameter of type `Fix f` is not mentioned
  anywhere in the implementation, for the sake of point-free style in haskell, which in scala, point-free will be pretty much
  unpleasant if one needs to write
  
  ```scala
  (f _) andThen (g _)
  ```
  
  instead of 
  
  ```haskell
  f . g
  ```

  the cost of creating a function is too high(literal an object each function, comes with 16 bytes of minimum overhead)

* turing complete type system == compile time proof system

  it turns out that type system as complicated as haskell's and scala's is in fact a compile time proof system.
  
  we can embed information in the types for compiler to infer and thereafter reason the logic of the code, instead of
  delegating the error report to runtime system.
  
  the implementation of a type inferrence system is very close to a logic system, like prolog, as they both belong to 
  unification. not as obvious as prolog, in an expression, types are essentially establishing relations via symbolic
  equations.
  
  starting from the very beginning ones:
  
  ```haskell
  id x = x -- which converts to id = \x. x during compilation
  ```
  the list of equations as following
  
  ```
  id :: t1
  x  :: t2
  t1 :~: t2 -> t2
  ```
  
  where `:~:` means type equivalence.
  
  so we conclude `id :: t1 :~: t2 -> t2` which means `id :: t2 -> t2`
  
  
  more sophisticated example (S combinator)
  
  ```haskell
  f x y z = x z (y z) -- becomes f = \x -> \y -> \z -> x z (y z)
  ```
  
  forms a graph:
  
  ```
  x :: t1 z :: t2     y :: t3 z :: t2
  ---------------$    ---------------$
    (x z) :: t4         (y z) :: t5
    -------------------------------$
           (x z (y z)) :: t6
           -----------------\x -> \y -> \z ->
                 f :: t7
  ```
  
  equation has:
  
  ```
  t1 :~: t2 -> t4
  t3 :~: t2 -> t5
  t4 :~: t5 -> t6
  t7 :~: t1 -> t3 -> t2 -> t6
  ```
  
  solving it brings us to:
  
  ```
  f :: t7 :~: (t2 -> t4        ) -> t3         -> t2 -> t6
              (t2 -> (t5 -> t6)) -> (t2 -> t5) -> t2 -> t6
  ```
  
  hence we got the first impression on how unification in type inference works.(example taken from <The Implementation
  of Funtional Programming Languages>, P151)
  
  // probably try to implement a symbol type inference system using prolog

* recursion schemes to fp is for loop to imperative languages

  what recursion schemes do can totally put an analogy to for loop, but with a much wider usage over the latter.

  fmap: manipulate one element in each iteration
  bind: a double for loop but the result in flattened

  catamorphism: recursion. fold, each iteration reduces the corresponding element and accumulate
  anamorphism: corecursion. unfold, each iteration generates an element according to the previous element


* experience in the industry

  a talk about politics
