"""
Settings module
"""
# FOLDERS
PATH_RAW_FOLDER = 'data/raw'
PATH_PROCESSED_AUDIO = 'data/processed/audio'
PATH_PROCESSED_JSON = 'data/processed/json'

# MODELS
PATH_MODEL_EN = 'models/vosk/vosk-model-small-en-us-0.15'
PATH_MODEL_PT = 'models/vosk/vosk-model-small-pt-0.3'

# STOPWORDS EN & PT-BR
STOPWORDS_EN = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
    "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
    "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while",
    "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
])

STOPWORDS_PT = set([
    "a", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo", "as", "até", "com",
    "como", "da", "das", "de", "dela", "delas", "dele", "deles", "depois", "do", "dos", "e",
    "ela", "elas", "ele", "eles", "em", "entre", "era", "eram", "essa", "essas", "esse", "esses",
    "esta", "estamos","estas", "estava", "estavam", "este", "esteja", "estejam", "estejamos",
    "estes", "esteve", "estive", "estivemos", "estiver", "estivera", "estiveram", "estiverem",
    "estivermos", "estivesse", "estivessem", "estivéramos", "estivéssemos", "estou", "eu", "foi",
    "fomos", "for", "fora", "foram", "forem", "formos", "fosse", "fossem", "fui", "fôramos",
    "fôssemos", "haja", "hajam", "hajamos", "havemos", "hei", "houve", "houvemos", "houver",
    "houvera", "houveram", "houverei", "houverem", "houveremos", "houveria", "houveriam",
    "houvermos", "houverá", "houverão", "houveríamos", "houvesse", "houvessem", "houvéramos",
    "houvéssemos", "isso", "isto", "já", "lhe", "lhes", "mais", "mas", "me", "mesmo", "meu",
    "meus", "minha", "minhas", "muito", "na", "nas", "nem", "no", "nos", "nossa", "nossas",
    "nosso", "nossos", "num", "numa", "não", "nós", "o", "os", "ou", "para", "pela", "pelas",
    "pelo", "pelos", "por", "qual", "quando", "que", "quem", "se", "seja", "sejam", "sejamos",
    "sem", "serei", "seremos", "seria", "seriam", "será", "serão", "seríamos", "seu", "seus",
    "somos", "sou", "sua", "suas", "são", "só", "também", "te", "tem", "temos", "tenha",
    "tenham", "tenhamos", "tenho", "terei", "teremos", "teria", "teriam", "terá", "terão",
    "teríamos", "teu", "teus", "teve", "tinha", "tinham", "tive", "tivemos", "tiver", "tivera",
    "tiveram", "tiverem", "tivermos", "tivesse", "tivessem", "tivéramos", "tivéssemos", "tu",
    "tua", "tuas", "tém", "tínhamos", "um", "uma", "você", "vocês", "vos", "à", "às", "é", "está",
    "então", "vou"
])
