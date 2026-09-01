from . import *

# Doombot — allie signature, x2. TECH. Cout 1, 2 PV, ATQ 2*, CTR « — ».
# Requirement ([mental]). Toughness.
# Interrupt: When an enemy attacks you, play Doombot from your hand (paying
#   its resource cost) and declare it the defender without exhausting it.
#
# Carte de reference : 45031 * Colossus (pack aoa), JUMEAU EXACT — meme texte
# au nom pres. Son montage est donc repris tel quel :
#  - `CanPlayThisAllyCard()` — le commentaire du moteur est explicite :
#    « Without this, this ally cannot be play ». C'est ce qui manquait a la
#    premiere version de ce module : le pilote ne voyait qu'une option
#    « Defense » et Doombot n'etait jamais propose (trace le 01/09/2026) ;
#  - `WhenUnitBeingAttack(Interrupt, "You", Enemy, op).SetPlay()` — et NON
#    `WhenUnitInitiatesAttackAgainst`, qui se declenche trop tot pour declarer
#    un defenseur ;
#  - `initiator.PlayCardsLikeInTurn([this], effect, ignore_resources_cost=True,
#    forced=True)` : la carte est jouee DEPUIS la fenetre d'interruption. Le
#    cout a deja ete paye au declenchement, d'ou `ignore_resources_cost` ;
#  - `message.DeclareDefender(this, effect)`, garde par `this.IsInPlay()` : si
#    la mise en jeu echoue, on ne declare pas un defenseur fantome.
#
# ⚠ `DeclareDefender` N'INCLINE PAS de lui-meme (32017 Mutant Protectors
# appelle `Faces.ExhaustAll` juste avant, parce que SA carte incline). Ne rien
# appeler ici, c'est tout le sens de « without exhausting it ».
#
# ⚠ `Requirement ([mental])` est un mot-cle OFFICIEL, base automatique lue dans
# `desc.Requirement` (has_cost.py:24) : AUCUN module. 8 cartes officielles
# l'emploient, dont 27006 Web Binding, dont le script ne le mentionne pas non
# plus. Fiche : docs/reference/mots-cles/requirement.md.
# ⚠ A ne pas confondre avec « If you paid for this card using only [mental]
# resources » (dd004, dd005, dd006), qui est une condition d'EFFET.
#
# ⚠ « Toughness » est lu dans `desc` : aucun module non plus.
#
# ⚠ CTR imprime « — » (tiret) et non 0 : Doombot ne peut pas contrer du tout.
# La convention du moteur est d'OMETTRE la cle `THW` (9 allies officiels le
# font, dont 01050 * Hulk) — surtout pas `"THW": "-"`, qui leve
# `ValueError: invalid literal for int() with base 10: '-'` des la mise en
# place. A ne pas confondre avec `"THW": "0"` (44013 Dogpool), qui signifie
# « contre pour 0 », pas « ne contre pas ».

def GetAbilities() -> Sequence['Ability']:

    def doombot(effect: 'Effect', message: 'Message.WhenUnitBeingAttack') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.PlayCardsLikeInTurn([this], effect,
                                      ignore_resources_cost=True, forced=True)
        if this.IsInPlay():
            message.DeclareDefender(this, effect)

    return [
        # Sans ceci, l'allie ne peut PAS etre joue (commentaire du moteur sur
        # 45031, verifie : le pilote ne proposait que « Defense »).
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitBeingAttack(
            AbilityType.Interrupt,
            "You",
            Enemy,
            doombot,
        ).SetPlay(),
    ]
