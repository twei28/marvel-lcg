from . import *

# * Black Beast : SBIRE (ELITE. MUTANT.), nemesis de Beast. SCH 2, ATQ 0*, PV 6, boost 4.
# [star] Black Beast gets +X ATK, where X is the printed resource cost of the card tucked under him.
# When Revealed: Tuck the highest-cost TECH upgrade you control under Black Beast. If you cannot, tuck the top card of your deck under Black Beast. (Beast's nemesis minion.)
#
# CARTES DE REFERENCE
#  - `dy001a` (Destiny) : `ThisGainKeyword(fn, attack=1, change_on_event=[OnEvent.PlacedCard(..)])` pour un bonus = X mesure sur une zone de cartes glissees ; ici `OnEvent.PlacedCard("Here")` (carte glissee sous CETTE carte).
#  - `gs099q` Maelstrom / `tuck.md` : `TuckCardUnderHere` d'une amelioration en jeu ; `ra031` : `max(printed_cost.val)` pour « the highest-cost ».
#  - `22006`-style nemesis : `desc.Nemesis` natif.
#
# TEXTE CONTRE CODE
#  « [star] » : le ★ de la valeur d'ATQ (`ATK = "0*"`), PAS un effet de boost. « +X ATK, where X is the PRINTED resource cost of the card tucked under him » : somme des couts imprimes des cartes glissees (une seule en
#    pratique) ; 0 sans carte glissee ou pour une carte sans cout. « the HIGHEST-cost TECH upgrade YOU CONTROL » : parmi les ameliorations TECH du joueur qui revele (egalite : il choisit) ; elle QUITTE le jeu pour aller
#    sous Black Beast. « If you cannot » : aucune amelioration TECH -> la carte du dessus du deck du joueur, face cachee, sous Black Beast. Deck vide : rien.
#  Chiffres : PV 6, SCH 2, ATQ 0 + X, boost 4.


def GetAbilities() -> Sequence['Ability']:

    def x_cout(effect: 'Effect', ui: List['CardFace']) -> int:
        glissees = list(effect.this.GetPlacedCardArea().Get())
        ui.extend(glissees)
        return sum(CoutImprime(f) for f in glissees)

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        techs = AmeliorationsTech(joueur)
        if techs:
            haut = max(CoutImprime(f) for f in techs)
            candidates = [f for f in techs if CoutImprime(f) == haut]
            choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect, prompt="Tuck the highest-cost TECH upgrade under Black Beast", not_move=True)
            if choisie is not None:
                this.TuckCardUnderHere(choisie, effect)
            return
        dessus = joueur.player_deck.GetTop()
        if dessus is not None:
            this.TuckCardUnderHere(dessus, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            x_cout,
            attack=1,
            change_on_event=[OnEvent.PlacedCard("Here")],
        ).SetName("X"),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
    ]
