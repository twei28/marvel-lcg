from . import *

# * Hyper-Cosmic Awareness — AMELIORATION signature, custom « jakxin »
# Cout 2, [mental], trait SUPERPOWER.
#
# Hero Response: After you play a [[SUPERPOWER]] card, place 1 star counter
#   on this card.
# Hero Interrupt: When an encounter card is revealed, exhaust this card and
#   remove 4 star counters from it → cancel all of its effects and discard it.
#
# ---------------------------------------------------------------------------
# LE COMPTEUR `star`
#
# Declare dans le `Literal` `CardFace.COUNTER` (card_face.py:209-212,
# commentaire `# CORRECTIF`). Sans cette entree, `IsCounter` refuse le nom et
# la construction de la carte PLANTE.
#
# ---------------------------------------------------------------------------
# CAPACITE 1 — ACCUMULER
#
# Carte de reference : `mk005` Different Folks (pack moon_knight), meme
# structure « une Response qui pose 1 compteur ici, une Action qui en depense
# N ». Meme `Faces.PlaceCountersOn([this], 1, <nom>, effect)`
# (faces.py:205-212).
#
# Le declencheur est le MEME que Star-Gaze (`AfterPlayerPlayedCard`,
# `CardFinder(trait=SUPERPOWER)`, `"You"`), et c'est voulu : les deux
# capacites lisent le meme evenement. Mais ce sont deux capacites
# INDEPENDANTES — Hyper-Cosmic Awareness compte meme si Star-Gaze ne resout
# rien, parce que son texte parle de « jouer une carte SUPERPOWER », pas de
# « resoudre Star-Gaze » (contrairement a ma002 Alloy).
#
# ---------------------------------------------------------------------------
# CAPACITE 2 — ANNULER
#
# Cartes de reference : `40048` Lucky Break (pack next_evol) et `mw009`
# Foresight (pack madame_web). Toutes deux
# `WhenPlayerRevealCard(<type>, <joueur>, <carte>, "All", fn)` puis
# `message.CancelAllEffectsAndDiscardIt(effect)`.
#
# ⚠ LE NIVEAU « All » (reveal.py:41) — leçon Dazzler n°5 : « cancel ALL of
# its effects » annule TOUT, y compris les mots-cles et le SURGE de la carte
# rencontre. Le niveau `"WhenRevealed"` n'annulerait que la capacite « Une
# fois revelee » et laisserait passer le deferlement. Le texte imprime dit
# bien « all of its effects ».
#
# ECART DOCUMENTE — LA PORTEE. Le texte dit « When AN ENCOUNTER CARD IS
# REVEALED », sans « you » ni « against you » : on ne restreint donc pas au
# joueur qui controle la carte (`"AnyPlayer"`). `mw009` dit « When YOU reveal
# an encounter card » et emploie `"You"` : deux textes differents, deux
# portees differentes, on ne recopie pas l'une sur l'autre (mot-piege
# `against you` / `your` du PROCESSUS-CARTE §5). En solo la difference est
# nulle ; en multijoueur Ms. America peut proteger un coequipier, ce que le
# texte autorise.
#
# ⚠ PAS de `.SetPlay()` ni de `.SetLabel()` ici, contrairement a `mw009` :
# celle-la est un EVENEMENT joue depuis la main, celle-ci une amelioration
# DEJA EN JEU. `Ability.Initialize` (ability.py:196) n'accepte de toute facon
# que 'defense' et 'thwart' comme libelles d'une interruption, et la carte
# n'en imprime aucun (piege paye sur `pt015`).
#
# LE COUT A DEUX PARTIES, LES DEUX SONT PAYEES (mot-piege « and remove » du
# PROCESSUS-CARTE §5) : `CostFunc.Exhaust("This")` ET
# `CostFunc.Counter("This", 4, 'star')`. `CostFunc.Counter` filtre
# lui-meme les porteurs qui n'ont pas assez de compteurs
# (`has_enough_counter`, cost_func.py:802-816) : MOINS DE 4 COMPTEURS =
# CAPACITE INJOUABLE, sans une ligne de garde a ecrire. Deux `.SetCostFunc`
# chaines, idiome de `06017` (exhaust + 3 compteurs 'glory') et de `pt008`.


def GetAbilities() -> Sequence['Ability']:

    def compter(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, COMPTEUR_STAR, effect)

    def annuler(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.CancelAllEffectsAndDiscardIt(effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(trait=TRAIT_SUPERPOWER),
            compter,
        ),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            EncounterCard,
            "All",
            annuler,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", COMPTEURS_POUR_ANNULER, COMPTEUR_STAR)),
    ]
