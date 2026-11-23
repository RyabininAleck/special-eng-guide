"""Шаблоны предложений для автогенерации RU→EN карточек."""

from __future__ import annotations

import re

from word_list_parser import primary_ru

IRREGULAR_PAST: dict[str, str] = {
    "be": "was",
    "become": "became",
    "begin": "began",
    "blow": "blew",
    "break": "broke",
    "bring": "brought",
    "build": "built",
    "buy": "bought",
    "catch": "caught",
    "come": "came",
    "deal": "dealt",
    "do": "did",
    "drink": "drank",
    "drive": "drove",
    "eat": "ate",
    "fall": "fell",
    "feel": "felt",
    "find": "found",
    "fly": "flew",
    "get": "got",
    "give": "gave",
    "go": "went",
    "grow": "grew",
    "hang": "hung",
    "have": "had",
    "hear": "heard",
    "hold": "held",
    "keep": "kept",
    "know": "knew",
    "leave": "left",
    "let": "let",
    "lose": "lost",
    "make": "made",
    "mean": "meant",
    "meet": "met",
    "pay": "paid",
    "put": "put",
    "read": "read",
    "run": "ran",
    "say": "said",
    "see": "saw",
    "sell": "sold",
    "send": "sent",
    "set": "set",
    "show": "showed",
    "sit": "sat",
    "sleep": "slept",
    "speak": "spoke",
    "spend": "spent",
    "stand": "stood",
    "take": "took",
    "teach": "taught",
    "tell": "told",
    "think": "thought",
    "throw": "threw",
    "understand": "understood",
    "wake": "woke",
    "wear": "wore",
    "win": "won",
    "write": "wrote",
}

CONNECTOR_OPPOSITES: dict[str, str] = {
    "because of": "despite / in spite of",
    "due to": "regardless of",
    "thanks to": "because of problems with",
    "as a result": "nevertheless",
    "therefore": "however",
    "that's why": "even so",
    "for this reason": "despite this",
    "however": "therefore",
    "although": "because",
    "even though": "since",
    "in spite of": "because of",
    "despite": "because of",
    "on the other hand": "on the one hand",
    "while": "whereas (same side)",
    "whereas": "while",
    "instead of": "as well as",
    "rather than": "as well as",
    "nevertheless": "therefore",
    "still": "no longer",
    "yet": "already",
    "instead": "as well",
    "turn on": "turn off",
    "turn off": "turn on",
    "get up": "lie down / go to bed",
    "wake up": "fall asleep",
    "go out": "stay in",
    "come back": "leave",
    "break up": "get back together",
    "give up": "keep going",
    "speed up": "slow down",
    "slow down": "speed up",
    "move in": "move out",
    "move out": "move in",
    "check in": "check out",
    "check out": "check in",
    "put on": "take off",
    "take off": "put on",
    "throw away": "keep",
    "call off": "go ahead with",
    "put off": "do immediately",
    "calm down": "get worked up",
    "cheer up": "feel down",
    "look for": "find",
    "find out": "remain unaware",
    "give back": "keep",
    "hand in": "keep",
    "back up": "move forward",
    "turn back": "go on",
    "get away": "stay",
    "run away": "stay / face",
    "fall apart": "hold together",
    "blow up": "calm down",
    "let down": "support",
    "figure out": "remain confused",
    "keep up with": "fall behind",
    "look forward to": "dread",
    "get over": "dwell on",
    "pass away": "be born",
    "hang up": "pick up (the phone)",
    "pick up": "drop off",
    "drop off": "pick up",
}

PHRASAL_SPECIAL: dict[str, tuple[list[str], list[str]]] = {
    "run out of": (
        [
            "У нас закончилось молоко.",
            "В офисе закончилась бумага.",
            "К вечеру у них закончились идеи.",
        ],
        [
            "We RAN OUT OF milk.",
            "The office RAN OUT OF paper.",
            "By evening they RAN OUT OF ideas.",
        ],
    ),
    "look forward to": (
        [
            "Я с нетерпением жду отпуска.",
            "Она с нетерпением ждёт встречи с друзьями.",
            "Мы с нетерпением ждём премьеры фильма.",
        ],
        [
            "I LOOK FORWARD TO my holiday.",
            "She LOOKS FORWARD TO meeting her friends.",
            "We LOOK FORWARD TO the film premiere.",
        ],
    ),
    "keep in touch": (
        [
            "Мы поддерживаем связь через мессенджер.",
            "Важно поддерживать связь с бывшими коллегами.",
            "Они поддерживают связь, хотя живут в разных странах.",
        ],
        [
            "We KEEP IN TOUCH via messenger.",
            "It's important to KEEP IN TOUCH with former colleagues.",
            "They KEEP IN TOUCH although they live in different countries.",
        ],
    ),
    "get along with": (
        [
            "Он хорошо ладит с соседями.",
            "Не всегда легко ладить с начальником.",
            "Дети отлично ладят друг с другом.",
        ],
        [
            "He GETS ALONG WITH his neighbors.",
            "It isn't always easy to GET ALONG WITH your boss.",
            "The kids GET ALONG WITH each other very well.",
        ],
    ),
    "make up with": (
        [
            "Они помирились после ссоры.",
            "Надо помириться, пока не поздно.",
            "Она помирилась с подругой за чашкой кофе.",
        ],
        [
            "They MADE UP WITH each other after the argument.",
            "You should MAKE UP WITH him before it's too late.",
            "She MADE UP WITH her friend over coffee.",
        ],
    ),
    "move in together": (
        [
            "Они решили съехаться в следующем месяце.",
            "Съехаться — серьёзный шаг в отношениях.",
            "Пара съехалась после года встреч.",
        ],
        [
            "They decided to MOVE IN TOGETHER next month.",
            "To MOVE IN TOGETHER is a serious step in a relationship.",
            "The couple MOVED IN TOGETHER after a year of dating.",
        ],
    ),
    "cut down on": (
        [
            "Он решил сократить потребление сахара.",
            "Нужно сократить потребление кофе.",
            "Семья сократила потребление фастфуда.",
        ],
        [
            "He decided to CUT DOWN ON sugar.",
            "You should CUT DOWN ON coffee.",
            "The family CUT DOWN ON fast food.",
        ],
    ),
    "end up": (
        [
            "Мы в итоге оказались в другом городе.",
            "Он в итоге остался работать там же.",
            "Разговор в итоге перешёл на политику.",
        ],
        [
            "We ENDED UP in another city.",
            "He ENDED UP staying at the same job.",
            "The conversation ENDED UP about politics.",
        ],
    ),
    "turn out": (
        [
            "Оказалось, что билеты уже распроданы.",
            "Фильм оказался лучше, чем я думал.",
            "Встреча оказалась короче, чем планировали.",
        ],
        [
            "It TURNED OUT the tickets were sold out.",
            "The film TURNED OUT better than I expected.",
            "The meeting TURNED OUT shorter than planned.",
        ],
    ),
    "come across": (
        [
            "Я случайно наткнулся на старую фотографию.",
            "Она наткнулась на интересную статью.",
            "Мы случайно наткнулись на уютное кафе.",
        ],
        [
            "I CAME ACROSS an old photo.",
            "She CAME ACROSS an interesting article.",
            "We CAME ACROSS a cozy café by chance.",
        ],
    ),
    "run into": (
        [
            "Я случайно встретил старого друга в метро.",
            "Она случайно встретила коллегу в аэропорту.",
            "Мы случайно встретили соседей в супермаркете.",
        ],
        [
            "I RAN INTO an old friend on the metro.",
            "She RAN INTO a colleague at the airport.",
            "We RAN INTO our neighbors at the supermarket.",
        ],
    ),
    "pass away": (
        [
            "Его дедушка ушёл из жизни много лет назад.",
            "Соседка ушла из жизни на прошлой неделе.",
            "Они скорбят о друге, который ушёл из жизни.",
        ],
        [
            "His grandfather PASSED AWAY many years ago.",
            "Our neighbor PASSED AWAY last week.",
            "They mourn a friend who PASSED AWAY.",
        ],
    ),
    "do without": (
        [
            "Можно обойтись без машины в этом районе.",
            "Они как-то обходятся без помощника.",
            "Придётся обойтись без второго монитора.",
        ],
        [
            "You can DO WITHOUT a car in this area.",
            "They somehow DO WITHOUT an assistant.",
            "We'll have to DO WITHOUT a second monitor.",
        ],
    ),
    "put up with": (
        [
            "Она больше не хочет терпеть этот шум.",
            "Сколько можно терпеть такое отношение?",
            "Он терпит задержки только из-за зарплаты.",
        ],
        [
            "She won't PUT UP WITH this noise anymore.",
            "How long can you PUT UP WITH this attitude?",
            "He PUTS UP WITH delays only because of the salary.",
        ],
    ),
    "take back": (
        [
            "Он хотел взять свои слова назад.",
            "Магазин согласился вернуть товар.",
            "Она не может взять назад то, что сказала.",
        ],
        [
            "He wanted to TAKE BACK his words.",
            "The shop agreed to TAKE BACK the product.",
            "She can't TAKE BACK what she said.",
        ],
    ),
    "whether or not": (
        [
            "Независимо от того, согласишься ты или нет, решение уже принято.",
            "Он придёт, независимо от того, позовут его или нет.",
            "Мы поедем, независимо от того, пойдёт дождь или нет.",
        ],
        [
            "WHETHER OR NOT you agree, the decision is made.",
            "He will come WHETHER OR NOT they invite him.",
            "We'll go WHETHER OR NOT it rains.",
        ],
    ),
    "not only ... but also": (
        [
            "Он не только умный, но и очень внимательный.",
            "Город не только красивый, но и удобный для жизни.",
            "Она не только поёт, но и играет на гитаре.",
        ],
        [
            "He is NOT ONLY smart BUT ALSO very attentive.",
            "The city is NOT ONLY beautiful BUT ALSO convenient to live in.",
            "She NOT ONLY sings BUT ALSO plays the guitar.",
        ],
    ),
    "both ... and": (
        [
            "Мне нравятся и чай, и кофе.",
            "Он и работает, и учится одновременно.",
            "В проекте учли и сроки, и бюджет.",
        ],
        [
            "I like BOTH tea AND coffee.",
            "He BOTH works AND studies at the same time.",
            "The project considered BOTH deadlines AND budget.",
        ],
    ),
    "either ... or": (
        [
            "Можно либо остаться, либо уйти сейчас.",
            "Либо ты звонишь, либо я.",
            "Нужно либо согласиться, либо отказаться.",
        ],
        [
            "You can EITHER stay OR leave now.",
            "EITHER you call OR I will.",
            "You must EITHER agree OR refuse.",
        ],
    ),
    "neither ... nor": (
        [
            "Он ни звонил, ни писал.",
            "Мне не нравится ни этот вариант, ни тот.",
            "Они ни пришли, ни предупредили.",
        ],
        [
            "He NEITHER called NOR wrote.",
            "I like NEITHER this option NOR that one.",
            "They NEITHER came NOR warned us.",
        ],
    ),
    "the more ..., the more ...": (
        [
            "Чем больше практикуешься, тем увереннее говоришь.",
            "Чем раньше начнёшь, тем быстрее закончишь.",
            "Чем дольше ждёшь, тем сложнее решиться.",
        ],
        [
            "THE MORE you practise, THE MORE confidently you speak.",
            "THE SOONER you start, THE FASTER you finish.",
            "THE LONGER you wait, THE HARDER it is to decide.",
        ],
    ),
    "one of the most ...": (
        [
            "Это один из самых популярных фильмов года.",
            "Она — одна из самых опытных в команде.",
            "Это один из самых сложных вопросов на экзамене.",
        ],
        [
            "It is ONE OF THE MOST popular films of the year.",
            "She is ONE OF THE MOST experienced people on the team.",
            "This is ONE OF THE MOST difficult exam questions.",
        ],
    ),
}


def _past_form(verb: str) -> str:
    if verb in IRREGULAR_PAST:
        return IRREGULAR_PAST[verb]
    if verb.endswith("e"):
        return verb + "d"
    if verb.endswith("y") and len(verb) > 2 and verb[-2] not in "aeiou":
        return verb[:-1] + "ied"
    if len(verb) >= 2 and verb[-1] not in "aeiou" and verb[-2] in "aeiou" and verb[-3] not in "aeiou":
        return verb + verb[-1] + "ed"
    return verb + "ed"


def phrasal_past(en: str) -> str:
    parts = en.split()
    if len(parts) == 1:
        return _past_form(parts[0])
    verb = parts[0]
    rest = " ".join(parts[1:])
    return f"{_past_form(verb)} {rest}"


def _cap(s: str) -> str:
    return s[0].upper() + s[1:] if s else s


def _ru_cap(s: str) -> str:
    return _cap(s)


def connector_sentences(en: str, ru: str) -> tuple[list[str], list[str]]:
    key = en.lower().replace("’", "'")
    ru_short = primary_ru(ru)

    if key in PHRASAL_SPECIAL:
        return PHRASAL_SPECIAL[key]

    if key in {"because of", "due to", "thanks to"}:
        return (
            [
                f"Мы опоздали {ru_short} пробок.",
                f"Концерт отменили {ru_short} дождя.",
                f"Он добился успеха {ru_short} поддержки команды.",
            ],
            [
                f"We were late {en} the traffic.",
                f"The concert was cancelled {en} the rain.",
                f"He succeeded {en} the team's support.",
            ],
        )

    if key in {"as a result", "therefore", "for this reason"}:
        return (
            [
                f"{_ru_cap(ru_short)}, проект сдали вовремя.",
                f"План не сработал; {ru_short}, мы начали сначала.",
                f"{_ru_cap(ru_short)}, команда получила бонус.",
            ],
            [
                f"{_cap(en)}, the project was delivered on time.",
                f"The plan failed; {en}, we started again.",
                f"{_cap(en)}, the team received a bonus.",
            ],
        )

    if key == "that's why":
        return (
            [
                "Он заболел, вот почему его не было на встрече.",
                "Дорога была закрыта, вот почему мы опоздали.",
                "Я устал, вот почему лёг спать рано.",
            ],
            [
                "He was ill; THAT'S WHY he missed the meeting.",
                "The road was closed; THAT'S WHY we were late.",
                "I was tired; THAT'S WHY I went to bed early.",
            ],
        )

    if key in {"however", "nevertheless", "still", "yet"}:
        return (
            [
                f"{_ru_cap(ru_short)}, идея всё ещё кажется рискованной.",
                f"План сложный; {ru_short}, мы попробуем.",
                f"{_ru_cap(ru_short)}, я согласен попробовать ещё раз.",
            ],
            [
                f"{_cap(en)}, the idea still seems risky.",
                f"The plan is tough; {en}, we'll try.",
                f"{_cap(en)}, I agree to try again.",
            ],
        )

    if key in {"although", "even though"}:
        return (
            [
                f"{_ru_cap(ru_short)} шёл дождь, мы всё равно вышли.",
                f"{_ru_cap(ru_short)} он устал, доклад был отличным.",
                f"{_ru_cap(ru_short)} билеты дорогие, зал был полон.",
            ],
            [
                f"{_cap(en)} it was raining, we still went out.",
                f"{_cap(en)} he was tired, the talk was excellent.",
                f"{_cap(en)} the tickets were expensive, the hall was full.",
            ],
        )

    if key in {"in spite of", "despite"}:
        return (
            [
                f"{_ru_cap(ru_short)} дождя мы вышли на прогулку.",
                f"{_ru_cap(ru_short)} усталости она закончила проект.",
                f"{_ru_cap(ru_short)} пробок они успели вовремя.",
            ],
            [
                f"{_cap(en)} the rain, we went for a walk.",
                f"{_cap(en)} the tiredness, she finished the project.",
                f"{_cap(en)} the traffic, they arrived on time.",
            ],
        )

    if key in {"on the other hand", "while", "whereas"}:
        return (
            [
                f"{_ru_cap(ru_short)}, это может сэкономить деньги.",
                f"Он любит город, {ru_short} она предпочитает природу.",
                f"Один вариант быстрее, {ru_short} другой дешевле.",
            ],
            [
                f"{_cap(en)}, it could save money.",
                f"He loves the city, {en} she prefers nature.",
                f"One option is faster, {en} the other is cheaper.",
            ],
        )

    if key in {"instead of", "rather than"}:
        return (
            [
                f"{_ru_cap(ru_short)} такси мы пошли пешком.",
                f"{_ru_cap(ru_short)} жалоб лучше предложи решение.",
                f"{_ru_cap(ru_short)} кофе он выпил чай.",
            ],
            [
                f"{_cap(en)} taking a taxi, we walked.",
                f"{_cap(en)} complaining, offer a solution.",
                f"{_cap(en)} coffee, he drank tea.",
            ],
        )

    if key in {"and also", "in addition", "besides"}:
        return (
            [
                "Нужно сделать отчёт и также подготовить презентацию.",
                "Кроме того, надо согласовать бюджет.",
                "Она говорит по-английски и также по-испански.",
            ],
            [
                f"We need the report and {en} a presentation.",
                f"{_cap(en)}, we need to approve the budget.",
                f"She speaks English and {en} Spanish.",
            ],
        )

    if key == "as well":
        return (
            [
                "Она говорит по-английски и тоже по-испански.",
                "Мне нравится чай, и кофе тоже.",
                "Он живёт здесь и работает здесь тоже.",
            ],
            [
                "She speaks English and Spanish AS WELL.",
                "I like tea and coffee AS WELL.",
                "He lives here and works here AS WELL.",
            ],
        )

    if key in {"in addition to", "apart from", "except for", "including"}:
        return (
            [
                f"{_ru_cap(ru_short)} зарплаты есть премии.",
                f"{_ru_cap(ru_short)} этого, нужен ещё один документ.",
                f"Все пришли, {ru_short} одного человека.",
            ],
            [
                f"{_cap(en)} the salary, there are bonuses.",
                f"{_cap(en)} this, we need one more document.",
                f"Everyone came {en} one person.",
            ],
        )

    if key in {"for example", "for instance", "such as", "like"}:
        return (
            [
                f"Есть много хобби, {ru_short}, чтение или бег.",
                f"Можно выбрать другой маршрут, {ru_short}, через парк.",
                f"Он изучает языки, {ru_short} немецкий и французский.",
            ],
            [
                f"There are many hobbies, {en}, reading or running.",
                f"You can choose another route, {en}, through the park.",
                f"He studies languages, {en}, German and French.",
            ],
        )

    if key in {"in other words", "that is"}:
        return (
            [
                f"{_ru_cap(ru_short)}, нам нужно больше времени.",
                f"Проект провалился; {ru_short}, бюджет сгорел.",
                f"{_ru_cap(ru_short)}, он просто не пришёл.",
            ],
            [
                f"{_cap(en)}, we need more time.",
                f"The project failed; {en}, the budget was wasted.",
                f"{_cap(en)}, he simply didn't show up.",
            ],
        )

    if key in {"especially", "in particular", "mainly", "in general"}:
        return (
            [
                f"{_ru_cap(ru_short)} зимой цены растут.",
                f"Мне нравится музыка, {ru_short} джаз.",
                f"{_ru_cap(ru_short)} проект прошёл успешно.",
            ],
            [
                f"{_cap(en)} in winter, prices rise.",
                f"I like music, {en} jazz.",
                f"{_cap(en)}, the project went well.",
            ],
        )

    if key in {"first of all", "at first", "then", "after that", "before that", "in the end", "finally", "meanwhile"}:
        seq = {
            "first of all": ("Прежде всего, проверь данные.", "FIRST OF ALL, check the data."),
            "at first": ("Сначала всё казалось простым.", "AT FIRST, everything seemed easy."),
            "then": ("Сначала позвонил, затем написал.", "He called, THEN he texted."),
            "after that": ("Мы поели, после этого пошли гулять.", "We ate; AFTER THAT, we went for a walk."),
            "before that": ("Он переехал; до этого жил у родителей.", "He moved; BEFORE THAT, he lived with his parents."),
            "in the end": ("Спорили долго, но в конце концов договорились.", "They argued for long, but IN THE END they agreed."),
            "finally": ("Мы ждали час и наконец получили ответ.", "We waited an hour and FINALLY got an answer."),
            "meanwhile": ("Он готовил ужин; тем временем я работала.", "He cooked dinner; MEANWHILE, I was working."),
        }
        item = seq[key]
        return (
            [item[0], f"Ещё пример с «{ru_short}» в разговоре.", f"Запомни связку «{en}» для логичной речи."],
            [item[1], f"Another example with {en} in conversation.", f"Remember {en} for clearer speech."],
        )

    if key in {"as soon as", "by the time", "until", "unless", "once", "as long as", "provided that", "in case"}:
        templates = {
            "as soon as": (
                ["Позвони, как только приедешь.", "Как только увижу его, скажу.", "Мы начнём, как только все будут готовы."],
                ["Call me AS SOON AS you arrive.", "I'll tell him AS SOON AS I see him.", "We'll start AS SOON AS everyone is ready."],
            ),
            "by the time": (
                ["К тому времени как поезд пришёл, мы уже устали.", "К тому времени как он вернулся, дождь закончился.", "К тому времени как я проснулся, письмо уже пришло."],
                ["BY THE TIME the train arrived, we were tired.", "BY THE TIME he returned, the rain had stopped.", "BY THE TIME I woke up, the email had arrived."],
            ),
            "until": (
                ["Жди, пока не позвонят.", "Магазин открыт, пока не наступит вечер.", "Не уходи, пока я не вернусь."],
                ["Wait UNTIL they call.", "The shop is open UNTIL evening.", "Don't leave UNTIL I come back."],
            ),
            "unless": (
                ["Не пойду, если не погода не улучшится.", "Он не приедет, если его не попросят.", "Не выключай, если не закончишь."],
                ["I won't go UNLESS the weather improves.", "He won't come UNLESS you ask him.", "Don't switch off UNLESS you finish."],
            ),
            "once": (
                ["Как только попробуешь, поймёшь.", "Как только оплатим, отправят заказ.", "Как только услышишь новость, позвони."],
                ["ONCE you try it, you'll understand.", "ONCE we pay, they'll ship the order.", "ONCE you hear the news, call me."],
            ),
            "as long as": (
                ["Можешь остаться, пока тихо.", "Всё будет хорошо, пока мы на связи.", "Скидка действует, пока есть товар."],
                ["You can stay AS LONG AS it's quiet.", "Everything will be fine AS LONG AS we stay in touch.", "The discount works AS LONG AS stock lasts."],
            ),
            "provided that": (
                ["Согласен, при условии что сроки реальные.", "Поедем, при условии что погода хорошая.", "Подпишу, при условии что условия изменят."],
                ["I agree PROVIDED THAT the deadlines are realistic.", "We'll go PROVIDED THAT the weather is good.", "I'll sign PROVIDED THAT they change the terms."],
            ),
            "in case": (
                ["Возьми зонт на случай если пойдёт дождь.", "Сохрани номер на случай если связь пропадёт.", "Запиши адрес на случай если заблудишься."],
                ["Take an umbrella IN CASE it rains.", "Save the number IN CASE the signal drops.", "Write down the address IN CASE you get lost."],
            ),
        }
        if key in templates:
            return templates[key]

    if key in {"if so", "if not", "from time to time", "sooner or later", "either way", "instead"}:
        templates = {
            "if so": (["Если да, тогда начнём сейчас.", "Ты свободен? Если да, созвонимся.", "Она согласна? Если да, бронируем."], ["IF SO, let's start now.", "Are you free? IF SO, let's call.", "Did she agree? IF SO, we'll book it."]),
            "if not": (["Если нет, попробуем завтра.", "Тебе не подходит? Если нет, найдём другое.", "Не готов? Если нет, подождём."], ["IF NOT, we'll try tomorrow.", "Doesn't suit you? IF NOT, we'll find another.", "Not ready? IF NOT, we'll wait."]),
            "from time to time": (["Мы время от времени ходим в этот ресторан.", "Он время от времени работает из дома.", "Время от времени стоит делать перерыв."], ["We eat at this restaurant FROM TIME TO TIME.", "He works from home FROM TIME TO TIME.", "You should take a break FROM TIME TO TIME."]),
            "sooner or later": (["Рано или поздно правда всплывёт.", "Рано или поздно он ответит.", "Рано или поздно придётся решать."], ["SOONER OR LATER the truth will come out.", "SOONER OR LATER he will reply.", "SOONER OR LATER you'll have to decide."]),
            "either way": (["В любом случае сообщи мне.", "В любом случае нам нужен план B.", "В любом случае встреча состоится."], ["EITHER WAY, let me know.", "EITHER WAY, we need a plan B.", "EITHER WAY, the meeting will happen."]),
            "instead": (["Давай вместо этого выпьем чай.", "Вместо этого предложи другой вариант.", "Я останусь дома вместо похода в кино."], ["Let's drink tea INSTEAD.", "INSTEAD, suggest another option.", "I'll stay home INSTEAD of going to the cinema."]),
        }
        return templates[key]

    if key in {"i think", "i believe", "in my opinion", "as far as i know", "as far as i'm concerned"}:
        return (
            [
                f"{_ru_cap(ru_short)}, это лучший вариант.",
                f"{_ru_cap(ru_short)}, цены слишком высокие.",
                f"{_ru_cap(ru_short)}, нам стоит подождать.",
            ],
            [
                f"{_cap(en)}, this is the best option.",
                f"{_cap(en)}, prices are too high.",
                f"{_cap(en)}, we should wait.",
            ],
        )

    if key in {"according to", "in terms of", "with regard to", "as for"}:
        return (
            [
                f"{_ru_cap(ru_short)} отчёта, продажи выросли.",
                f"{_ru_cap(ru_short)} качества, продукт отличный.",
                f"{_ru_cap(ru_short)} сроков, всё под контролем.",
            ],
            [
                f"{_cap(en)} the report, sales grew.",
                f"{_cap(en)} quality, the product is excellent.",
                f"{_cap(en)} deadlines, everything is under control.",
            ],
        )

    if key in {"compared with", "compared to"}:
        return (
            [
                f"{_ru_cap(ru_short)} прошлого года прибыль выше.",
                f"{_ru_cap(ru_short)} конкурентов наш сервис быстрее.",
                f"{_ru_cap(ru_short)} планом мы опережаем график.",
            ],
            [
                f"{_cap(en)} last year, profit is higher.",
                f"{_cap(en)} competitors, our service is faster.",
                f"{_cap(en)} the plan, we are ahead of schedule.",
            ],
        )

    if key == "as well as":
        return (
            [
                "Она знает французский, а также немецкий.",
                "Нужен отчёт, а также краткая презентация.",
                "Он играет на гитаре, а также поёт.",
            ],
            [
                "She knows French AS WELL AS German.",
                "We need a report AS WELL AS a short presentation.",
                "He plays the guitar AS WELL AS sings.",
            ],
        )

    if key == "for one thing":
        return (
            [
                "Во-первых, это слишком дорого.",
                "Во-первых, у нас нет времени.",
                "Во-первых, решение уже принято.",
            ],
            [
                "FOR ONE THING, it's too expensive.",
                "FOR ONE THING, we don't have time.",
                "FOR ONE THING, the decision is already made.",
            ],
        )

    return (
        [
            f"Пример с «{ru_short}» в начале предложения.",
            f"Ещё одно предложение со связкой «{en}».",
            f"Запомни: {ru_short}.",
        ],
        [
            f"{_cap(en)}, this makes the sentence clearer.",
            f"Use {en} to connect your ideas logically.",
            f"Another sentence with {en}.",
        ],
    )


def phrasal_sentences(en: str, ru: str) -> tuple[list[str], list[str]]:
    key = en.lower()
    if key in PHRASAL_SPECIAL:
        return PHRASAL_SPECIAL[key]

    meaning = primary_ru(ru)
    past = phrasal_past(en)

    if key == "hold on":
        return (
            ["Подожди секунду, я сейчас.", "Подожди, я ищу документ.", "Подожди, не клади трубку."],
            ["HOLD ON a second, please.", "HOLD ON, I'm looking for the file.", "HOLD ON, don't hang up."],
        )

    if key.endswith(" up") and meaning.endswith(("ать", "яться", "ться")):
        return (
            [
                f"Каждый день приходится {meaning} рано.",
                f"Вчера было трудно {meaning}.",
                f"Не забудь {meaning} перед выходом.",
            ],
            [
                f"I have to {en} early every day.",
                f"Yesterday it was hard to {en}.",
                f"Don't forget to {en} before you leave.",
            ],
        )

    templates = [
        (
            [
                f"Каждый день приходится {meaning}.",
                f"Сегодня ему было трудно {meaning}.",
                f"Она решила {meaning} пораньше обычного.",
            ],
            [
                f"I have to {en} every day.",
                f"Today it was hard to {en}.",
                f"She decided to {en} earlier than usual.",
            ],
        ),
        (
            [
                f"Вчера он смог {meaning} без проблем.",
                f"Нам нужно {meaning} до вечера.",
                f"По выходным они обычно этим занимаются.",
            ],
            [
                f"Yesterday he {past} without problems.",
                f"We need to {en} before evening.",
                f"They usually {en} at weekends.",
            ],
        ),
        (
            [
                f"Не забудь {meaning}.",
                f"Когда ты последний раз мог {meaning}?",
                f"Без этого нельзя {meaning}.",
            ],
            [
                f"Don't forget to {en}.",
                f"When did you last {en}?",
                f"You can't {en} without this.",
            ],
        ),
    ]
    idx = sum(ord(c) for c in en) % len(templates)
    return templates[idx]


def connector_related(en: str) -> tuple[str, str, str, str]:
    key = en.lower().replace("’", "'")
    if key in {"because of", "due to"}:
        return "—", "cause / reason", "—", CONNECTOR_OPPOSITES.get(key, "—")
    if key in {"thanks to"}:
        return "—", "gratitude", "—", CONNECTOR_OPPOSITES.get(key, "—")
    if key in {"however", "therefore", "although"}:
        return "—", "linker", "—", CONNECTOR_OPPOSITES.get(key, "—")
    if key.startswith("i "):
        return "—", "opinion", "—", "—"
    return "—", "linker / phrase", "—", CONNECTOR_OPPOSITES.get(key, "—")


def phrasal_related(en: str) -> tuple[str, str, str, str]:
    return f"to {en}", "—", "—", CONNECTOR_OPPOSITES.get(en.lower(), "—")
