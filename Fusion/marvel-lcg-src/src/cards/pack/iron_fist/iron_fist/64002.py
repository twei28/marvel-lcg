from . import *

# Deep Breathing — EVENEMENT, cout 0, [mental]. SKILL. x3 (Iron Fist 1/15).
# Hero Action: Discard cards from the top of your deck until you discard an Iron Fist card
#   and add it to your hand.
#
# CARTES DE REFERENCE
#  - « Discard cards from the top of your deck until you discard X » : `Player.DiscardDeckUntil`
#    (fiche mots-cles/seek.md ; `venus/tv001b` Bonnie Setup, `sm001a`). La carte trouvee est
#    DEFAUSSEE par la primitive : l'ajouter en main est une etape separee (`Faces.AddToHand`).
#  - « an Iron Fist card » = une carte du set signature : `cyclops/33004` Field Commander
#    (« Cyclops upgrade » -> `CardFinder(set_name="Cyclops")`).
#  - evenement Hero Action sans libelle : `luke_cage/62003` Harlem's Hero (`.SetPlay()`).
#
# TEXTE CONTRE CODE
#  ⚠ « until you discard an IRON FIST card » -> `set_name == "Iron Fist"` (bandeau « IRON FIST
#    (n/15) ») : ni le nom, ni un trait. Une autre carte nommee « Iron Fist » (l'allie Lin Lie du
#    deck Protection, bandeau PROTECTION) ne l'arrete pas.
#  ⚠ « and add IT to your hand » : la carte trouvee, et elle seule ; les autres restent en defausse.
#  ⚠ Deck sans carte Iron Fist : tout le deck est defausse, rien n'est ajoute (decision n°4) ; le
#    deck epuise suit la regle du moteur (remelange, carte rencontre).
#  ⚠ Carte trouvee = derniere du deck : le moteur remelange aussitot la defausse ; la primitive la
#    rend quand meme (piege paye par venus), on la prend ou qu'elle soit.


def GetAbilities() -> Sequence['Ability']:

    def deep_breathing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = joueur.DiscardDeckUntil(effect, set_name=SET_IRON_FIST)
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deep_breathing,
        ).SetPlay(),
    ]
