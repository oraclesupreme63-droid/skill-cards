// Tratamiento tipo "Icon" / "Hero" de FIFA Ultimate Team para las
// reference cards: blanco-dorado nacarado para Legendary, morado-azul
// brillante para Epic. Es un concepto distinto de RARITY_STYLES
// (que colorea cada skill individual) — este es el tier GENERAL de
// la carta.
export const REFERENCE_TIER_STYLES = {
  Legendary: {
    background:
      'linear-gradient(160deg, #fffbe6, #f5e7c1 30%, #e8c766 55%, #fff6d9 75%, #f5e7c1)',
    color: '#3a2a00',
    border: '#e8c766',
    glow: 'rgba(232, 199, 102, 0.85)',
  },
  Epic: {
    background:
      'linear-gradient(160deg, #2a0a5e, #6d1fd8 35%, #a855f7 60%, #2a0a5e 85%)',
    color: '#ffffff',
    border: '#c084fc',
    glow: 'rgba(168, 85, 247, 0.85)',
  },
}

export function referenceTierStyle(tier) {
  return REFERENCE_TIER_STYLES[tier] ?? REFERENCE_TIER_STYLES.Epic
}
