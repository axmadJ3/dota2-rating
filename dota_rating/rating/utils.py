def calculate_rating_change(win, kills, deaths, assists):
    return (5 if win else -5) + kills - deaths + assists * 0.25
