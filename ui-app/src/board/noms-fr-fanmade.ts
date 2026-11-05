// noms-fr-fanmade.ts — nom français des cartes FAN-MADE qui ont un vrai
// scan français déposé (assets/pics-fr/fr_<card_id>.jpg).
//
// ÉCRIT À LA MAIN, à la différence de noms-fr.ts (généré depuis marvelcdb,
// qui ne connaît pas les cartes fan-made — voir son commentaire d'en-tête).
// Nécessaire car le JOUEUR VOIT le nom français sur le scan, mais le champ
// `name` du moteur reste en anglais (c'est une clé de logique, jamais
// traduite à la source, voir noms-cartes-fr.ts) : sans ce dictionnaire, les
// boîtes de dialogue (titre de choix, etc.) qui recomposent un titre à partir
// de `name` affichent l'anglais alors que la carte à l'écran est en français.
//
// Signalement mobile du 05/11/2026 (nicodede62, pack Blade) : « Vampire Bite »
// affiché dans le titre d'une boîte de choix alors que le scan dit
// « Morsure de Vampire ».
//
// N'AJOUTER UNE CARTE ICI QUE SI SON SCAN FR EXISTE VRAIMENT
// (assets/pics-fr/fr_<card_id>.jpg) : sinon le nom affiché divergerait du
// scan anglais que le joueur a sous les yeux (même piège que noms-fr.ts).
// Noms relevés directement sur les scans déposés le 04/11/2026 (Blade,
// préfixe bl, auteur Rainy) ; bl001a/bl001b/bl009 omis car identiques à
// l'anglais (« Blade », « Eric Brooks », « Daywalker ») ; bl010 et suivants
// n'ont pas de scan FR déposé, donc pas d'entrée ici.
export const NOMS_FR_FANMADE: Readonly<Record<string, string | undefined>> = {
  bl002: 'Préparer la Chasse',
  bl003: 'En Plein Cœur',
  bl004: 'En Pleine Traque',
  bl005: 'Morsure de Vampire',
  bl006: 'Réflexes Vampiriques',
  bl007: 'Pieux en Bandoulière',
  bl008: 'Épée de Blade',
}
