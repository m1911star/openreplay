package main

import (
	"github.com/google/uuid"
)

func getUUID(u *string) string {
	if u != nil {
		_, err := uuid.Parse(*u)
		if err == nil {
			return *u
		}
	}
	return uuid.New().String()
}