#!/usr/bin/env Rscript
read_input <- function() {
	input <- read.table("input.txt", header=FALSE)
	return(as.matrix(input$V1)[,1])
}

part1 <- function(input) {
	two_count <- 0
	three_count <- 0
	for (box_id in input) {
		numerical <- utf8ToInt(box_id) - utf8ToInt("a")
		counts <- integer(26)
		for (n in numerical) {
			counts[n + 1] <- counts[n + 1] + 1
		}
		two_count <- two_count + is.element(2, counts)
		three_count <- three_count + is.element(3, counts)
	}
	return(two_count * three_count)
}

difference <- function(s1, s2) {
	return(sum(utf8ToInt(s1) != utf8ToInt(s2)))
}

overlap <- function(s1, s2) {
	l1 <- strsplit(s1, "")[[1]]
	l2 <- strsplit(s2, "")[[1]]
	output <- c()
	for (i in 1:length(l1))
		if (l1[i] == l2[i])
			output <- c(output, l1[i])
	return(paste(output, collapse=""))
}

part2 <- function(input) {
	for (i in 1:length(input)) {
		for (j in (i+1):length(input)) {
			if (difference(input[[i]], input[[j]]) == 1)
				return(overlap(input[i], input[j]))
		}
	}
}


input <- read_input()
print(part1(input))
print(part2(input))
