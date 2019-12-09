# AutoRIA Car monitoring

Simple web application for creating model/brand car monitoring from AutoRIA website. Application should notify user about changes in current monitoring (e.g. price for specific car has changed)

## Setup

Backend:
 - `pipenv install --dev`
 - `pipenv shell`
 - `./manage.py migrate`
 - `make server`
 - `make celery` 
 - `make celery-beat`

Frontend:
 - `cd autoria && yarn` (or `npm install`)
 - `yarn run dev`(or `npm run dev`)

Using docker:
 - `docker-compose up`

## TODOs

- [x] ~~Create script for populating database using Autoria API data~~
- [x] ~~Create custom `PeriodicTask` with `query_string` and `user`~~
- [ ] Create scraper for parsing/updating existing advertisements
- [ ] Add celery task for checking `MonitorResult` models and notify related user via linked services (e.g. Telegram or email )