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

* scala insufficiency
    
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
  
  hence we got the first impression on how unification in type inference works.(example taken from &lt;The Implementation
  of Funtional Programming Languages&gt;, P151)
 
  in prolog:

  ```prolog
  | ?- T1 = ap(T2, T4),
  T3 = ap(T2, T5),
  T4 = ap(T5, T6),
  T7 = ap(T1, ap(T3, ap(T2, T6))).
  
  T1 = ap(T2,ap(T5,T6))
  T3 = ap(T2,T5)
  T4 = ap(T5,T6)
  T7 = ap(ap(T2,ap(T5,T6)),ap(ap(T2,T5),ap(T2,T6)))
  ```

* recursion schemes to fp is for loop to imperative languages

  what recursion schemes do can totally put an analogy to for loop, but with a much wider usage over the latter.

  fmap: manipulate one element in each iteration
  bind: a double for loop but the result in flattened

  catamorphism: recursion. fold, each iteration reduces the corresponding element and accumulate
  anamorphism: corecursion. unfold, each iteration generates an element according to the previous element

* how more general the type system in scala is compared to the one in haskell

  there are a number of things if we allow inheritence in the type system like scala. with the power of traits,
  we can further separate logic from data to exercise a better level of software design. it's very interesting to see
  in scala community, in terms of type system, most people try very hard to port existing functionality in haskell into
  the scala library. fine though, i think it's much better if we can explore more and find out that's the extra thing 
  we can do in scala language.

  it turns out that with inheritence taken into account, all of sudden we introduces the partial ordering relationship
  into the type system. this immediately breaks the classic unification algorithm, which solves symbolic equalities, 
  whilst scala types relations are inequalities now.

  also noticing that, scala type system is actually a complete lattice, with `Any` as the unique supremum, and `Nothing`
  to be the unique infimum. compared to haskell type system, which actually has no partial ordering relation, and typical
  OO type system, which has no infimum in the types and less power in the system, scala type system is actually the most
  advanced and complex one, but also be capable of describing data relations freely and soundly. satisfying this property,
  we can actually introduce abstract algebra to the analysis of the type system.

  noticing the nature of (complete) lattice in the scala type system, it's very straightforward to conclude that for
  a set of type relation, it's practically good if we also construct the subset of those types to form a complete lattice.
  since `Nothing` will automatically become the infimum of the lattice, the only thing we need to do is guarantee a
  supremum exists.

  for example, we start with following relation

  ```scala
  trait Property

  trait Owner[P <: Property]
  ```
  it represents the `Owner` of certain type of `Property`. however, generic type `P` being invariance borthers a lot, since
  there is no supremum for this poset. if we are sure that we need this generics(depending on the design purpose, in a trait
  driven principle, this kind of generics can very often be moved up to a higher level), there are 2 ways of fixing it

  make `P` covariant:

  ```scala
  trait Owner[+P <: Property]
  ```

  this solution is much preferred. it naturally makes `Owner[Property]` be the supremum and the poset forms a lattice.

  or defining a trait without generic:

  ```scala
  trait GOwner

  trait Owner[P <: Property] extends GOwner
  ```

  but this solution indicates a problem. what prevents us from making `P` covariant is probably it's used somewhere in a
  contravariant position. this sets a flag for design flaw, since `GOwner` is most likely very useless, probably just to
  introduce a supremum. It's very helpful to use some mathematical principle to verify the design and overlap theory and
  the practice.

  that said, it's not necessary to say we must have complete lattice in our type relations but just preferred. sometimes
  it's a complex tradeoff. e.g. `Set[C]` is invariant as `C` appears in a contravariant position. so which one you prefer,
  guarding checking the existence of a totally unrelated object in a set, or allow `Set[C]` being able to perform upcast?
  this is reality. this is life. life is so hard.


* functional programming and lambda calculi

  the idea of functional programming and one of imperative/OO programming are fundamentally different. in the first place,
  fp are developed based on either lambda calculi or combinatory logic(mathematical modeling that allows vanilla mathematical
  analysis to the program), while imperative/OO are based on turing machine(a more command based, engineering oriented
  computational model).

  a very distinct difference between these 2 is the concept of data and logic. for instance, a tuple is a cell that has 2 fields,
  each of which contains it's own data and there is no necessity to correlate both fields. in haskell, we do

  ```lhaskell
  > let cell = (10, "hello world")
  ```

  in imperative programming's perspective, it belongs to data, and we need operation on it. for instance, to extract the fields,

  ```lhaskell
  > fst cell
  10
  > snd cell
  "hello world"
  ```

  at this moment, it might be very clear that how this works. it's just a struct of 2 pointers pointing to some other data 
  structures. please note now the memory layout of tuple is still very easy to visualize.

  so far so good, there is no difference. however, i can define a tuple in a totally different way:

  ```haskell
  tup' a b f = f a b
  fst' t     = t $ \a b -> a
  snd' t     = t $ \a b -> b
  ```

  subsequently, we can do:

  ```lhaskell
  > let cell = tup' 10 "hello world"
  > fst' cell
  10
  > snd' cell
  "hello world"
  ```

  it does the job. but what about now? or to be specific, where are `a` and `b` stored in memory? for those having difficulties
  understanding what just happened, `tup'` is supposed to take 2 pieces of arbitrary data, and put them into a closure, which
  has some sort of promise to be invoked as parameters of some function, which is not yet known.

  after all, the locations of `a` and `b` are no more transparent but rather managed by, either language or runtime, depending
  on which you think the responsibility falls to. 

  more example,

  ```haskell
  bimap' f g t = t $ \a b -> tup' (f a) (g b) -- map both fields together with 2 functions
  first' f     = bimap' f  id
  second' g    = bimap' id g
  ```

  it's very interesting to see functions(logic) and data are much more ambiguous in a functional programming language, and 
  what we will be focusing on is just to describe what the data has, instead of how the data is constructed. this, i guess,
  might be due to the nature of lacking execution model in lambda calculi, compared to very obvious tape based one in turing
  machine. or i might have used the wrong word, which might lead me to criticism: there is no such thing called execution
  in mathematics. the only thing exists is the relation of equivalence(or Referentially Transparency, out of mouths of
  some fp nerds). in fp language, say haskell(almost), expressions in default context are equivalent, if all its subexpressions
  are equivalent. exquivalence in such context very often means extensional equivalence. in above example,

  ```haskell
  200
  ```

  and 

  ```haskell
  fst' $ bimap' (20*) id $ tup' 10 undefined
  ```
  
  are equivalent. and the rule to examine that is substitution. we have:

  ```
  fst' $ bimap' (20*) id $ tup' 10 undefined
  >> tup' 10 undefined $ (\a b -> tup' (20 * a) (id b)) $ (\a b -> a)
  >> ((\a b -> a) . (\a b f -> f (20 * a) (id b))) 10 undefined
  >> (\a b -> a) (\f -> f (20 * 10) (id undefined))
  >> (\a b -> a) (20 * 10) (id undefined)
  >> 20 * 10
  >> 200
  ```

  hence they are equivalent. one thing worth mentioning is that, equivalence relation is mathematically speaking detached
  to what so-called evaluation, but just a simple `a equals b` relation. in previous example, we can also say the latter
  expression is equivalent to `2 + 198`, as both denote the very same mathematical obejct. this effectively decouples the
  actual representation of the data structure from the comparison of the meaning of it. in fp, we just focus on the 
  denotation of a program. on the other hand, in imperative language, we have to be concerned about the operational effect.

* experience in the industry

  a talk about politics
