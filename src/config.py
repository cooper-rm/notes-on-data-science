from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'

FRENCH_URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip'
BITFINEX_URL = 'https://api-pub.bitfinex.com/v2/candles/trade:1D:t{symbol}/hist'
HMDA_URL = 'https://ffiec.cfpb.gov/v2/data-browser-api/view/csv'

HEADERS = {'User-Agent': 'notes-on-data-science/0.1'}

CRYPTO_SYMBOLS = ['BTCUSD', 'ETHUSD']
CRYPTO_LIMIT = 10000

HMDA_PARAMS = {'years': 2023, 'states': 'RI', 'actions_taken': '1,3'}

FRENCH_FILE = RAW_DIR / 'french_factors_daily.csv'
CRYPTO_FILE = RAW_DIR / 'crypto_daily.csv'
HMDA_FILE = RAW_DIR / 'hmda_2023_ri.csv'
