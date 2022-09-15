package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
)

const (
	compressFname   = "logs.tar.gz"
	logSizeFname    = "logsize.out"
	logBatchesFname = "logbatches.out"
	logCountFname   = "logcounts.out"

	logFileExt = ".log"
	walFileExt = ".wal"
)

var folderNames = []string{
	"../exp/pl-300",
	"../exp/pl-600",
	"../exp/pl-900",
	"../exp/pl-1200",
	"../exp/sl-1",
}

var workloads = []string{
	"workloada",
	"workloadalatest",
	"workloadaprime",
	"workloadb",
	"workloadc",
	"workloadd",
}

// e.g. 10-15-2 -> 6 commands batch, 2 commands within
func getBatchAndCommandCountFromName(name string) (int, int, error) {
	logIndexes := strings.Split(name, "-")
	if len(logIndexes) != 3 {
		return 0, 0, nil
	}

	first, err := strconv.Atoi(logIndexes[0])
	if err != nil {
		return 0, 0, err
	}

	last, err := strconv.Atoi(logIndexes[1])
	if err != nil {
		return 0, 0, err
	}

	count, err := strconv.Atoi(logIndexes[2])
	if err != nil {
		return 0, 0, err
	}
	return last - first + 1, count, nil
}

func GenerateLogStats(folder string) (*LogStats, error) {
	stats := newLogStats()

	walkfn := filepath.WalkFunc(func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if ext := filepath.Ext(info.Name()); ext != logFileExt && ext != walFileExt {
			return nil
		}
		stats.TotalSize += info.Size()

		name := strings.TrimSuffix(info.Name(), filepath.Ext(info.Name()))
		batch, count, err := getBatchAndCommandCountFromName(name)
		if err != nil {
			return err
		}

		stats.BatchSizes = append(stats.BatchSizes, batch)
		stats.CommandCounts = append(stats.CommandCounts, count)
		return nil
	})
	err := filepath.Walk(folder, walkfn)
	return stats, err
}

func decompressLogFile(logFile, dest string) error {
	return exec.Command("tar", "-xzf", logFile, "-C", dest).Run()
}

func deleteDecompressLogsOnDir(dir string) error {
	files, err := filepath.Glob(dir + "*.log")
	if err != nil {
		return err
	}

	for _, f := range files {
		if err := os.Remove(f); err != nil {
			return err
		}
	}
	return nil
}

func main() {
	for _, folder := range folderNames {
		for _, workload := range workloads {
			dest := fmt.Sprintf("%s/%s/", folder, workload)
			if err := decompressLogFile(dest+compressFname, dest); err != nil {
				log.Fatalf("failed decompressing log file at '%s', err: %s\n", dest, err.Error())
			}

			dir := folder + "/" + workload + "/"
			stats, err := GenerateLogStats(dir)
			if err != nil {
				log.Fatalf("failed calculating log stats on %s, err: %s\n", dir, err.Error())
			}

			if err := stats.WriteToFile(dir); err != nil {
				log.Fatalf("failed writing log stats, err: %s\n", err.Error())
			}

			if err := deleteDecompressLogsOnDir(dest); err != nil {
				log.Fatalf("failed deleting logs at '%s', err: %s\n", dest, err.Error())
			}
		}
	}
}

type LogStats struct {
	BatchSizes    []int
	CommandCounts []int
	TotalSize     int64
}

func newLogStats() *LogStats {
	return &LogStats{
		BatchSizes:    make([]int, 0),
		CommandCounts: make([]int, 0),
	}
}

func (stats *LogStats) WriteToFile(folder string) error {
	fn := folder + logSizeFname
	if err := writeInt64IntoFile(stats.TotalSize, fn); err != nil {
		return err
	}

	fn = folder + logBatchesFname
	if err := writeIntSliceIntoFile(stats.BatchSizes, fn); err != nil {
		return err
	}

	fn = folder + logCountFname
	if err := writeIntSliceIntoFile(stats.CommandCounts, fn); err != nil {
		return err
	}
	return nil
}

func writeInt64IntoFile(size int64, fname string) error {
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

func writeIntSliceIntoFile(counts []int, fname string) error {
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
