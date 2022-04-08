package main

import (
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

const (
	logSizeFname  = "logsize.out"
	logCountFname = "logcounts.out"
	logFileExt    = ".log"
)

var folderNames = []string{
	"../logs-PL-10/",
}

// e.g. 10-15 -> 6 commands
func getCommandCountFromName(name string) (int, error) {
	logIndexes := strings.Split(name, "-")
	if len(logIndexes) != 2 {
		return 0, nil
	}

	first, err := strconv.Atoi(logIndexes[0])
	if err != nil {
		return 0, err
	}

	last, err := strconv.Atoi(logIndexes[1])
	if err != nil {
		return 0, err
	}
	return last - first + 1, nil
}

func generateLogTotalSize(folder string) int64 {
	totalSize := int64(0)

	walkfn := filepath.WalkFunc(func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if filepath.Ext(info.Name()) != logFileExt {
			return nil
		}

		totalSize += info.Size()
		return nil
	})
	filepath.Walk(folder, walkfn)
	return totalSize
}

func generateLogCommandsCount(folder string) ([]int, error) {
	commandCounts := make([]int, 0)

	walkfn := filepath.WalkFunc(func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if filepath.Ext(info.Name()) != logFileExt {
			return nil
		}

		name := strings.TrimSuffix(info.Name(), filepath.Ext(info.Name()))
		count, err := getCommandCountFromName(name)
		if err != nil {
			return err
		}

		if count > 0 {
			commandCounts = append(commandCounts, count)
		}
		return nil
	})
	err := filepath.Walk(folder, walkfn)
	return commandCounts, err
}

func main() {
	for _, folder := range folderNames {
		size := generateLogTotalSize(folder)
		counts, err := generateLogCommandsCount(folder)
		if err != nil {
			log.Fatalf("failed calculating counts on %s, err: %s\n", folder, err.Error())
		}

		fn := folder + logSizeFname
		if err := writeTotalSizeIntoFile(size, fn); err != nil {
			log.Fatalf("failed writing size on %s, err: %s\n", fn, err.Error())
		}

		fn = folder + logCountFname
		if err := writeCommandCountsIntoFile(counts, fn); err != nil {
			log.Fatalf("failed writing size on %s, err: %s\n", fn, err.Error())
		}
	}
}
