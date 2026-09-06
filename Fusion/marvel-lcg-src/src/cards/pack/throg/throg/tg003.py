from . import *

# Great Courage — EVENEMENT, cout 2, [mental]. THWART. x2.
# Hero Action (thwart): Remove 2 threat from a scheme. Engage any number of
#   minions in play. For each minion engaged with you (to a maximum of 3),
#   remove 2 threat from a scheme.
#
# ⚠ LA CARTE QUI FAIT LE PACK. C'est elle qui explique pourquoi Throg attire
# les sbires : chaque sbire engage vaut 2 menaces de plus, jusqu'a 8 au total.
# Le prix est qu'ils sont tous sur lui a la phase du vilain.
#
# CARTES DE REFERENCE
#  - `42006` Natural Flight : « Hero Action (thwart): Remove N threat from a
#    scheme » -> `SetPlay().SetLabel('thwart').SetTarget(Scheme2)` puis
#    `this.RemoveThreatFromSchemes(effect.targets, N, effect)`.
#  - `br005` Star Jump : `minion.EngagePlayer(joueur, effect)`.
#  - `08013` / `16155` : le choix d'une SECONDE cible dans le corps, par
#    `joueur.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...))`.
#    C'est l'idiome du projet (RECETTES-MOTEUR §2, « Choix secondaire »).
#
# TEXTE CONTRE CODE
#  « Remove 2 threat from A SCHEME » (premiere phrase) -> UNE manigance au
#    choix, cible principale de la capacite. Pas « each scheme ».
#  « Engage ANY NUMBER of minions IN PLAY » -> zero compris, et « in play »
#    couvre les sbires engages avec un AUTRE joueur comme ceux qui ne sont
#    engages avec personne. Ce n'est pas « minions engaged with you » : la
#    phrase sert justement a en ramener.
#  ⚠ « For each minion engaged WITH YOU (to a maximum of 3) » -> le decompte
#    se fait APRES l'engagement, et il compte TOUS les sbires engages avec
#    vous, y compris ceux qui l'etaient DEJA avant la carte. Le texte ne dit
#    pas « engaged this way » — mot-piege « each », relu deux fois.
#  ⚠ « remove 2 threat from A SCHEME » (seconde phrase) -> repete pour chaque
#    sbire, donc UN CHOIX PAR SBIRE. Le joueur peut etaler sur plusieurs
#    manigances ou tout mettre sur la meme. C'est pour ca que la boucle
#    rouvre un `ChooseAbilities` a chaque tour, au lieu de multiplier la
#    valeur sur la cible principale.
#  « (to a maximum of 3) » -> plafond a 3 SBIRES, soit 6 menaces au maximum
#    pour la seconde phrase, 8 avec la premiere. Un quatrieme sbire engage
#    n'ajoute rien.


def GetAbilities() -> Sequence['Ability']:

    def grand_courage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        # « Remove 2 threat from a scheme. »
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # « Engage any number of minions in play. »
        sbires = [f for f in Worlds.FindCardsOnField(effect, CardFinder(card_type=Minion))
                  if f is not None and f.card.IsOnField()]
        if sbires:
            choisis = joueur.AskChooseFaces(
                sbires, (0, len(sbires)), effect,
                prompt="Engage any number of minions",
            )
            for sbire in choisis:
                sbire.CastTo(Minion).EngagePlayer(joueur, effect)

        # « For each minion engaged with you (to a maximum of 3), remove 2
        #   threat from a scheme. »
        engages = [m for m in joueur.GetEngagedMinions() if m is not None]
        for _ in range(min(len(engages), 3)):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    lambda cibles: this.RemoveThreatFromSchemes(cibles, 2, effect),
                ).SetTarget(Scheme2),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            grand_courage,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
