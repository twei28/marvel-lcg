from . import *

# * Karaoke Night
# PARTY.
# Action: Exhaust Karaoke Night and choose a SONG in the Setlist -> resolve the
#   'Hero Action' of that card. Discard that card.
#
# Le pendant de « Rehearsal » : la ou le heros resout le « Showtime! » d'une
# chanson de la Setlist, cette carte y rejoue son « Hero Action ». Meme
# mecanique moteur, autre type de capacite : `Faces.ResolveAbility` avec
# `AbilityType.HeroAction` au lieu de `AbilityType.Special`.
#
# La chanson est ensuite defaussee, quel que soit son compteur `sound` : on
# efface donc sa marque, sinon elle reviendrait « deja repetee » si Encore la
# ramenait.


def GetAbilities() -> Sequence['Ability']:

    def karaoke(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        setlist = Setlist(effect)
        if not setlist:
            return
        chanson = joueur.AskChooseOneText(setlist) if len(setlist) > 1 \
            else setlist[0]
        if chanson is None:
            return

        # CORRECTIF (partie reelle) : il faut FOURNIR le message de reference.
        # Un « Hero Action » est accroche a `Message.WhenPlayerInTurn`, qui ne
        # fait pas partie de la liste blanche de `ResolveSelfInternal`
        # (effect_invoke.py:197) : sans `ref_message`, resoudre la chanson
        # levait une `AssertionError` seche. C'est pour cela que le
        # « Showtime! » passait deja, lui : il est accroche a
        # `WhenCardRevealed`, qui EST dans la liste. Modele : le defi
        # Symbiote Smackdown (2414), qui passe aussi son message.
        ref = Message.WhenPlayerInTurn(joueur, effect)
        Faces.ResolveAbility([chanson], joueur, AbilityType.HeroAction,
                             effect, ref)
        OublierLaSetlist(effect, [chanson])
        Faces.DiscardAll([chanson], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            karaoke,
            conditions=[
                # Sans Setlist, l'action ne changerait rien : on ne l'offre pas.
                lambda effect, message: len(Setlist(effect)) > 0,
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
