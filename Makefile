.PHONY: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 \
        1_2 2_2 3_2 4_2 5_2 6_2 7_2 8_2 9_2 10_2 11_2 12_2 13_2 14_2 15_2 16_2 17_2 18_2 19_2 20_2 21_2 22_2 23_2 24_2 25_2

# Create directories and files for Advent of Code days (part 1)
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25:
	cd "/Users/hugoromero/Documents/GitHub/advent-of-code-24" && \
	rm -rf $@ && \
	mkdir -p $@ && \
	cd $@ && \
	curl -s https://adventofcode.com/2024/day/$@ | awk '/<main>/{flag=1;next}/<\/main>/{flag=0}flag' | sed 's/<[^>]*>//g' > problem.md && \
	curl -s --cookie "session=$$(cat ../.env | grep COOKIE | cut -d '=' -f2)" https://adventofcode.com/2024/day/$@/input > in.txt && \
	cd .. && python3 claude.py $@ && cd $@ && python3 exec.py

# Create directories and files for part 2 of each day
1_2 2_2 3_2 4_2 5_2 6_2 7_2 8_2 9_2 10_2 11_2 12_2 13_2 14_2 15_2 16_2 17_2 18_2 19_2 20_2 21_2 22_2 23_2 24_2 25_2:
	$(eval NUM=$(shell echo $@ | cut -d '_' -f1))
	cd "/Users/hugoromero/Documents/GitHub/advent-of-code-24" && \
	rm -rf $@ && \
	mkdir -p $@ && \
	cd $@ && \
	curl -s --cookie "session=$$(cat ../.env | grep COOKIE | cut -d '=' -f2)" https://adventofcode.com/2024/day/$(NUM) | awk '/<main>/{flag=1;next}/<\/main>/{flag=0}flag' | sed 's/<[^>]*>//g' > problem.md && \
	cp ../$(NUM)/in.txt . && \
	cd .. && python3 claude_part2.py $@ && cd $@ && python3 exec.py