export const RARITY_STYLES = {
  bronce: {
    background: 'linear-gradient(160deg, #e8a463, #cd7f32 55%, #8a5423)',
    color: '#2a1608',
    glow: 'rgba(205, 127, 50, 0.55)',
  },
  plata: {
    background: 'linear-gradient(160deg, #f3f3f5, #c0c0c0 55%, #8f8f94)',
    color: '#232324',
    glow: 'rgba(192, 192, 192, 0.6)',
  },
  oro: {
    background: 'linear-gradient(160deg, #fff3b0, #ffd700 50%, #b8860b)',
    color: '#3a2a00',
    glow: 'rgba(255, 215, 0, 0.65)',
  },
  platino: {
    background: 'linear-gradient(160deg, #f4fbff, #cfe7f0 45%, #7fa8b8)',
    color: '#12262d',
    glow: 'rgba(150, 210, 230, 0.65)',
  },
  dios: {
    background:
      'linear-gradient(160deg, #ff9de6, #b83bff 40%, #6d1fd8 75%, #2c0a5e)',
    color: '#ffffff',
    glow: 'rgba(184, 59, 255, 0.75)',
  },
}

export function rarityStyle(rarity) {
  return RARITY_STYLES[rarity] ?? RARITY_STYLES.bronce
}
