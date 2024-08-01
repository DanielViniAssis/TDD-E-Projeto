run:
	@uvicorn store.main:app --reload

precommit-install:
<<<<<<< HEAD
	@poetry run pre-commit install

test:
	@poetry run pytest

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/
=======
    @poetry run pre-commit install
>>>>>>> f44af51a971f61c5e771acb97d8ff8fdabaf3363
