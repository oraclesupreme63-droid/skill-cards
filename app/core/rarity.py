def calculate_rarity(level: int) -> str:
    if level <= 20:
        return "bronce"
    if level <= 40:
        return "plata"
    if level <= 60:
        return "oro"
    if level <= 80:
        return "platino"
    return "dios"
