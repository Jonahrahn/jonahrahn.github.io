.PHONY: validate score leaderboard clean

validate:
	python -m harness.validate data/*.jsonl

score:
	@for f in results/*.jsonl; do \
		echo "==== $$f ===="; \
		python -m harness.score $$f; \
	done

leaderboard:
	python -m harness.leaderboard

clean:
	rm -f results/*.jsonl
