from . import *

# Thunderstrike — EVENEMENT, cout 3, [energy]. SUPERPOWER. x2.
# Requirement ([energy]).
# Hero Action: Choose a player -> deal 3 damage to the villain and each minion
#   engaged with that player. Stun each enemy damaged this way.
#
# MOT-CLE : REQUIREMENT — fiche `docs/reference/mots-cles/requirement.md`.
# C'est une BASE AUTOMATIQUE : la cle `desc.Requirement` vaut `"Y"` et le
# moteur la lit seul. AUCUN script ne doit la recoder.
#
# TEXTE CONTRE CODE
#  « the villain AND each minion engaged with THAT PLAYER » -> le vilain est
#    touche quel que soit le joueur choisi ; seuls les SBIRES dependent du
#    choix. Frapper « chaque ennemi » serait plus fort en multijoueur.
#  « STUN EACH ENEMY DAMAGED THIS WAY » -> uniquement ceux qui ont pris les
#    degats. Un sbire deja vaincu par ces 3 degats n'est plus la pour etre
#    etourdi, et le moteur l'ecarte de fait.
#  ⚠ AUCUN libelle `(attack)` sur le scan : ce n'est PAS une attaque, elle ne
#    consomme donc pas l'action d'attaque du tour et ne declenche ni Riposte
#    ni defense. `SetLabel` serait une invention.
#
# ⚠ LE CIBLAGE EST UN LITTERAL DU MOTEUR, ET J'EN AVAIS INVENTE UN.
# Une premiere version ecrivait `SetTarget("EachPlayerIdentity")`, qui
# n'existe nulle part dans le moteur — `test_cards` construit pourtant la
# carte SANS BRONCHER, la chaine n'etant validee qu'a la selection. Le bon
# litteral est `"VillainAndEngagedSamePlayerMinion"` (modeles `42029` Bombs
# Away, `04006`, `ho004`), et il rend EXACTEMENT la phrase imprimee : le
# choix du joueur est DANS le selecteur, et `effect.targets` arrive deja
# rempli du vilain et des sbires engages avec lui. Le §6 des recettes le
# documente depuis le pack harry_osborn.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_tonnerre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        ennemis = list(effect.targets)
        if not ennemis:
            return
        this.DealDamage(ennemis, 3, effect)
        # « STUN EACH ENEMY DAMAGED THIS WAY » : ceux que les 3 degats ont
        # vaincus ne sont plus la pour etre etourdis, d'ou le filtre.
        vivants = [e for e in ennemis if e.IsInPlay()]
        if vivants:
            Faces.GiveStatus(vivants, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            coup_de_tonnerre,
        ).SetPlay()
        .SetTarget("VillainAndEngagedSamePlayerMinion"),
    ]
