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

    def action_de(chanson: 'CardFace') -> 'Effect|None':
        trouves = chanson.effect.Find(type=AbilityType.HeroAction)
        return trouves[0] if trouves else None

    def cout_payable(chanson: 'CardFace') -> bool:
        """Le cout AVANT LA FLECHE de la Hero Action peut-il etre paye ?

        Decision de l'utilisateur (Q5 du backlog 12, 20/10/2026) : le cout se
        paie (Song of Leadership, « Exhaust an ally -> ») ; sans allie pret, ce
        choix n'est pas propose. Les chansons sans cout sont toujours payables.
        """
        trouve = action_de(chanson)
        if trouve is None or chanson.is_treat_as_if_blank:
            return False
        trouve.context.initiator = chanson.GetControlByOrOwner()
        return all(cf.HasTargets(trouve) for cf in trouve.cost_func.GetAll())

    def resoudre(chanson: 'CardFace', joueur: 'Player', effect: 'Effect',
                 ref: 'Message2') -> None:
        """Resout la Hero Action de `chanson` : cible choisie par le JOUEUR, cout
        PAYE.

        - Cible : `CardFace.ResolveAbility` (card_face.py) remplit les cibles
          tout seul avec les PREMIERES cibles legales ; pour une Hero Action a
          UNE cible, on pose la question (correctif du 20/10/2026, cas
          « le joueur CHOISIT la cible »).
        - Cout : `ResolveToPlayer` passe `skip_cost=True` ; on appelle le meme
          chemin (`EffectInvoker.ResolveSelfInternal`) avec `skip_cost=False`,
          ce qui fait payer « Exhaust an ally -> » comme une carte jouee (Q5).
        """
        from game.effect.effect_invoke import EffectInvoker
        trouve = action_de(chanson)
        if trouve is None or chanson.is_treat_as_if_blank:
            return
        trouve.context.initiator = chanson.GetControlByOrOwner()
        trouve.checker.UpdateLegalTargets()
        legales = [f for f in (trouve.context.all_legal_targets or []) if f is not None]
        fourchette = tuple(trouve.context.target_range)
        if len(legales) >= 2 and fourchette == (1, 1):
            choisie = joueur.AskChooseOneText(legales)
            if choisie is None or choisie not in legales:
                choisie = legales[0]
            trouve.context.targets_internal = [choisie]
        else:
            trouve.context.targets_internal = legales[:fourchette[0]]
        trouve.context.initiator = chanson.GetControlByOrOwner()
        EffectInvoker.ResolveSelfInternal(trouve, None, joueur, effect, ref,
                                          skip_cost=False)

    def karaoke(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        setlist = [c for c in Setlist(effect) if cout_payable(c)]
        if not setlist:
            return
        chanson = joueur.AskChooseOneText(setlist) if len(setlist) > 1 \
            else setlist[0]
        if chanson is None or chanson not in setlist:
            chanson = setlist[0]

        # CORRECTIF (partie reelle) : il faut FOURNIR le message de reference.
        # Un « Hero Action » est accroche a `Message.WhenPlayerInTurn`, qui ne
        # fait pas partie de la liste blanche de `ResolveSelfInternal`
        # (effect_invoke.py:197) : sans `ref_message`, resoudre la chanson
        # levait une `AssertionError` seche. C'est pour cela que le
        # « Showtime! » passait deja, lui : il est accroche a
        # `WhenCardRevealed`, qui EST dans la liste. Modele : le defi
        # Symbiote Smackdown (2414), qui passe aussi son message.
        ref = Message.WhenPlayerInTurn(joueur, effect)
        resoudre(chanson, joueur, effect, ref)
        OublierLaSetlist(effect, [chanson])
        Faces.DiscardAll([chanson], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            karaoke,
            conditions=[
                # Sans Setlist, l'action ne changerait rien : on ne l'offre pas.
                # Q5 : une chanson dont le cout est impayable n'est pas proposee.
                lambda effect, message: any(cout_payable(c) for c in Setlist(effect)),
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
