from . import *
# Divas — EVENEMENT BASIQUE custom (jakxin), cout 0, [energy].
# Team-Up (any 2 of Black Cat, Firestar, Hellcat, and Monica Rambeau). Max 1
#   per deck.
# Hero Action: Search your discard pile for 3 cards, each with a different
#   printed resource. Add 1 to your hand and shuffle the rest into your deck.
#
# ⚠ TEAM-UP « 2 PARMI 4 » : `desc.TeamUp` du moteur attend deux groupes
#   (« A;B », has_teamup.py) et exigerait les DEUX. On code la condition a la
#   main (`conditions=`) : au moins deux des quatre personnages en jeu, cote
#   joueur. Le deckbuilder n'a donc pas de restriction Team-Up sur cette carte
#   (ecart note). Black Cat n'est pas portee (absente du dossier).
# ⚠ « each with a DIFFERENT printed resource » : trois choix successifs, la
#   couleur deja prise sortant des candidates. `MaxPerDeck` : desc, base auto.

DIVAS = ("Black Cat", "Firestar", "Hellcat", "Captain Marvel")

def GetAbilities() -> Sequence['Ability']:

    def couleur_imprimee(face: 'CardFace') -> str|None:
        res = FacesCounter.GetPrintedResources([face])
        for c in ("R", "B", "Y", "G"):
            if res.GetColor(c, convert_green_res=False) > 0:
                return c
        return None

    def deux_divas_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        noms = set()
        for u in Worlds.GetOnFieldFriendlyCharacters(effect):
            if u.GetControlByPlayer() is joueur:
                for nom in DIVAS:
                    if u.IsName(nom):
                        noms.add(nom)
        return len(noms) >= 2

    def divas(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        prises: List['CardFace'] = []
        couleurs: set = set()
        for _ in range(3):
            candidates = [f for f in joueur.discard_pile.Get(True)
                          if f not in prises and couleur_imprimee(f) and couleur_imprimee(f) not in couleurs]
            if not candidates:
                break
            choix = list(joueur.AskChooseFaces(candidates, (1, 1), effect, prompt="Search"))
            if not choix:
                break
            prises += choix
            couleurs.add(couleur_imprimee(choix[0]))
        if not prises:
            return
        en_main = list(joueur.AskChooseFaces(prises, (1, 1), effect, prompt="Add to hand"))
        if en_main:
            Faces.AddToHand(en_main, joueur, effect)
        reste = [f for f in prises if f not in en_main]
        if reste:
            Faces.ShuffleAllTo(reste, joueur.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            divas,
            conditions=[deux_divas_en_jeu],
        ).SetPlay().SetLabel(),
    ]
