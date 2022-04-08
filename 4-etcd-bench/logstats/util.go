package main

import (
	"fmt"
	"os"
)

func writeTotalSizeIntoFile(size int64, fname string) error {
	fd, err := os.OpenFile(fname, os.O_CREATE|os.O_TRUNC|os.O_WRONLY|os.O_APPEND, 0600)
	if err != nil {
		return err
	}
	defer fd.Close()

	if _, err := fmt.Fprintf(fd, "%d\n", size); err != nil {
		return err
	}
	return nil
}

func writeCommandCountsIntoFile(counts []int, fname string) error {
	fd, err := os.OpenFile(fname, os.O_CREATE|os.O_TRUNC|os.O_WRONLY|os.O_APPEND, 0600)
	if err != nil {
		return err
	}
	defer fd.Close()

	for _, c := range counts {
		if _, err := fmt.Fprintf(fd, "%d\n", c); err != nil {
			return err
		}
	}
	return nil
}
