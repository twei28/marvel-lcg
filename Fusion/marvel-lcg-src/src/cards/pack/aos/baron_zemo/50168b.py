from . import *

# The Accusation

def GetAbilities() -> Sequence['Ability']:

    def the_accusation_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        buff = this.GetBuff(Buff_50168a)

        means = buff.means
        motive = buff.motive
        opportunity = buff.opportunity
        accused = buff.accused

        # ~~1. Use the cards in the A.I.M. envelope to identify the mole.~~
        mole = CalcMole(effect)

        # C'est ICI que l'enveloppe s'ouvre, et pas avant : le livret p.19 dit
        # « the players take the evidence cards from the A.I.M. envelope » au
        # moment de comparer. En campagne les trois preuves n'existaient donc
        # pas encore comme cartes — le secret dormait au carnet, hors de portee
        # du navigateur. On les fabrique maintenant, face visible : le joueur a
        # desormais le droit de les voir.
        # Campagne ou pas : les trois preuves n'existent pas encore comme cartes,
        # elles sont fabriquees ICI. Hors campagne, ce code lisait la pile
        # « A.I.M.Envelope » — qui n'est plus montee depuis que la repartition ne
        # part plus au navigateur, et la chaine s'arretait la, en silence.
        from cards.pack.aos.campaign import PreuveEnJeu
        card_ids = CartesDeLEnveloppeAim(effect)
        faces = [PreuveEnJeu(effect, card_id) for card_id in card_ids]
        for face in faces:
            face.CastTo(Evidence).AttachTo2(mole, effect)

        # 2. For each guess you got wrong, place 1 secret counter on each [[Board Member]] card.
        wrong = 0
        if means not in card_ids:
            wrong += 1
        if motive not in card_ids:
            wrong += 1
        if opportunity not in card_ids:
            wrong += 1
        PlaceSecretCounterOnEachBoardMemberCard(wrong, effect)

        # 3. If you accused the wrong board member, place 3 secret counters on the accused.
        if accused != mole:
            Faces.PlaceCountersOn([accused], 3, 'secret', effect)

        # 4. Advance to stage 3A.
        this.Advance("3A", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            the_accusation_revealed
        ),
    ]

