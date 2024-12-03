.PHONY: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 \
        1_2 2_2 3_2 4_2 5_2 6_2 7_2 8_2 9_2 10_2 11_2 12_2 13_2 14_2 15_2 16_2 17_2 18_2 19_2 20_2 21_2 22_2 23_2 24_2 25_2

# Create directories and files for Advent of Code days (part 1)
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25:
	@if curl -s https://adventofcode.com/2024/day/$@ | grep -q "Please don't repeatedly request this endpoint"; then \
		echo "Problem $@ is not available yet"; \
		exit 1; \
	else \
		cd "/Users/hugoromero/Documents/GitHub/advent-of-code-24" && \
		rm -rf $@ && \
		mkdir -p $@ && \
		cd $@ && \
		for i in {1..5}; do \
			curl -s https://adventofcode.com/2024/day/$@ | awk '/<main>/{flag=1;next}/<\/main>/{flag=0}flag' | sed 's/<[^>]*>//g' > problem.md; \
			if ! grep -q "Internal Server Error" problem.md && [ -s problem.md ]; then break; \
			else echo "Retrying problem.md download ($$i/5)..."; sleep 2; fi; \
			if [ $$i -eq 5 ]; then echo "Failed to download problem.md after 5 attempts"; exit 1; fi; \
		done && \
		for i in {1..5}; do \
			curl -s --cookie "session=$$(cat ../.env | grep COOKIE | cut -d '=' -f2)" https://adventofcode.com/2024/day/$@/input > in.txt; \
			if ! grep -q "Internal Server Error" in.txt && [ -s in.txt ]; then break; \
			else echo "Retrying input download ($$i/5)..."; sleep 2; fi; \
			if [ $$i -eq 5 ]; then echo "Failed to download input after 5 attempts"; exit 1; fi; \
		done && \
		cd .. && python3 claude.py $@ && cd $@ && python3 exec.py; \
	fi

# Create directories and files for part 2 of each day
1_2 2_2 3_2 4_2 5_2 6_2 7_2 8_2 9_2 10_2 11_2 12_2 13_2 14_2 15_2 16_2 17_2 18_2 19_2 20_2 21_2 22_2 23_2 24_2 25_2:
	$(eval NUM=$(shell echo $@ | cut -d '_' -f1))
	cd "/Users/hugoromero/Documents/GitHub/advent-of-code-24" && \
	rm -rf $@ && \
	mkdir -p $@ && \
	cd $@ && \
	for i in {1..5}; do \
		curl -s --cookie "session=$$(cat ../.env | grep COOKIE | cut -d '=' -f2)" https://adventofcode.com/2024/day/$(NUM) | awk '/<main>/{flag=1;next}/<\/main>/{flag=0}flag' | sed 's/<[^>]*>//g' > problem.md; \
		if ! grep -q "Internal Server Error" problem.md && [ -s problem.md ]; then break; \
		else echo "Retrying problem.md download ($$i/5)..."; sleep 2; fi; \
		if [ $$i -eq 5 ]; then echo "Failed to download problem.md after 5 attempts"; exit 1; fi; \
	done && \
	cp ../$(NUM)/in.txt . && \
	cd .. && python3 claude_part2.py $@ && cd $@ && python3 exec.py

# Retry targets for both part 1 and part 2
retry_%:
	@cd "/Users/hugoromero/Documents/GitHub/advent-of-code-24" && \
	python retry.py $* $(filter-out $@,$(MAKECMDGOALS)) && \
	cd $* && \
	python exec.py && \
	cd ..

# Helper target to handle the wrong_output argument
%:
	@:

.SILENT: retry_%