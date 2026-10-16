---
title: "Undergraduate teaching assistant"
collection: teaching
type: "Teaching Assistant"
permalink: /teaching/2018-goshen-college
venue: "Goshen College"
date: 2017-09-01
terms: "2017–2018"
location: "Goshen, IN"
courses:
  - course: "General Chemistry II"
    terms: "Spring 2018"
  - course: "Organismal Biology"
    terms: "Spring 2018"
  - course: "Introductory Chemistry"
    terms: "Fall 2017"
---
{% for c in page.courses %}
* {{ c.course }}, {{ c.terms }}
{% endfor %}
