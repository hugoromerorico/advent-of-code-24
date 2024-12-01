.PHONY: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25

# Create directories and files for Advent of Code days
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25:
	cd "/Users/hugoromero/Documents/GitHub/advent-of-code-24" && \
	rm -rf $@ && \
	mkdir -p $@ && \
	cd $@ && touch 1.py 2.py && \
	curl -s https://adventofcode.com/2024/day/$@ | awk '/<main>/{flag=1;next}/<\/main>/{flag=0}flag' | sed 's/<[^>]*>//g' > problem.md && \
	curl -s --cookie "session=$$(cat ../.env | grep COOKIE | cut -d '=' -f2)" https://adventofcode.com/2024/day/$@/input > in.txt