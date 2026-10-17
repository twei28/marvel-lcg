from . import *

# * Stealth Fighter (Raph) — ALLIE double aspect Justice/Leadership (Inkwire, TMNT Aspects).
# Cout 4, PV 2, THW 1 / ATK 1 (1 degat consecutif chacun), ressource [physical].
#
# Response: After Stealth Fighter enters play or takes consequential damage ([consequential]),
#   cloak him.
# Interrupt: After Stealth Fighter is defeated by consequential damage ([consequential]), cloak a
#   friendly character.
#
# Cartes de reference :
#  - Cloak : fiche mots-cles/cloak.md (`Faces.GiveStatus([X], "Cloaked", effect)`), tl016 ;
#  - « After X enters play » : `AfterCardEnterPlay(Response, "This", ...)` ;
#  - « After X takes consequential damage » : 19012 Martyr (`AfterAllyTakeConsequentialDamage`) ;
#  - « defeated by consequential damage » : 30021 SP//dr (`WhenUnitBeDefeated(...,
#    by_consequential=True)`) ;
#  - « cloak a friendly character » : td005 (`Worlds.GetOnFieldFriendlyCharacters`,
#    `AskChooseFaces`).
#
# ⚠ QUESTION OUVERTE Q-UD3 (.planning/tmnt/aspects-dual-aspect-questions.md) : « Interrupt: AFTER
#   ... is defeated » est contradictoire (coquille du meme type que The Made Men). Lecture
#   provisoire = l'option recommandee : une Interruption « When Stealth Fighter is defeated by
#   consequential damage » (meme tournure que Rōnin, Doomsayer, Sōhei du meme pack) ; un allie
#   vaincu a quitte le jeu, une Reponse « after » n'aurait plus de carte pour la porter.
#   Carte NON terminee tant que la question n'est pas tranchee.
#
# Mots-pieges : « cloak HIM » (lui-meme) ; « enters play OR takes consequential damage » (deux
# declencheurs, une seule capacite imprimee : deux montages ici) ; « takes » = degats reellement
# subis (Tenace les empeche, cf. 19012) ; vaincu par ces degats, il n'est plus la pour etre cloake ;
# « a FRIENDLY character » : identites et allies de tous les joueurs, sauf lui-meme (il quitte le
# jeu : sa carte d'etat partirait avec lui).


def GetAbilities() -> Sequence['Ability']:

    def se_camoufler(effect: 'Effect', message: 'Message') -> None:
        Unused(message)
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Cloaked", effect)

    def camoufler_un_ami(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        amis = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f != effect.this]
        if not amis or joueur is None:
            return
        choisis = joueur.AskChooseFaces(amis, (1, 1), effect,
                                        prompt="Cloak a friendly character", not_move=True)
        if choisis:
            Faces.GiveStatus(choisis, "Cloaked", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            se_camoufler,
        ),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            se_camoufler,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            camoufler_un_ami,
            by_consequential=True,
        ),
    ]
