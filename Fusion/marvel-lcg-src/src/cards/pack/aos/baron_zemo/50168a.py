from . import *

# The Accusation

def GetAbilities() -> Sequence['Ability']:

    def the_accusation_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        player = Worlds.GetFirstPlayer(effect)

        means = player.AskChoosePaper(["50185", "50186", "50187"])
        motive = player.AskChoosePaper(["50188", "50189", "50190"])
        opportunity = player.AskChoosePaper(["50191", "50192", "50193"])

        # CORRECTIF, divergence volontaire du bytecode d'origine. L'accuse etait
        # DEMANDE au joueur parmi les environnements [[Board Member]] encore sur
        # la table. Deux defauts :
        #
        # * le livret p.19 dit qu'il DECOULE de la combinaison — « Each
        #   combination is listed underneath a board member. This board member
        #   is the accused ». On pouvait donc accuser un membre que sa propre
        #   combinaison n'accusait pas, ce qui n'est pas une decision du joueur
        #   mais une lecture du carnet ;
        # * un membre passe cote attachement n'est plus un environnement de ce
        #   nom, donc n'etait plus proposable. En campagne c'est bloquant : les
        #   secrets se reportent, un membre a quatre secrets arrive deja
        #   retourne et le reste jusqu'a la fin (p.6). Mesure faite : avec le
        #   Medecin en chef retourne a l'arrivee, il etait impossible de
        #   l'accuser alors qu'il etait la taupe.
        #
        # `MembreDeLaCombinaison` rend le membre quelle que soit sa face.
        accused = MembreDeLaCombinaison([means, motive, opportunity], effect)

        buff = this.GetBuff(Buff_50168a)
        buff.means = means
        buff.motive = motive
        buff.opportunity = opportunity
        buff.accused = accused

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            the_accusation_revealed
        ),
    ]

