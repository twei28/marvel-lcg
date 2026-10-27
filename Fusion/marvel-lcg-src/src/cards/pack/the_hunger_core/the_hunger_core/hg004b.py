from . import *

# The Devourer's Skin — MANIGANCE PRINCIPALE, stade 1, face B. Starting threat 1[per_hero]. Escalade +1[per_hero]
# (★). Seuil 9[per_hero].
# Forced Interrupt: When The Hunger Core would be defeated, instead advance to stage 2 of the main scheme and
# put the next stage of The Hunger Core into play.
# If this scheme is completed, the players lose.
#
# Cartes de reference :
#  - « instead advance to stage 2 ... and put the next stage ... into play » (« Deeper Inside », livret page
#    5) : `AbilityFactory.WhenUnitWouldBeDefeated` + `message.SetBeInstead(effect)`, puis
#    `effect.world.AdvanceMainScheme(this, None, effect)` (modele Klaw 01116b/01117b : deux stades simples,
#    pas de saut comme AvP) et `coeur.Advance(effect, to_villain=commun.ProchainStadeDuCoeur(...))`.
#  - « If this stage is completed, the players lose the game » : `AbilityFactory.WhenMainSchemeStageWouldBeCompleted`
#    + `Worlds.SetGameOver(False, effect)`, modele AvP `PerdQuandAccompli` (`ap005b.py`).
#
# ⚠ Mots-pieges :
#  - « instead » ANNULE la defaite du Coeur (`SetBeInstead`) : la progression de stade du VILLAIN que le moteur
#    ferait automatiquement sur une vraie defaite (`Villain.OnBeDefeated` -> `self.Advance()`) NE PART PAS
#    toute seule ici, elle doit etre rejouee a la main avec `to_villain` explicite.
#  - Rupture (hg001-hg003) peut vaincre le Coeur MEME avec des Metazombies en jeu (FAQ page 8) : ce Forced
#    Interrupt se declenche pareil, aucune condition sur le nombre de Metazombies a coder ici.
#  - la manigance avance vers hg005a (stade 2), PAS vers un stade choisi : `to_face=None` suffit (un seul
#    stade suivant dans `main_schemes_deck`, comme Klaw).
#  - hg005a (stade 2, face A) N'A AUCUNE menace imprimee : le moteur generique l'auto-avance IMMEDIATEMENT
#    sur hg005b des sa revelation (`MainScheme.OnAfterCardRevealedEnd`, « printed_target_threat == None » ->
#    auto-`Advance`). L'etat observable APRES ce Forced Interrupt est donc deja hg005b (son « When Revealed »
#    -- Inside Galactus + 2 Metazombies -- a deja resolu), jamais hg005a toute seule. Mesure le 27/10/2026,
#    confirmee par substitution : hg005a est la MEME regle qui a deja fait passer hg004a -> hg004b a la mise
#    en place (hg004a non plus n'a pas de menace imprimee).


def GetAbilities() -> Sequence['Ability']:

    def deeper_inside(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        message.SetBeInstead(effect)

        this = effect.this.CastTo(MainScheme)
        effect.world.AdvanceMainScheme(this, None, effect)

        coeur = message.trigger.CastTo(Villain)
        prochain = ProchainStadeDuCoeur(effect, coeur)
        if prochain is not None:
            coeur.Advance(effect, to_villain=prochain)

    def perdu_si_accompli(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        Unused(effect)
        message.SetBeInstead(effect)
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            CardFinder(name=CORE, card_type=Villain),
            deeper_inside,
        ),
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.WhenCompleted, "This", perdu_si_accompli),
    ]
