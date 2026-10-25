from . import *

# * Yd'Nar (face ALTER-EGO) — SOLDIER. YAUTJA. PV 13, REC 4, main 6.
# Setup: Put Infralocked into play.
# Future Trophy — Action: Discard cards from the top of your deck until you discard an upgrade, then add that card to
#   your hand. (Limit once per round.)
#
# Cartes de reference :
#  - Setup d'une carte mise de cote : `ch001b` Shang-Chi / `36001b` * Ororo Munroe (storm) : `BeginGameWithSetAside([...])` +
#    `WhenCardSetup("This", op)` puis `PutIntoPlay`. Infralocked est « Permanent » et n'est PAS une des 15 cartes du deck
#    (les impressions vont de 1/16 a 16/16, Infralocked est la 1/16) : elle part de cote et entre en jeu au Setup.
#  - « discard cards from the top of your deck until you discard X, then add that card to your hand » : le mot-cle `seek`
#    (fiche mots-cles/seek.md), `br009` Oathbrother : `joueur.DiscardDeckUntil(effect, card_type=Upgrade)` puis `Faces.AddToHand`.
#  - Action d'alter-ego limitee : `WhenInYourPlayTurn(AbilityType.AlterEgoAction, op).LimitOncePerRound()` (bt001b).
#
# ⚠ Mots-pieges :
#  - « Put Infralocked INTO PLAY » : Infralocked s'attache a l'IDENTITE du joueur (le moteur n'a pas d'amelioration libre :
#    « return this card to your play area » = revenir sur l'identite, voir pd002). Seule la face ALTER-EGO le fait.
#  - « Action » nu sur l'alter-ego : `AlterEgoAction` ; « Limit once per round » (par carte).
#  - « until you discard AN UPGRADE » : n'importe quelle amelioration (Upgrade), pas seulement TECH.
#  - « then add THAT card to your hand » : la carte defaussee qui a arrete la boucle revient en main (et elle seule).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None or Infralocked(effect, joueur) is not None:
            return
        candidates = list(joueur.set_aside_deck.Get()) + list(joueur.additional_discard_pile.Get())
        for face in candidates:
            if face.paper.card_id == ID_INFRALOCKED:
                infra = face.CastTo(Upgrade)
                infra.PutIntoPlay(joueur, effect)
                # « Put Infralocked into play » : l'amelioration n'a pas de cible a choisir, elle va sur l'identite (une
                # amelioration libre n'existe pas dans le moteur, voir pd002).
                identite = joueur.GetIdentity()
                if identite is not None and infra.GetBindFace() is None:
                    infra.AttachTo2(identite, effect)
                return

    def trophee_futur(effect: 'Effect', message: 'Message.WhenInYourPlayTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        trouvee = joueur.DiscardDeckUntil(effect, card_type=Upgrade)
        if trouvee is not None:
            Faces.AddToHand([trouvee], joueur, effect)

    return [
        AbilityFactory.BeginGameWithSetAside([ID_INFRALOCKED]),
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            trophee_futur,
        ).SetName("Future Trophy").LimitOncePerRound(),
        ActionHonorHuntEnVitrine(),
    ]
