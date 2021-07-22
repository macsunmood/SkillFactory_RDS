pA = 0  # Вероятность встретить спам
pNotA = 0  # Вероятность встретить НЕ спам

## __Consts
SPAM = 1
NOT_SPAM = 0

###

trainPositive, trainNegative = {}, {}  # Словари для хранения количеств спам-слов и неспам-слов.
totals = [0, 0]

def train():
    global pA, pNotA
    spam_count = 0
    for (email, label) in train_data:
        calculate_word_frequencies(email, label)
        if label == SPAM:
            spam_count += 1
    total = len(train_data)
    pA = spam_count / total
    pNotA = (total - spam_count) / total

get_dict = lambda label: trainPositive if label == SPAM else trainNegative

def calculate_word_frequencies(body, label):
    wordsDict = get_dict(label)
    for word in body.lower().split():
        wordsDict[word] = wordsDict.get(word, 0) + 1
        totals[label] += 1

# P(Bi|A) - вероятность встретить слово
def calculate_P_Bi_A(word, label):
	return (get_dict(label).get(word, 0) + 1) / totals[label]
    
# P(B|A) - вероятность встретить текст
def calculate_P_B_A(body, label):
    result = 1.0
    for word in body.lower().split():
        result *= calculate_P_Bi_A(word, label)
    return result

def classify(email):
	if totals[SPAM] == 0 or totals[NOT_SPAM] == 0:
		return 'ERROR: Not enough train data or model training failed!'
	isSpam = pA * calculate_P_B_A(email, SPAM)
	isNotSpam = pNotA * calculate_P_B_A(email, NOT_SPAM)
	# return ('SPAM' if isSpam > isNotSpam else 'NOT SPAM') + f' [pA = {pA}]'
	return 'SPAM' if isSpam > isNotSpam else 'NOT SPAM'

train_data = [  
    ['Купите новое чистящее средство', SPAM],
    ['Купи мою новую книгу', SPAM],
    ['Подари себе новый телефон', SPAM],
    ['Добро пожаловать и купите новый телевизор', SPAM],
    ['Привет давно не виделись', NOT_SPAM],
    ['Довезем до аэропорта из пригорода всего за 399 рублей', SPAM],
    ['Добро пожаловать в Мой Круг', NOT_SPAM],
    ['Я все еще жду документы', NOT_SPAM],
    ['Приглашаем на конференцию Data Science', NOT_SPAM],
    ['Потерял твой телефон напомни', NOT_SPAM],
    ['Порадуй своего питомца новым костюмом', SPAM]
]