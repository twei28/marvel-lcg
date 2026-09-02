from . import *

# Mind-Hewn Blade — ATTACHEMENT NECROVERSE. WEAPON. +1 ATQ, 3 icones de boost.
#
# Attach to Gorr the God Butcher.
# [star] Forced Interrupt: When Gorr the God Butcher attacks you, discard the
#   top 2 cards of your deck. This attack gains piercing.
# Hero Action: Take 2 indirect damage and discard the top 2 cards of your deck
#   → discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Piercing` (mots-cles/piercing.md) : AUCUNE cle `desc`, toujours scripte.
#   Sur l'attaque en cours : `message.GainPiercing(effect)`
#   (sender_damage.py), modele 45182b.
# - Le `[star]` en tete de l'interruption est le marqueur d'une capacite
#   permanente (mots-cles/special.md) : ici il coiffe une Interruption
#   Obligatoire, donc le type reste `ForcedInterrupt`, l'etoile ne dit que
#   « c'est la capacite etoilee de la carte ».
# - `ATK+` : base automatique (`desc["ATK+"] = "1"`), aucun script.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Attachement pose sur un ennemi nomme : 07020 (Ball and Chain), 45107
#   (Apocalypse) — `AttachToFaceWhenPutIntoPlay(CardFinder(name=...))`.
# - « When X attacks you » : `WhenUnitAttackYou`, employe par 01132 (Melter).
# - Action de heros qui se defausse elle-meme : 07020,
#   `PlayerActionToDiscardThis(AbilityType.HeroAction)`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Gorr the God Butcher ATTACKS YOU » -> l'attaque doit viser le joueur
#   qui subit, d'ou `WhenUnitAttackYou` et non `WhenUnitWouldAttack`.
# « discard the top 2 cards of YOUR deck » -> le deck du joueur attaque.
# « THIS ATTACK gains piercing » -> l'attaque en cours, pas les suivantes.
# « Take 2 INDIRECT damage AND discard the top 2 » -> un cout a DEUX parties :
#   les deux doivent etre payees (piege « and remove » de PROCESSUS-CARTE).


def GetAbilities() -> Sequence['Ability']:

    def lame_taillee_dans_l_esprit(effect: 'Effect', message: 'Message.WhenUnitAttackYou') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        # ⚠ `WhenUnitWouldAttack` n'a PAS de `GetToPlayer` (c'est une methode
        # des messages de revelation) : le joueur attaque se lit
        # `GetAgainstPlayer()`, comme 40105a. Panne attrapee par le cas gb012
        # le 02/09/2026.
        joueur = message.GetAgainstPlayer()
        if joueur:
            joueur.DiscardDeckTopCards(2, effect)
        message.GainPiercing(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_GORR)
        ),
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.ForcedInterrupt,
            CardFinder(name=NOM_GORR),
            lame_taillee_dans_l_esprit,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.TakeIndirectDamage(2))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 2)),
    ]
