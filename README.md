# Projekt na kurs "Programowanie w języku Python"

# PyMeno


Autorzy:
Klaudia Olejniczak
Oleksandr Kuzhel





# Opis ogólny projektu

	Aplikacja która dzięki przeszukaniu biblioteki muzycznej użytkownika odnajduje 
	podobne do nich i wyświetla je użytkownikowi wraz z możliwością otworzenia odnośnika 
	bezpośrednio do ich utworów na YouTube. Wyszukiwanie podobieństwa opiera się
	 na analizie tekstów utworów.

# Informacje wstępne:

	Projekt PyMeno realizowany jest w ramach przedmiotu Programowanie w języku Python.
	 Implementacja odbyła się w języku Python 3.4  . Dokumentacja ta ma na celu opisać 
	 program, by ułatwić użytkowanie oraz zapoznanie się z kodem.


# Wymagane dodatkowe biblioteki :

	PyLyrics, nltk, mutagen, Youtube API
	       -  PyLyrics - Komenda :   pip install PyLyrics 
	       (W razie problemów : https://pypi.python.org/pypi/PyLyrics/ )
	       - nltk - Strona : https://pypi.python.org/pypi/nltk 
	       - mutagen - Strona : https://pypi.python.org/pypi/mutagen 
	       - YouTube API - Komenda : pip install --upgrade google-api-python-client 
	       ( W razie problemów : https://developers.google.com/api-client-library/python/start/installation )
	       

# Opis aplikacji :

	Projekt składa się z elementów zajmujących się tworzeniem biblioteki muzycznej do 
	porównywania posiadanych przez użytkownika utworów, analizy biblioteki użytkownika, 
	wyszukiwania podobieństw oraz GUI.  


# Funkcjonalność :

	## Nowe źródła porównań
	
	W aplikacji mamy możliwość uaktualnienia bazy porównań. (Data → Download artists list)  
	Dzięki temu można uaktualnić swoją listę scrobble.xml, względem toplisty z Last.fm. 

	## Tworzenie  i poszerzanie biblioteki utworów do porównań

	Bibliotekę można tworzyć od zera lub kontynuować jej rozbudowywanie. 
	Poprzez  ( Data → Parse artists information to database ), gdzie podaje się od którego do 
	którego artysty chce się ściągnąć. Minimalna liczba to 0, maksymalna 1000. 
	W wersji użytkowej gromadzenie danych nie powinno być dostępne dla użytkownika,
	 ale nie mamy dostępu do takiej bazy.

	## Wyszukiwanie podobnych utworów

	Wyszukiwanie podobnych utworów dzieli się na trzy etapy, niezależnie od algorytmu, 
	który się wybierze ( dostępne są 3). 
                1. Przeszukiwanie biblioteki użytkownika i przetwarzanie tekstów
                2. Zastosowanie algorytmu i wyszukanie podobieństw.
                    Algorytm I
                    	Na podstawie wektorów dla każdego artysty w bazie i wektora wszystkich słów
                    	 w naszej bibliotece wybieramy najbliższe 1 wyniki, po czym porównujemy je ze 
                    	 względu na średnią ilość słów na utwór. ( Naszym zdaniem istnieje tutaj 
                    	 zależność względem tempa utworu, im więcej, tym dynamiczniejsza ). Po czym 
                    	 wyszukuje się ponownie za pomocą miary podobieństw wektorów, tylko na 
                    	 bazie artysta, album ,z zachowaniem najlepszych wyników z poprzedniej 
                    	 eliminacji.
                     Algorytm II
                    	Na podstawie słowników z bibliotek i zbioru słów powstaje przecięcie pomiędzy 
                    	nimi. Wybieramy te zbiory które są największe, ograniczamy poprzez ilość słów 
                    	(analogicznie jak w alg I) i na wyniku wykorzystujemy podobieństwo wektorów
                    	 z wykorzystaniem artysta,album. 
                     Algorytm III
                    	Ten algorytm w stosunku poprzednich nie opiera się na wspólnym słowniku dla 
                    	całej biblioteki użytkownika, tylko za pomocą podobieństwa wektorów wyszukuje 
                    	najbardziej podobne artysty do każdego znalezionego wykonawcy. Po czym opiera 
                    	się o kryterium ze średnią słów w utworze o powiększonym lekko zakresie niż 
                    	średnia wynikająca z obliczeń.
                3. Wylosowanie utworu z wybranego autora oraz albumu.

	## Odsyłanie do utworu na serwisie YouTube

	Po dwukrotnym kliknięciu na zespół : utwór na liście zaproponowanych użytkownikowi 
	zostanie otworzona nowa zakładka w przeglądarce wraz z utworem, który został mu 
	zaproponowany.