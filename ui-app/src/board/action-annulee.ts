// Rapport du 26/10/2026 (Safe House #30) : fermer ou abandonner une action avant de l'avoir validee ne disait RIEN. La carte
// se redressait, aucun effet, aucun message : le joueur croyait l'action jouee. Une action qui s'eteint cote client SANS
// qu'aucune reponse ne soit partie au moteur, et sans que le moteur ait pose une autre question, est une action abandonnee.
import { useCallback, useEffect, useRef, useState } from 'react'
import { t } from './langue'

const DUREE_MESSAGE_MS = 3500

export function useActionAnnulee(nomOption: string | undefined, demande: object | undefined) {
  const [message, setMessage] = useState<string | undefined>(undefined)
  // L'action et la question du moteur telles qu'elles etaient au rendu d'avant.
  const precedent = useRef<{ nom: string | undefined; demande: object | undefined }>({ nom: undefined, demande: undefined })
  const reponseEnvoyee = useRef(false)

  const noterReponse = useCallback(() => {
    reponseEnvoyee.current = true
  }, [])

  useEffect(() => {
    const avant = precedent.current
    precedent.current = { nom: nomOption, demande }
    if (nomOption !== undefined) {
      // Une action (re)commence : la reponse eventuelle d'avant ne compte plus.
      if (avant.nom === undefined) reponseEnvoyee.current = false
      return
    }
    if (avant.nom === undefined) return
    const abandonnee = !reponseEnvoyee.current && demande !== undefined && demande === avant.demande
    reponseEnvoyee.current = false
    if (abandonnee) setMessage(`${t('Action annulée')} : ${avant.nom}`)
  }, [nomOption, demande])

  useEffect(() => {
    if (message === undefined) return
    const minuteur = window.setTimeout(() => setMessage(undefined), DUREE_MESSAGE_MS)
    return () => window.clearTimeout(minuteur)
  }, [message])

  return { message, noterReponse }
}
