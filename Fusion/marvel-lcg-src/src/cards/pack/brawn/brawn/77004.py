from . import *

# Calculated Defense — custom « Rainy »
# Hero Interrupt: When Brawn defends against an attack, ready Brawn and draw 1
#   card (2 cards instead if Brawn did not ready this way.) If you played this
#   card from your hand using a [mental] resource, put this card into your
#   reserve.
#
# « ready Brawn and draw 1 card (2 instead if Brawn did not ready this way) » :
# un heros deja PRET ne se redresse pas, et c'est ce cas-la qui rapporte la
# seconde carte. On mesure donc l'etat AVANT de tenter le redressement.
#
# Le retour en reserve n'est PAS conditionne au fait d'avoir paye uniquement en
# [mental] : le texte dit « using a [mental] resource », donc au moins une.

def GetAbilities() -> Sequence['Ability']:

    def calculated_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)

        joueur = effect.GetInitiator()
        heros = joueur.GetHero()

        sest_redresse = False
        if heros is not None and heros.card.IsExhaust():
            Faces.ReadyAll([heros], effect)
            sest_redresse = True

        joueur.DrawUp(1 if sest_redresse else 2, effect)

        paye = effect.GetPaidResources()
        if paye.HasColor("B") and effect.context.play_from_area == joueur.hand_cards:
            RecyclerVersLaReserve(this, joueur, effect)

    return [
        # ⚠ `LimitOncePerEvent` est INDISPENSABLE ici, et c'est propre a cette
        # carte. Signale en partie reelle le 7/8/2026 : la carte payee en
        # [mental] depuis la main revient en RESERVE, or la reserve est une zone
        # « comme en main » — la carte y redevenait donc immediatement jouable,
        # DANS LA MEME fenetre de defense, qui n'etait pas encore refermee. Le
        # jeu reproposait « Play Calculated Defense » en boucle, et chaque tour
        # de boucle relancait la sequence d'attaque.
        #
        # Une carte ordinaire ne connait pas ce probleme : elle part en defausse
        # et cesse d'etre jouable. Toute carte du pack qui se recycle vers la
        # reserve pendant une fenetre de reaction doit donc borner son
        # declencheur. La limite est PAR EVENEMENT, pas par phase : deux
        # exemplaires differents restent jouables sur la meme defense, ce que le
        # texte imprime autorise (« 2 cards instead if Brawn did not ready »).
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            calculated_defense,
        ).SetPlay().SetLabel('defense').LimitOncePerEvent(),
    ]
