// types-de-carte.ts — les TYPES de carte tels que le moteur les nomme dans une question « nommez un type de carte ».
//
// Rapport nicodede62 du 18/11/2026 (#149) : Cosmo (« name a card type ») proposait 17 boutons, tous intitulés
// « EMPATHETIC ADVANTAGE » sauf « RESOURCE ». Le moteur (`player_ask.py`, `DeclareCardType`) envoie les noms de CLASSE
// (« Hero », « AlterEgo », « MainScheme »...) ; l'interface les prenait pour des noms de capacité (« Spider-Sense ») et
// les remplaçait par le nom imprimé de la carte qui porte la question (l'identité Mantis). Ici, chaque nom de classe
// reçoit son libellé de joueur, en français et en anglais (dico-en.ts).
import { t } from './langue'

const TYPES: Readonly<Record<string, string>> = {
  Hero: 'Héros',
  AlterEgo: 'Alter ego',
  Ally: 'Allié',
  Event: 'Événement',
  Resource: 'Ressource',
  Support: 'Soutien',
  Upgrade: 'Amélioration',
  Obligation: 'Obligation',
  MainScheme: 'Manigance principale',
  EncounterSideScheme: 'Manigance annexe (rencontre)',
  PlayerSideScheme: 'Manigance annexe (joueur)',
  Minion: 'Sbire',
  Villain: 'Méchant',
  Treachery: 'Traîtrise',
  Attachment: 'Attachement',
  Environment: 'Environnement',
  Evidence: 'Preuve',
}

/** Le libellé d'un type de carte nommé par le moteur (« MainScheme » -> « Manigance principale »), sinon `undefined`. */
export function libelleTypeDeCarte(nomMoteur: string): string | undefined {
  const fr = TYPES[nomMoteur.trim()]
  return fr ? t(fr) : undefined
}
