#!/usr/bin/env Rscript
read_input <- function() {
	input <- read.table("input.txt", header=FALSE)
	return(input)
}

part2_old <- function(input) {
	frequency <- 0
	outcome <- c(0)
	while (TRUE) {
		for (freq_adjust in input$V1) {
			frequency <- frequency + freq_adjust
			if (is.element(frequency, outcome)) {
				return(frequency)
			}
			outcome <- c(outcome, frequency)
		}	
	}
}

part2_new <- function(input) {
	running_total <- 0

	offset <- 1000
	count_list <- integer(200000)

	while (TRUE) {
		for (freq_adjust in input$V1) {
			running_total <- running_total + freq_adjust
			if (count_list[offset + running_total] == 1) {
				return(running_total)
			}

			count_list[offset + running_total] <- 1
		}	
	}
}

input <- read_input()
# Deel 1
print(sum(input))
# Deel 2
print(part2_new(input))
