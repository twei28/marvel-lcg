from . import *

# Sniff Out Trouble (x2) — EVENEMENT, cout 1, [mental].
# Hero Action: Discard cards from the encounter deck until you discard a minion
#   or side scheme. Reveal that card -> draw 2 cards and ready each [[KAMA]]
#   upgrade you control.
#
# Cartes de reference :
#  - « discard from the encounter deck until » : `Worlds.DiscardEncounterTopCard`
#    (worlds.py:581) en boucle, bornee par le deck ; `DiscardEncounterCardsUntil`
#    n'accepte pas une UNION de types (minion OU manigance annexe) ;
#  - « Reveal that card » depuis la defausse rencontre : `ho014` / `ss019`,
#    `face.Reveal(joueur, effect)` ;
#  - « ready each [[KAMA]] upgrade you control » : `Faces.ReadyAll` sur
#    `joueur.GetControlUpgrades`-equivalent (`Worlds.FindCardsOnField` filtre).
#
# Mots-pieges :
#  - « minion OR SIDE SCHEME » : un sbire ou une manigance annexe de
#    RENCONTRE ; les autres cartes sont defaussees au passage ;
#  - « Reveal that card -> » : la revelation est le COUT de la suite. Si le
#    deck est epuise sans avoir trouve de sbire ni de manigance, rien n'est
#    revele et rien n'est pioche (cout non paye) ;
#  - « draw 2 cards AND ready EACH [[KAMA]] upgrade YOU CONTROL » : les deux,
#    uniquement les Kama du joueur ;
#  - la carte revelee est resolue (Une fois revelee, sbire engage, manigance
#    en jeu) AVANT la pioche ;
#  - Action NUE de heros (« Hero Action »), sans label.


def GetAbilities() -> Sequence['Ability']:

    def sniff_out_trouble(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        trouvee = None
        taille = Worlds.GetEncounterDeck(effect).GetSize()
        for _ in range(taille):
            face = Worlds.DiscardEncounterTopCard(effect)
            if face is None:
                break
            if Minion.IsType(face) or EncounterSideScheme.IsType(face):
                trouvee = face
                break
        if trouvee is None:
            return

        trouvee.Reveal(joueur, effect)
        joueur.DrawUp(2, effect)
        kamas = [f for f in Worlds.FindCardsOnField(
                     effect, card_type=Upgrade, trait=TRAIT_KAMA)
                 if f.GetControlByOrOwner() is joueur]
        if kamas:
            Faces.ReadyAll(kamas, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sniff_out_trouble,
        ).SetPlay(),
    ]
