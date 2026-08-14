from . import *

# Power Surge (2B)

def GetAbilities() -> Sequence['Ability']:

    def icone_dacceleration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # La carte porte une ICONE D'ACCELERATION imprimee.
        #
        # ⚠ ECART DE FORME, ecrit : `Acceleration` est un attribut de manigance
        # SECONDAIRE, de sbire ou d'environnement — `MainScheme` n'herite pas de
        # `HasAccelerationIcon`, et le moteur refuse de generer la carte si on
        # le lui donne (`KeyError('Acceleration')`).
        #
        # Un JETON d'acceleration fait exactement le meme travail : l'escalade
        # du complot principal additionne les deux (`scheme_main.py`, les
        # `acceleration_tokens` rejoignent les `acceleration_icons`), et le
        # « for each acceleration token and icon in play » que comptent
        # Power Outage, Accelerated Plans et Dark Matter Conversion le voit
        # aussi. On le pose donc a la revelation du stade.
        effect.this.CastTo(CanAccelerationToken).PlaceAccelerationToken(1, effect)

    def est_une_traitrise_electro(effect: 'Effect', message: 'Message.AfterCardRevealed') -> bool:
        return Treachery.IsType(message.trigger) and \
            message.trigger.paper.set_name == "Electro"

    def retirer(effect: 'Effect', message: 'Message.AfterCardRevealed') -> None:
        # « [star] Forced Response: After you resolve an Electro treachery,
        # remove that treachery from the game. »
        #
        # Le deck rencontre s'asseche a mesure : chaque traitrise du set jouee
        # ne revient plus, et la partie devient une course.
        Faces.RemoveAllFromGame([message.trigger], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            icone_dacceleration
        ),
        # ⚠ `AfterYouResolveTreachery` compare `effect.GetInitiator()` au joueur
        # qui revele, et cette methode EXIGE un joueur. L'initiateur du complot
        # principal est le VILAIN : la fabrique levait une assertion a chaque
        # traitrise resolue. L'abilite est donc construite a la main, sans le
        # filtre « you » — sur un complot principal, tous les joueurs sont
        # concernes de toute facon.
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterCardRevealed,
            [est_une_traitrise_electro],
            retirer,
        ),
        # « If this stage is completed, the players lose the game. »
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
