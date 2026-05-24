package main

import (
	"fmt"

	"github.com/shopspring/decimal"
)

func main() {
	value := "400.20"

	amount, err := decimal.NewFromString(value)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println("val: " + amount.String())
		fmt.Println(amount.Add(decimal.NewFromInt(3)))
	}
}
