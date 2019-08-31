---
layout: post
categories: blog
tags: scala type
title: Scala Type Unsoundness
---

Scala is a developing language and it has experienced a number of decision changes within the short history. On the
other hand, more and more Scala programmers noticed the limitation of typical object oriented style, though the
compiler has taken a part of the burden on its own. As a consequence, the Scala language itself appears to suffer from
inconsistency within the language design due to lack of central theoretical guidance. 

## The problem of sound type signatures

### A basic style

Scala provides a nice style to help with, or even attempt to eliminate inheritence problem. The construct that is
playing the central role is `trait`. `trait` in Scala has an overwhelming number of meanings, and among all, the most
basic ones are to represent interfaces, and segregate logic and data. So it's common practice to have code like this:

```scala
trait CanFly {
  def fly: Unit
}

trait HelicopterLike extends CanFly {
  def fly: Unit = println("fly like a helicopter")
}

trait Weapon
case object GatlingGun
case object Missle

trait CanFight {
  def weapons: Seq[Weapon] = Seq.empty
  def fight: Unit = println("I am equipped with " + weapons.mkString(" and "))
}

trait HasGatlingGun extends CanFight {
 override def weapons = GatlingGun +: super.weapons
}

trait HasMissle extends CanFight {
  override def weapons = Missle +: super.weapons
}

class Apache extends CanFly with HelicopterLike with CanFight with HasGatlingGun with HasMissle
```

Notice there, we have 2 traits, `CanFly` and `CanFight` serve as interfaces, to signal the capabilities of the class.
And we segregate the implementation into three other small traits which just do the exact thing it's supposed to do. Here,
these 3 traits signify logic instead of represent some sort of interfaces.

It seems natural to do this in Scala, as, for example, `HelicopterLike` is indeed a `CanFly`, with extra implementation
logic with it. Though it provides a way to resolve the diamond problem, it doesn't cover all situations and brings
complexity and unsoundness to the type systems.

### The problems

If the traits has no common base trait, things become very complicated. Consider the following:

```scala
trait A
trait B

trait RetA { def ret: A }
trait RetB { def ret: B }

def ret(o: RetA with RetB) = o.ret
```

and it compiles in console(2.12.1). The problem is, this piece of code doesn't make any sense. Specifically, what `o.ret` is
supposed to return? It totally depends on how you resolve the type `RetA with RetB`. In cosole, it returns:

```
scala> def ret(o: RetA with RetB) = o.ret
ret: (o: RetA with RetB)B
```

which simply gives the type of `RetB`.

This type of unsoundness can be seen in many other ways, including self type bound:

```scala
trait Ret {
  self: RetA with RetB =>

  def foo = ret
}
```

In console:

```
scala> val r: Ret = null
r: Ret = null

scala> :t r.foo
B
```

Even worse:

```
scala> class C
defined class C

scala> class D
defined class D

scala> val o: C with D = null
o: C with D = null
```

The bound `C with D` makes no sense, as both there can be only 2 possible types of instances of this type:
`null` and some exceptions, and it violates the principle of single inheritance, so it can be certain that 
the program is fundamentally wrong and type system is supposed to reject this type of programs(in fact,
you have no way to write such implementation consisting of 2 classes).

However, type system does not always make this mistake:

```
scala> trait RetAImpl extends RetA { def ret = new A {} }
defined trait RetAImpl

scala> trait RetBImpl extends RetB { def ret = new B {} }
defined trait RetBImpl

scala> new RetAImpl with RetBImpl {}
<console>:14: error: <$anon: RetAImpl with RetBImpl> inherits conflicting members:
  method ret in trait RetAImpl of type => A  and
  method ret in trait RetBImpl of type => B
(Note: this can be resolved by declaring an override in <$anon: RetAImpl with RetBImpl>.)
       new RetAImpl with RetBImpl {}
```

Now the type system gives an error as it's supposed to do. The difference between these two cases is the former just
means a type signature, while the latter tries to create a concrete class. And the cause is the compiler tries to be
too smart but fails.

This phenomenon divides into two problems:

1. Should we accept types like `A with B` with incompatible type among members?
1. If we should, then what `A with B` means?

