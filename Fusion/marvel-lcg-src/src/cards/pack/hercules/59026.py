from . import *
def GetAbilities() -> Sequence['Ability']:
    def ancient_rivalry(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=False, include_discard_pile=True, may=True, finder=CardFinder(card_type=Upgrade, card_class='IdentitySpecific'))
        if face:
            Faces.AddToHand([face], initiator, effect)
        # ⚠ « Ready Hercules and Thor » VISE AUSSI LES ALLIES (17/09/2026).
        # Signale en jeu : « Rivalite Antique ne redresse pas Thor quand il est
        # sur le terrain avec Hercule ». On ne cherchait qu'un HEROS nomme
        # Thor : en solo il n'y en a pas, et l'allie 59020 « * Thor Odinson »
        # restait incline.
        #
        # Or c'est LUI qui rend la carte jouable. Le mot-cle Team-Up exige que
        # les deux personnages nommes soient en jeu, « identity OR ally »
        # (has_teamup.py, en-tete), et le moteur bloque la carte sinon. Les
        # unites qui AUTORISENT la carte sont donc exactement celles qu'elle
        # redresse : `GetTeamUpUnits()` les rend, et c'est la seule liste qui
        # ne puisse pas diverger de la condition de jeu.
        #
        # Carte de reference : al023 Little Rascals, meme famille, qui redresse
        # deja parmi les personnages amis en jeu sans filtrer sur le type.
        Faces.ReadyAll(this.GetTeamUpUnits(), effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, ancient_rivalry).SetPlay().SetLabel().SetTarget('TeamUp')]
