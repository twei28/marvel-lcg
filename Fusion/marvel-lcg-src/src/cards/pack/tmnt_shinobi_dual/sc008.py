from . import *

# Naito Dansā — EVENEMENT DUAL Kuji-Kiri/Ninjutsu, cout 2, [energy]. SPELL.
# Classe : « Kuji-Kiri;Ninjutsu ».
# Hero Action: Discard cards from the top of the encounter deck until you discard an attachment or side scheme. Reveal that
#   card -> cloak up to 2 friendly characters. Daze up to 2 enemies.
#
# Mots-cles (fiches lues AVANT le code) : Cloak (cloak.md, cloaked.md) ; Daze (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - « Discard cards from the encounter deck until you discard <X>. Reveal that card -> ... » : MEME PHRASE que
#    `alopex/ta006` Sniff Out Trouble (« until you discard a minion or side scheme. Reveal that card -> draw 2 cards... ») et
#    `sm/27015` Return the Favor (« until you discard a treachery. Reveal that treachery -> deal 5 damage ») : la revelation est
#    le COUT de la suite (`CostFunc.DiscardDeckTopUntil("EncounterDeck", type, "Reveal")` de 27015) ; ici le type est une UNION
#    (attachement OU manigance annexe), que `DiscardEncounterCardsUntil` ne sait pas rendre : meme boucle que `ta006`
#    (`Worlds.DiscardEncounterTopCard` bornee par la taille du deck), mais posee en COUT (`CostFunc.Custom`) ;
#  - « cloak up to 2 friendly characters » : `td005` Improvised Tactics (`Worlds.GetOnFieldFriendlyCharacters`,
#    `AskChooseFaces`) ; « daze up to 2 enemies » : `shinobi_paths/se010` (`ShinobiDaze`) avec choix de 0 a 2.
#
# TEXTE CONTRE CODE
#  ⚠ « until you discard AN ATTACHMENT OR SIDE SCHEME » : un attachement de RENCONTRE ou une manigance annexe de rencontre ;
#    les autres cartes sont defaussees au passage. Si le deck est epuise sans en trouver, rien n'est revele : le cout n'est pas
#    paye, ni cloak ni daze.
#  ⚠ « Reveal that card -> » : la revelation (attachement qui s'attache, manigance annexe qui entre en jeu, « When Revealed »)
#    est AVANT la fleche (cout) ; elle est resolue avant le camouflage / l'hebetement.
#  ⚠ « cloak UP TO 2 FRIENDLY characters » : de 0 a 2 personnages amis (identite et allies de tous les joueurs) ; « daze UP TO 2
#    enemies » : de 0 a 2 ennemis (vilain ou sbires) ; deux phrases independantes.
#  ⚠ « Hero Action » : forme heros seulement ; aucun libelle.


def GetAbilities() -> Sequence['Ability']:

    def defausser_jusqu_a_un_attachement_ou_une_manigance_annexe(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        trouvee = None
        taille = Worlds.GetEncounterDeck(effect).GetSize()
        for _ in range(taille):
            face = Worlds.DiscardEncounterTopCard(effect)
            if face is None:
                break
            if Attachment.IsType(face) or EncounterSideScheme.IsType(face):
                trouvee = face
                break
        if trouvee is None:
            return False
        return trouvee.Reveal(joueur, effect) is not None

    def naito_dansa(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        amis = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f.cloaked < f.cloaked_max]
        if amis:
            choisis = joueur.AskChooseFaces(amis, (0, min(2, len(amis))), effect,
                                            prompt="Cloak up to 2 friendly characters", not_move=True)
            if choisis:
                ShinobiCloak(effect, list(choisis))

        ennemis = [e for e in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not e.IsDefeated() and e.CanbeDazed()]
        if ennemis:
            choisis = joueur.AskChooseFaces(ennemis, (0, min(2, len(ennemis))), effect,
                                            prompt="Daze up to 2 enemies", not_move=True)
            if choisis:
                ShinobiDaze(effect, list(choisis))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            naito_dansa,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Custom(
            Select.From("This"),
            defausser_jusqu_a_un_attachement_ou_une_manigance_annexe,
        )),
    ]
