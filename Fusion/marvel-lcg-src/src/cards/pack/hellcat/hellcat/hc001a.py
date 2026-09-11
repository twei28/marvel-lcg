from . import *
# * Hellcat — HEROINE. AVENGER. PSIONIC. CTR 2 / ATQ 2 / DEF 2, MNG 5, 11 PV.
# Response: After you play a card with a printed [mental] resource, attach that
#   card to Hellcat (to a maximum of 3). (Limit twice per round.)
# Empowered — Resource: Discard 1 attached card from Hellcat → generate a
#   [mental] resource.
#
# Modeles : dd001a Doctor Doom (`AfterPlayerPlayedCard` + `paid_resources`),
# ze011 Mount Olympus (ressource a cout `CostFunc.Custom`), ze014 The Mother of
# Night (`PlaceCardHere`).
#
# ⚠ « a card » = un EVENEMENT (arbitrage utilisateur, notice de l'auteur) :
#   `CardFinder(card_type=Event, has_printed_res="B")`. Un allie accroche
#   quitterait la table, ce que la notice ne decrit jamais.
# ⚠ « Limit TWICE per round » : le moteur n'a que `LimitOncePerRound`. Deux
#   Response identiques, chacune limitee a une fois par round = deux fois.
# ⚠ « to a maximum of 3 » : condition sur le nombre de cartes deja glissees,
#   verifiee dans `conditions` pour que la Response ne soit meme pas proposee.
# ⚠ Empowered : le cout defausse UNE carte glissee, choisie par le joueur.
#   `CostFunc.Custom` rend False s'il n'y en a aucune : la ressource n'est
#   alors pas proposee (cost_func.py). Ne JAMAIS passer par `CostFunc.Spend`
#   dans une capacite de ressource (piege ze011 : reset du pool).

def GetAbilities() -> Sequence['Ability']:

    def moins_de_trois_accrochees(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return len(CartesAttacheesA(effect.this)) < MAX_ATTACHEES

    def pas_encore_accrochee(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        # ⚠ Les deux Response (= « twice per round ») se declenchent toutes deux
        #   sur la MEME carte jouee : sans cette condition, la seconde
        #   re-accrochait la carte deja glissee et la limite etait consommee
        #   par UN seul evenement (vu au harnais le 11/09/2026 : 1 accrochee
        #   au lieu de 2 sur trois Illusion).
        return message.played_face not in CartesAttacheesA(effect.this)

    def accrocher(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        face = message.played_face
        if face is None or len(CartesAttacheesA(this)) >= MAX_ATTACHEES:
            return
        AccrocherA(this, [face], effect)

    def defausser_une_accrochee(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        this = effect.this.CastTo(Hero)
        joueur = effect.GetInitiator()
        accrochees = CartesAttacheesA(this)
        if not accrochees or joueur is None:
            return False
        choisies = joueur.AskChooseFaces(accrochees, (1, 1), effect, prompt="Discard")
        if not choisies:
            return False
        Faces.DiscardAll(list(choisies), effect)
        return True

    def response() -> 'Ability':
        return AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event, has_printed_res="B"),
            accrocher,
            conditions=[moins_de_trois_accrochees, pas_encore_accrochee],
        ).LimitOncePerRound()

    return [
        response(),
        response(),
        # ⚠ `conditions` OBLIGATOIRE : sans elle, Empowered est OFFERTE au paiement
        #   meme sans carte accrochee ; son cout Custom rend alors False et le
        #   moteur leve `GameSignal_UndoRequest`, qui ANNULE toute la carte en
        #   train d'etre payee (resources.py:409). Vu le 11/09/2026 : dix cas du
        #   pack rouges d'un coup, Green Hell « failed » sans motif.
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
            conditions=[lambda effect, message: len(CartesAttacheesA(effect.this)) > 0],
        ).SetCostFunc(CostFunc.Custom(None, defausser_une_accrochee))
        .SetName(EMPOWERED),
    ]
