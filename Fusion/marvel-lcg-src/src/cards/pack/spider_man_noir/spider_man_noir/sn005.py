from . import *

# Web Swinging — EVENEMENT, cout 0, [energy]. SUPERPOWER. x3.
# Hero Response: After Spider-Man Noir uses a basic power, discard a card
#   tucked under Spider-Man Noir -> ready Spider-Man Noir. Discard the top
#   card of the encounter deck and tuck it under Spider-Man Noir (to a
#   maximum of 3).
#
# CARTES DE REFERENCE
#  - `14001a` * Quicksilver / `tg001a` : `AfterUnitUseBasicPower` avec
#    `powers=["ATK","THW","DEF"]`, puis `Faces.ReadyAll`.
#  - `10003` Hulk Smash : l'evenement joue en reaction -> `.SetPlay()`.
#  - `15004` : `Worlds.DiscardEncounterTopCard`.
#
# TEXTE CONTRE CODE
#  « After SPIDER-MAN NOIR uses a basic power » -> la face HEROS. ⚠ Le filtre
#    est `"YourHero"`, pas le nom : deux ALLIES du depot s'appellent
#    « Spider-Man Noir ». La RECUPERATION de Peter Parker n'est pas couverte,
#    et « Hero Response » le confirme.
#  ⚠ « discard a card tucked under Spider-Man Noir » est DEVANT LA FLECHE :
#    c'est un COUT. Pile vide, la carte n'est pas jouable — ce qui la rend
#    inutile au tout premier tour, et c'est voulu : le heros doit d'abord
#    remplir sa pile.
#  ⚠ ET LE COUT SE PAIE SUR LA MEME PILE QUE L'EFFET REMPLIT. L'ordre compte
#    donc : on defausse d'abord (cout), on reglisse ensuite. Une carte nette
#    en moins puis une en plus : la pile revient a son niveau, et c'est ce qui
#    rend le cycle soutenable.
#  « READY Spider-Man Noir » -> il vient d'utiliser un pouvoir de base, donc
#    il est incline ; c'est le redressement qui prouve que la Reponse est
#    partie.
#  « Discard the top card ... and tuck it » -> seconde phrase, inconditionnelle
#    tant qu'il reste une carte au deck de rencontre. Deck vide, on ne glisse
#    rien et la carte a quand meme redresse.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def balancement(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

        face = Worlds.DiscardEncounterTopCard(effect)
        if face is not None:
            GlisserSousIdentite(effect, [face], joueur)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "YourHero",
            balancement,
            powers=["ATK", "THW", "DEF"],
            conditions=[PileNonVide],
        ).SetPlay()
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee)),
    ]
