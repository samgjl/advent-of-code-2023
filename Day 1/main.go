package main

import (
	"fmt"
	"log"
	"os"
	"strings"
	"unicode"
)

func ReadFile() string {
	fmt.Printf("\n\nReading a file in Go lang\n")
	fileName := "input.txt"

	data, err := os.ReadFile(fileName)
	if err != nil {
		log.Panicf("failed reading data from file: %s", err)
	}
	return string(data)
}

func get_digits(input []string) []int {
	result := make([]int, len(input))
	for i, str := range input {
		// iterate through each character in i if it is a digit set first degit to that value
		runes := []rune(str)
		var first_digit, last_digit int

		// forward loop, checks for first digit:
		for _, char := range runes {
			if unicode.IsDigit(char) {
				first_digit = int(char-'0') * 10
				break
			}
		}
		// for loop going in reverse order of runes
		for j := len(runes) - 1; j >= 0; j-- {
			char := runes[j]
			if unicode.IsDigit(char) {
				last_digit = int(char - '0')
				break
			}
		}

		result[i] = int(first_digit + last_digit)
	}

	return result
}

// main function
func main() {
	input := ReadFile()
	lines := strings.Split(input, "\n")
	just_digits := get_digits(lines)

	// sum the digits
	total := 0
	for _, num := range just_digits {
		total += num
	}
	fmt.Println("\n\nTotal:", total)

}
