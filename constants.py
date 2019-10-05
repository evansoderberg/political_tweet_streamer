import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CANDIDATES = {
    'sanders': r'(Bernie Sanders|@SenSanders)',
    'warren': r'(Elizabeth Warren|@ewarren)',
    'harris': r'(Kamala Harris|@KamalaHarris)',
    'biden': r'(Joe Biden|@JoeBiden)',
    'booker': r'(Cory Booker|@CoryBooker)',
    'buttigieg': r'(Pete Buttigieg|@PeteButtigieg)',
    'castro': r'(Julián Castro|Julian Castro|@JulianCastro)',
    'gabbard': r'(Tulsi Gabbard|@TulsiGabbard)',
    'klobuchar': r'(Amy Klobuchar|@amyklobuchar)',
    'orourke': r"(Beto O’Rourke|Beto ORourke|Beto O'Rourke|@BetoORourke)",
    'steyer': r'(Tom Steyer|@TomSteyer)',
    'yang': r'(Andrew Yang|@AndrewYang)'
}

RETWEET = 'RT'