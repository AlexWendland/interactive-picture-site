# interactive-picture-site

A simple html site to have a interactive slide show and realtime drawing functionality.

## Setup

1. Set up a new python virtual environment with python 3.11.9.
2. Install the requirements with `pip install -r requirements.txt`.
3. Setup poetry with `poetry install`.
4. Set up the pre-commit hooks with `pre-commit install`.

## Run the server

To run the server use `poetry run start` the server then can be accessed on `http://127.0.0.1:5000/`.

## To do list

- [ ] Buffer drawn points and retransmit upon subscription.
- [ ] Implement clear button.
- [ ] Implement pause/play button.
- [ ] Implement speed up/ spow down button.
- [ ] Take photos from google drive/self hosted photos site.
- [ ] (BUG) Drawing seems to disapear occationally.
- [ ] (BUG) Random picture rezising whilst streaming.
