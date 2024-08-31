.PHONY: check-code fix-code

check-code:
	@python -m flake8 simple_chat
	@python -m isort simple_chat --check
	@python -m black simple_chat --check

fix-code:
	@python -m isort simple_chat
	@python -m black simple_chat
