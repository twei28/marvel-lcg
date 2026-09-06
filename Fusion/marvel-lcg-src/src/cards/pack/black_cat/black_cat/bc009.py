from . import *

# Grappling Hook — AMELIORATION, cout 1, [physical]. ITEM. x2.
# Hero Action: Exhaust Grappling Hook and discard a card tucked under
#   Black Cat -> ready Black Cat and tuck the top card of the encounter deck
#   under her.
#
# ⚠ HOMONYME : « Grappling Hook » est DEJA `08008` (amelioration de Black
# Widow) et `50069` (attachement de Black Widow). Celle-ci est la TROISIEME.
# Le texte francais s'ecrit sur le `card_id`, jamais sur le nom.
#
# CARTES DE REFERENCE
#  - `sn005` Web Swinging (pack spider_man_noir) : le meme cycle exactement —
#    defausser une carte glissee pour redresser, puis en reglisser une. Une
#    carte nette en moins puis une en plus, la pile revient a son niveau.
#  - `31009` / `an001a` : `Faces.ReadyAll`.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX COUTS devant la fleche : incliner ET defausser une carte glissee.
#  ⚠ ET LE COUT SE PAIE SUR LA MEME PILE QUE L'EFFET REMPLIT. L'ordre compte :
#    on defausse d'abord (cout), on reglisse ensuite.
#  ⚠ `PileNonVide` en condition d'offre : sans elle, l'arme s'inclinerait et
#    ne redresserait rien (piege `sn005`, RECETTES §5). La carte est donc
#    inutile au tout premier tour, et c'est voulu.
#  « ready BLACK CAT » -> la face HEROS. ⚠ Le filtre est le TYPE, jamais le
#    nom : trois cartes du depot s'appellent « * Black Cat ». « Hero Action »
#    confirme d'ailleurs qu'on est en forme heros.
#  « tuck the top card ... UNDER HER » -> la meme pile, celle de l'identite.
#  « the top card of the encounter deck » -> seconde phrase, inconditionnelle
#    tant qu'il reste une carte. Deck vide, on ne glisse rien et le
#    redressement a quand meme eu lieu.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def grappin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

        face = Worlds.DiscardEncounterTopCard(effect)
        if face is not None:
            GlisserSousIdentite(effect, [face], joueur)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            grappin,
            conditions=[PileNonVide],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee)),
    ]
