INPUT_DESCRIPTION =  "Sprecyzuj parametry fizyczne oraz środowiskowe dla symulacji. Gęstość powietrza może być zadana bezpośrednio lub wyznaczona wykorzystując parametry środowiskowe misji wpisane do pierwszej kolumny.",
SIM1_DESCRIPTION = "Wyznacz średnicę czaszy spadochronu wymaganą do osiągnięcia docelowej prędkości opadania. Wartości MIN oraz MAX sterują zakresem prędkości, dla których wykonywane są obliczenia. Wyznaczona średnica spadochronu zostanie użyta w kolejnych sekcjach.",
SIM2_DESCRIPTION = "Wyznacz obciążenia występujące podczas otwarcia czaszy spadochronu o danej średnicy przy zadanej prędkości opadania. Średnica spadochronu może być zdefiniowana bezpośrednio lub wyznaczona w sekcji \"ŚREDNICA CZASZY SPADOCHRONU\".",
GENERATOR_DESCRIPTION = "Wyznacz kształt segmentów czaszy spadochronu. Średnica spadochronu może być zdefiniowana bezpośrednio lub wyznaczona w sekcji \"ŚREDNICA CZASZY SPADOCHRONU\".",
INPUT_PARAMETERS_DESCRIPTION = """PARAMETRY GŁÓWNE

Gęstość powietrza - wartość w kg/m^3 na wysokości otwarcia spadochronu. Do wpisania bezpośrednio lub wyznaczana przy użyciu dodatkowego modułu.
Przyśpieszenie ziemskie - wartość w m/s^2 dla lokalizacji platformy startowej. Wpływ zmiany wysokości na wartość tego parametru jest pomijalna.
Współczynnik oporu aerodynamicznego - wartość zależna od geometrii spadochronu, dobierana z tabel.

WYZNACZANIE GĘSTOŚCI POWIETRZA (PARAMETRY POŚREDNIE)

Ciśnienie odniesienia - wartość ciśnienia atmosferycznego mierzona na platformie startowej.
Temperatura odniesienia - wartość temperatury powietrza mierzona na platformie startowej.
Wilgotność powietrza - mierzona na platformie startowej.
Wysokość otworzenia spadochronu - wysokość (w metrach) otwarcia spadochronu (względem platformy startowej)."""

DESCRIPTION_AIR_DENSITY_PARAMS = {
    "refpressure": "Ciśnienie atmosferyczne mierzone na platformie startowej",
    "reftemp": "Temperatura powietrza mierzona na platformie startowej",
    "humidity": "Wilgotność powietrza mierzona na platformie startowej",
    "height": "Wysokość otwarcia spadochronu (względem platformy startowej)",
    "airdensitycalc": "Wyznaczona wartość gęstości powietrza",
}

DESCRIPTION_INPUT_PARAMS = {
    "airdensity": "Gęstość powietrza na wysokości otwarcia spadochronu",
    "gaccel": "Przyśpieszenie ziemskie mierzone na platformie startowej",
    "dragcoeff": "Współczynnik oporu aerodynamicznego zależny od kształtu spadochronu",
    "draginteg": "Znormalizowana wartość pola pod wykresem siły oporu aerodynamicznego w funkcji czasu",
}

DESCRIPTION_SIM1_PARAMS = {
    "mass": "Rzeczywista masa pojazdu",
    "velocitystart": "Początek zakresu rozpatrywanych prędkości opadania",
    "velocitystop": "Koniec zakresu rozpatrywanych prędkości opadania",
    "velocity": "Oczekiwana prędkość opadania pojazdu po otwarciu spadochronu",
    "diameter": "Wyznaczona średnica czaszy spadochronu"
}

DESCRIPTION_SIM2_PARAMS = {
    "mass" : "Rzeczywista masa pojazdu",
    "velocity": "Prędkość opadania przed otwarciem spadochronu",
    "diameter": "Średnica czaszy spadochronu"
}

DESCRIPTION_GENERATOR_PARAMS = {
    "diameter": "Średnica czaszy spadochronu",
    "segments": "Liczba segmentów czaszy spadochronu",
    "spherepercent": "Współczynnik sferyczności czaszy spadochronu, gdzie 0.5 do spadochron półsferyczny",
    "holediameter": "Średnica otworu w czaszy spadochronu",
    "points": "Liczba punktów na segment czaszy spadochronu. Więcej punktów oznacza dokładniejsze odwzorowanie kształtu"
}