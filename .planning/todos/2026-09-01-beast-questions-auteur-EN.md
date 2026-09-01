# Message Discord pour l'auteur du pack BEAST (à copier-coller)

---

Hey! I've been implementing your **Beast (Hank McCoy)** pack for a digital
Marvel Champions engine, and I got the whole thing working: 23 cards, the
Discovery pool, the nemesis set, all of it. Really fun kit. The DEF 3 plus
Thick Skinned engine is a great idea, and it holds up in play.

Coding it forced me to read every line very literally, and a handful of things
came up where I had to make a judgement call. I'd rather ask than guess, so
here they are, grouped by type. None of it is blocking, the pack plays fine
with my readings, I just want to match your intent.

**Cards or names that don't seem to exist**

- **Unfinished Projects** says *"Discard 2 upgrade/support cards in play →
  remove **Mutation Degeneration** from the game"*, but there's no card by that
  name in the pack, and nothing puts one into play. Is it a missing card, or an
  older name for the obligation itself? I went with the second reading, so the
  first bullet removes the obligation from the game while the second one only
  discards it. That gives the two bullets a nice asymmetry, which is why it
  feels intentional.
- **Mutant Science Program** looks for *"the **Lizard-Fied Minion**"*, but the
  nemesis minion is called *Lizard-Fied Mutant**s***. Same card, right?
- Also on that one: what happens when the last test counter comes off? I left
  the side scheme in play, just no longer triggering, so you still have to
  thwart it down.

**Wordings that fight each other a bit**

- **In The Heat Of Battle** says *"**shuffle** 1 discovery card into your
  **hand**"*. You can't really shuffle into a hand, and Dr Hank McCoy says
  *"shuffle 1 random discovery card into your **deck**"*. Was this meant to be
  "add to your hand"? I kept the verb and sent it to the deck, but honestly
  "add to hand" feels like the stronger, more interesting payoff for emptying a
  scheme.
- **Multi-Tasking**: *"If this was the first card you played this turn → repeat
  this hero action."* Taken literally this never stops, since the condition is
  still true during the repeat, so it repeats forever. I capped it at one
  repeat, meaning the effect resolves twice total. Is that what you meant?
- **Fighting With Friends** is a *"Hero **Response**"* with no trigger, no
  "After...". A response with no window can never fire, so I treated it as a
  Hero Action. Was there a trigger that got lost along the way?
- **Ambush** is a *"**Forced** Interrupt"* on an event you play from hand, which
  is unusual. The closest official card, Grasping Tendrils, is a Hero Interrupt.
  I followed the printed word and made it truly forced, but I suspect you meant
  it to be optional?
- **Peter Parker** and **Hunter Gear** both say *"**Action**: ... generate a X
  resource"*. In MC that's normally worded *"Resource:"*, because as an Action
  the resource shows up outside of paying for a card, where it does nothing. I
  read both as "Resource".
- **Dr Hank McCoy**'s Setup, *"All cards you mulligan during setup are shuffled
  back into your deck"*, was the single hardest thing to build, since nothing in
  the engine normally lets a card react to the mulligan. Got it working, just
  flagging that it's the one ability with no precedent anywhere.

**Wordings with no "you control"**

These three don't say whose cards they mean, which only matters in multiplayer:

- **Experimental Warfare**: *"Exhaust **all upgrade cards in play**"*. Just
  yours, or the whole table's? Read literally, Beast taps everyone's gear to
  protect himself and the DEF bonus gets huge. I went with yours only.
- **Ambush**: *"exhaust **an support card in play**"*. Same question, and I went
  with one of yours.
- **Dark Beast**: *"**All allies** are confused."* Everyone's allies, or just
  the nemesis owner's? I went fully literal (everyone's), which makes him a real
  table threat and justifies those 3 boost icons, though nemesis sets usually
  only hit their own player.

**Two structural things**

- There are two card #1s: **Wonder Man (1/15)** and **Phoenix (1B/15)**. Same
  text, same stats, different traits (AVENGER vs PSIONIC. X-MEN). Is 1B a
  replacement, or a second ally? In other words, is the signature deck 15 cards
  or 16? I ended up offering both as two deck options so people can pick.
- **Multi-Tasking 6/15 has a mental resource and 7/15 has a physical one**, so
  they're not two copies of the same card. Fighting With Friends, Primal Rage
  and Alien Materials *are* identical pairs, so I assume this one is deliberate,
  but I wanted to check it isn't a copy-paste slip.

Thanks for making this, and for reading all that! Happy to share how any of it
ended up being implemented if that's useful.
