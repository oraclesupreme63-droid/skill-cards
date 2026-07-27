export const RARITY_STYLES = {
  bronce: { background: '#cd7f32', color: '#3a2210' },
  plata: { background: '#c0c0c0', color: '#2b2b2b' },
  oro: { background: '#ffd700', color: '#3a2f00' },
  platino: { background: '#e5e4e2', color: '#2b2b2b' },
  dios: {
    background: 'linear-gradient(135deg, #7b2ff7, #f107a3)',
    color: '#ffffff',
  },
}

export function rarityStyle(rarity) {
  return RARITY_STYLES[rarity] ?? RARITY_STYLES.bronce
}
