from . import *

# Black Webbing — EVENEMENT, cout 1, RES [mental]. SUPERPOWER.
# Hero Action: Choose a minion engaged with another player -> stun and engage
#   that enemy.
#
# CARTE DE REFERENCE
#  - `tg002` Airborne Amphibian (pack throg, maison) : « choose a minion
#    engaged with another player and engage it ». MEME phrase, meme parcours
#    des autres joueurs par `Worlds.GetPlayers` puis `GetEngagedMinions`.
#
# TEXTE CONTRE CODE
#  ⚠ « engaged with ANOTHER PLAYER » : ni « in play », ni « engaged with
#    you ». EN SOLO LA CARTE NE FAIT JAMAIS RIEN, et c'est le texte qui le
#    veut, pas une panne — lecon deja payee sur `tg002`, dont le contre-cas
#    solo existe pour cette raison.
#  ⚠ « STUN AND ENGAGE » : les deux, dans cet ordre. Le sbire est etourdi
#    AVANT de changer de joueur, ce qui ne change rien au resultat mais suit
#    l'ordre imprime.
#  ⚠ Le choix n'est pas optionnel (« Choose », pas « You may choose ») : on
#    passe par `ChooseAbilities`, non par `MayChooseFace`. C'est l'ecart avec
#    `tg002`.
def GetAbilities() -> Sequence['Ability']:

    def black_webbing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        candidats: List['CardFace'] = []
        for autre in Worlds.GetPlayers(effect):
            if autre is joueur:
                continue
            for sbire in autre.GetEngagedMinions():
                if sbire is not None and sbire.card.IsOnField():
                    candidats.append(sbire)
        if not candidats:
            return

        def voler(cibles: Sequence['CardFace']) -> None:
            Faces.GiveStatus(list(cibles), "Stunned", effect)
            for sbire in cibles:
                sbire.CastTo(Minion).EngagePlayer(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun and engage that minion", voler,
            ).SetTarget(candidats, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            black_webbing
        ).SetPlay(),
    ]
