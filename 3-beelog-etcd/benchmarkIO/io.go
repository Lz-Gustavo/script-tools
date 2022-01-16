package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

const (
	logFile = `
		111003
		111003
		1
		��user7239563004053864699"�"
		user7239563004053864699dKGfTHQDHiVQzXThVVsJTvVZZbjJtoBwfXCHDpqElkmpUkmfZIJWLcYUDElGzqjkYggpdSNxkCOfJkuvuSwoPYewBivPzrhnRaTkN�
		�ĭ��̟�"
		EOL
	`

	iterations int = 1000000
)

func main() {
	args := os.Args
	if len(args) != 2 {
		log.Fatalln("run as", args[0], "path/to/file.out")
	}

	t1 := run(args[1], false)
	ave := calculateAverage(t1)
	fmt.Printf("average nanosec on non-sync: %f\n", ave)

	t2 := run(args[1]+".sync", true)
	ave = calculateAverage(t2)
	fmt.Printf("average nanosec on sync: %f\n", ave)
}

func run(filename string, sync bool) []int64 {
	dur := make([]int64, 0)
	for i := 0; i < iterations; i++ {
		fn := filename + "." + strconv.Itoa(i) + ".out"
		fd := createTestFile(fn, sync)

		start := time.Now()
		fmt.Fprintf(fd, "%s", logFile)
		end := time.Since(start)

		dur = append(dur, end.Nanoseconds())
		fd.Close()
		deleteFile(fn)
	}
	return dur
}

func calculateAverage(arr []int64) float64 {
	var sum float64
	for _, v := range arr {
		sum += float64(v)
	}
	return sum / float64(len(arr))
}

func createTestFile(filename string, sync bool) *os.File {
	flags := os.O_CREATE | os.O_TRUNC | os.O_WRONLY
	if sync {
		flags = flags | os.O_SYNC
	}

	fd, err := os.OpenFile(filename, flags, 0600)
	if err != nil {
		log.Fatalln("failed creating test file, err:", err.Error())
	}
	return fd
}

func deleteFile(filename string) {
	if err := os.Remove(filename); err != nil {
		log.Fatalln("failed deleting test file, err:", err.Error())
	}
}
