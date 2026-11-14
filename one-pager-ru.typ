// Сборка: typst compile one-pager.typ one-pager.pdf
// Точки правки — только эти четыре строки:
#let contact-email = "beattle1984@gmail.com"
#let contact-linkedin = "https://www.linkedin.com/in/evgeny-dolgov-research/"
#let repo-example = "github.com/sensus-stoa/permutation-test-ml"
#let details-url = "https://github.com/sensus-stoa/engineering-verdict/blob/main/service-description.ru.md"

#set page(paper: "a4", margin: (x: 17mm, y: 15mm))
#set text(font: ("Libertinus Serif", "DejaVu Sans"), size: 10.5pt, lang: "ru")
#set par(leading: 0.6em, justify: false)

#let accent = rgb("#1f3a5f")
#let bad = rgb("#b03a2e")
#let pale = rgb("#e6e6e6")

#let card(title, body) = rect(
  width: 100%, inset: 8pt, radius: 3pt,
  stroke: 0.6pt + rgb("#d5d5d5"), fill: rgb("#fafafa")
)[
  #text(size: 8.5pt, weight: "bold", fill: accent)[#title]
  #v(4pt)
  #text(size: 9.5pt)[#body]
]

#text(size: 15pt, weight: "bold", fill: accent)[
  Проверка одного утверждения о вашей модели
]
#v(3pt)
Евгений Долгов. 15 лет бэкенд и архитектура. Один человек, не агентство.
#v(9pt)

#grid(
  columns: (1fr, auto, 1fr, auto, 1fr), gutter: 5pt,
  card("ВЫ ДАЁТЕ", [Одно утверждение \ Код и настройки \ Данные или запуск у вас]),
  align(center + horizon, text(size: 13pt, fill: accent)[#sym.arrow.r]),
  card("МЫ ДЕЛАЕМ", [Фиксируем критерии до прогона \ Повторяем расчёт \ Проверяем на пустышке]),
  align(center + horizon, text(size: 13pt, fill: accent)[#sym.arrow.r]),
  card("ВЫ ПОЛУЧАЕТЕ", [Подтверждено / не подтверждено / данных мало \ Где вывод применять нельзя]),
)
#v(10pt)

#text(weight: "bold")[Типовая ошибка.] Модель показывала 3% ошибки в тесте и 12% в работе.
В тест ей подавали фактическую погоду за тот же день. В продакшене накануне доступен только
прогноз. Модель заглядывала в будущее, тест этого не ловил.
#v(9pt)

#let marks = range(50).map(i => rect(
  width: 7pt, height: 7pt, radius: 1pt, stroke: none,
  fill: if i < 36 { bad } else { pale }
))

#grid(columns: (auto, 1fr), gutter: 12pt,
  [
    #grid(columns: 10, gutter: 2.5pt, ..marks)
    #v(3pt)
    #text(size: 8.5pt, fill: bad)[36 из 50]
  ],
  [
    #text(weight: "bold")[Почему нам можно верить.] В нашем открытом примере
    наивная проверка приняла чистый шум за сигнал в 36 случаях из 50. Мы это
    измерили и опубликовали  вместе с тем, где наш метод не работает.
    Сколько ошибок пропускает сама наша процедура, опубликуем до первой платной проверки.
  ],
)
#v(10pt)
#line(length: 100%, stroke: 0.5pt + rgb("#dddddd"))
#v(7pt)

#grid(columns: (1fr, 1fr), gutter: 12pt,
  [
    #text(weight: "bold")[Цена и срок.] Ориентир: 73–110 тыс ₽ (800–1200 €) Точная цена, после оценки объёма, 3–5 рабочих дней
    от получения материалов.
  ],
  [
    #text(weight: "bold")[Чего не делаем.] Не обучаем модель. Не выдаём
    сертификат. Не обещаем, что она не сломается.
  ],
)
#v(9pt)
#line(length: 100%, stroke: 0.5pt + rgb("#dddddd"))
#v(6pt)
#text(size: 9pt)[
  Пример: #link("https://" + repo-example)[#repo-example] - синтетические данные; проверок на данных энергетики пока не было \
  Протокол проверки: #link("https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust")[https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust] \
  Подробное описание: #link(details-url)[#details-url] \
  Связь: #contact-email · LinkedIn #link(contact-linkedin)[#contact-linkedin]
]
