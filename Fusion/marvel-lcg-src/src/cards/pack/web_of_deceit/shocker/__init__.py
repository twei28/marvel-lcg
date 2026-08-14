from cards.pack.web_of_deceit import *


def RetournerShocker(effect: 'Effect', this: 'EncounterVillain', menace: int) -> None:
    """« Remove N threat from a side scheme. Flip this card. »

    Shocker n'est jamais vaincu pour de bon : sa defaite est INTERROMPUE, il
    retire de la menace et se retourne. La partie ne se gagne que par
    The Long Night.

    ⚠ LES POINTS DE VIE SONT PORTES PAR LA CARTE, PAS PAR LA FACE
    (`CardFace.components` rend `self.card.components`). Une carte retournee a
    0 PV arrive donc sur sa nouvelle face DEJA vaincue, et le moteur redeclenche
    la defaite pendant le retournement — avant meme que la ligne suivante ne
    s'execute. Mesure : Shocker se retournait sans fin, A vers B vers A, et la
    partie ne rendait plus la main.

    On rend donc ses PV a la face AVANT de retourner, puis on remet la nouvelle
    face a son propre maximum. Entre les deux, la carte n'est jamais a zero.
    """
    RetirerMenaceDUneManigance(effect, menace)

    this.ResetHealth(effect)
    this.card.Flip(effect)
    nouvelle = this.card.face.CastTo(Villain)
    nouvelle.ResetHealth(effect)
