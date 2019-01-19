# Questioner
Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or bottom of the log.

[![Build Status](https://travis-ci.org/wangonya/questioner2.svg?branch=develop)](https://travis-ci.org/wangonya/questioner2)
[![Coverage Status](https://coveralls.io/repos/github/wangonya/questioner2/badge.svg?branch=develop)](https://coveralls.io/github/wangonya/questioner2?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/0bf11a400ebb58b88a1e/maintainability)](https://codeclimate.com/github/wangonya/questioner2/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ebf163e6a2104fd6b05835bc40a4428a)](https://www.codacy.com/app/wangonya/questioner2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wangonya/questioner2&amp;utm_campaign=Badge_Grade)

## Api endpoints
|Endpoint                                    |Functionality                     |Route                                      |
|--------------------------------------------|----------------------------------|-------------------------------------------|
|POST /signup                                |Register new user                 |/api/v2/auth/signup                        |
|POST /login                                 |Login registered user             |/api/v2/auth/login                         |
|POST /reset                                 |Reset password                    |/api/v2/auth/reset                         |
|POST /meetups*                              |Create new meetup                 |/api/v2/meetups                            |
|GET /meetups/meetup-id                      |Fetch specific meetup record      |/api/v2/meetups/meetup-id                  |
|GET /meetups/upcoming                       |Get all upcoming meetups          |/api/v2/meetups/upcoming                   |
|POST /meetups/meetup-id/questions           |Post a new question on a meetup   |/api/v2/meetups/meetup-id/questions        |
|PATCH /questions/question-id/upvote         |Upvote a specific question        |/api/v2/questions/question-id/upvote       |
|PATCH /questions/question-id/downvote       |Downvote a specific question      |/api/v2/questions/question-id/downvote     |
|POST /meetups/meetup-id/rsvps               |Respond to meetup RSVP            |/api/v2/meetups/meetup-id/rsvps            |

**Endpoints marked with * are only accessible to admin users**

## How to run the app
*  Clone the repo
*  Activate `virtualenv venv` and run `pip3 install requirements.txt`
*  `export FLASK_APP=run.py`
*  Run `python3 -m flask run`
*  Use a Rest client to test the endpoints

## Running tests
*  Pytest is used as the test client. In the project directory, run: `pytest -vv` to run the tests, or `pytest -cov=/app` to see the coverage