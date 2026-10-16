---
title: "Guest lectures"
collection: teaching
type: "Guest lecturer"
permalink: /teaching/guest-lectures
venue: "Universities and colleges in Minnesota and South Dakota"
date: 2025-09-01          # set to your most recent lecture so this sorts first
terms: "2020–present"
# Add a lecture by copying one block below. The Teaching page and the CV both read this list.
lectures:
  - course: "Introduction to Fisheries, Wildlife and Conservation Biology"
    institution: "University of Minnesota"
    terms: "Fall 2025"
  - course: "Vertebrate Field Methods"
    institution: "University of Minnesota"
    terms: "Fall 2020, 2022, 2025; Spring 2021, 2023, 2024"
  - course: "Principles of Wildlife Management"
    institution: "University of Minnesota"
    terms: "Fall 2023"
  - course: "Field Biology"
    institution: "Anoka-Ramsey Community College"
    terms: "Fall 2020, 2022, 2024; Spring 2020–2022, 2025"
  - course: "GIS in Environmental Science and Management"
    institution: "St. Thomas University"
    terms: "Spring 2024"
  - course: "Principles of Wildlife Management"
    institution: "South Dakota State University"
    terms: "Fall 2022"
  - course: "Urban Ecology"
    institution: "Concordia College"
    terms: "Spring 2021"
  - course: "Animal Ethics"
    institution: "Macalester College"
    terms: "Spring 2021"
---
Guest lectures on urban carnivore ecology, wildlife field methods, and spatial analysis.

{% for l in page.lectures %}
* **{{ l.course }}**, {{ l.institution }} ({{ l.terms }})
{% endfor %}
