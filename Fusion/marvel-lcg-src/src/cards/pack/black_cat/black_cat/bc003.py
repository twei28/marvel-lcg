from . import *

# * Spider-Man (Peter Parker) — ALLIE, cout 3, [wild]. AVENGER.
#   PV 3, CTR 2, ATQ 2.
# Multiverse. Enters play with 2 web counters.
# Interrupt: When an enemy activates, remove 1 web counter from here and
#   discard a card tucked under your identity -> cancel that activation.
#
# MOT-CLE : MULTIVERSE — fiche `docs/reference/mots-cles/multiverse.md`,
# CREEE POUR CE PACK (le mot etait employe par TROIS auteurs et defini par
# AUCUN). Marqueur de DECKBUILDING, **zero ligne de code** : c'est l'unicite
# native qui interdit d'avoir deux versions de Spider-Man en jeu.
# ⚠ A ne pas confondre avec le TRAIT `MULTIVERSE` de `wd029`.
#
# ⚠ CETTE CARTE ET `bc002` PORTENT LE MEME NUMERO DE SET (« 1/15 ») et le meme
# NOM. Ce sont deux cartes differentes : PV 3 contre 4, AVENGER contre
# SYMBIOTE + WEB-WARRIOR, et deux capacites sans rapport.
#
# CARTES DE REFERENCE
#  - `av002` * Spider-Man (pack agent_anti_venom) : MOT POUR MOT l'annulation
#    d'activation — `WhenEnemyWouldActivate` + `SetBeInstead`, qui couvre d'un
#    coup l'attaque ET la manigance. Montage d'origine : `27006` Web Binding.
#  - `AbilityFactory.ThisEnterPlayWithCounters` (factory/counter.py:6) pour
#    « enters play with 2 web counters ».
#
# TEXTE CONTRE CODE
#  ⚠ DEUX COUTS devant la fleche : retirer un pion toile ET defausser une
#    carte glissee. Oublier le second rendrait l'annulation gratuite deux fois
#    par partie au lieu de la payer sur la pile (piege `wd005`).
#  ⚠ ET LE SECOND COUT EXIGE UNE CONDITION D'OFFRE. `CostFunc.Counter` sait
#    se rendre indisponible tout seul : son selecteur porte `has_enough_counter`
#    (cost_func.py:802), donc pion vide, la capacite n'est pas proposee.
#    `CostFunc.Custom`, lui, NE SAIT PAS : `HasTargets` (cost_func.py:47) rend
#    True des que le selecteur a une cible, or `Custom(None, ...)` se rabat sur
#    `Select.From("This")`, la carte elle-meme. Sans `PileNonVide`, la capacite
#    serait proposee pile vide, l'activation ne serait PAS annulee et le pion
#    toile serait perdu. Constate le 05/09/2026 sur `sn005`, RECETTES §5.
#    La condition sur le pion est gardee malgre tout : deux gardes valent mieux
#    qu'une quand l'une des deux est implicite.
#  ⚠ « When AN ENEMY activates » -> vilain OU sbire, sans filtre ELITE. C'est
#    plus large que `av002`, qui se limite aux sbires non-ELITE : ne pas
#    recopier la condition de la carte de reference.
#  « a card tucked under YOUR IDENTITY » -> la pile de l'identite, pas une
#    carte posee sous l'allie.
#  ⚠ Le compteur `web` EXISTE DEJA dans l'enum `COUNTER` (card_face.py:156) :
#    aucun correctif moteur n'est necessaire, contrairement a `foe` pour throg.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def il_reste_un_pion(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        Unused(message)
        return effect.this.CastTo(CanPlaceCounter).GetCounters('web') > 0

    def toile_daraignee(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        message.SetBeInstead(effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'web'),
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.Interrupt,
            None,
            toile_daraignee,
            conditions=[il_reste_un_pion, PileNonVide],
        ).SetCostFunc(CostFunc.Counter("This", 1, 'web'))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee)),
    ]
