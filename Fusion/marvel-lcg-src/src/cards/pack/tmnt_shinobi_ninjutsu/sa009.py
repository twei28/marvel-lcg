from . import *

# * Twilight Sentry — AMELIORATION unique 1 [mental], Ninjutsu (TMNT Shinobi, Inkwire). TITLE. TRAINING.
# Attach to an ally you control and cloak them.
# Max 1 TRAINING upgrade per ally.
# Interrupt: When attached ally would take any amount of damage, discard a cloaked status card from them instead.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `ua004` Attack Training : « Attach to a ... ally. Max 1 TRAINING upgrade per ally » = `CanPlayThisUpgradeCard(CardFinder(...,
#    card_type=Ally))` (la limite TRAINING est NATIVE, lue sur le trait) ;
#  - `dt088` False Security : « Attach to X and give it a status card » = `AfterCardEnterPlay(ForcedResponse, "This", fn)` qui
#    lit `this.GetBindFace()` ;
#  - `19032` Regroup / `27087b` : « instead » = `message.SetBeInstead(effect)` ;
#  - `04004` Autodefenestration : `WhenUnitWouldTakeDamage` + `message.PreventDamage("All", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « an ally YOU CONTROL » : l'allie sous le controle du joueur (pas celui d'un autre) ; « and cloak THEM » : obligatoire,
#    a la pose (ForcedResponse), l'allie recoit une carte Cloaked s'il n'en a pas deja une.
#  ⚠ « Interrupt » (pas Hero) : aussi en forme alter-ego ; « WHEN attached ally WOULD take ANY AMOUNT of damage » : au
#    moins 1 degat, d'une attaque OU d'un autre effet, y compris consecutif ; « discard a cloaked status card FROM THEM
#    INSTEAD » : SANS la carte Cloaked, l'Interruption n'est pas proposee ; avec elle, TOUS les degats sont evites
#    (pas seulement 2) et la carte est defaussee.
#  ⚠ Unique (✦).


def GetAbilities() -> Sequence['Ability']:

    def allie_a_moi(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = Select.GetYou(effect)
        return face.GetControlByPlayer() == joueur

    def camoufler_l_allie(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        allie = this.GetBindFace()
        if allie is not None:
            ShinobiCloak(effect, allie)

    def sentry(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        allie = this.GetBindFace()
        if allie is None or not allie.IsCloaked():
            return
        # « instead » : le degat n'a pas lieu (`SetBeInstead`, comme `27087b`) ; le statut Cloaked, qui se lit lui-meme
        # sur ce message (`is_be_instead`), ne se declenche donc pas : une seule carte Cloaked est defaussee, par Sentry.
        message.SetBeInstead(effect)
        allie.DiscardCloaked(effect, rule=1)

    def allie_camoufle(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(message)
        allie = effect.this.GetBindFace()
        return allie is not None and allie.IsCloaked()

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally, check_effect_fn=allie_a_moi)
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            camoufler_l_allie,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "AttachedAlly",
            sentry,
            conditions=[allie_camoufle],
        ),
    ]
