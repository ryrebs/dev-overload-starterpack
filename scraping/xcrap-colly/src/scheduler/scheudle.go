package scheduler

import (
	"scraper/backend/scraper"
	"scraper/backend/util"
	"time"

	"github.com/carlescere/scheduler"
)

func job() {
	util.LogWhenDev("Starting job scrape", time.Now().String())
	exitCh := make(chan struct{})
	// TODO: Create indeces for searching
	// TODO: Change prod setup
	// scraper.DeletePreviousData()
	// scraper.Scrape()
	// # Prod
	scheduler.Every().Day().At("23:00").Run(scraper.DeletePreviousData)
	scheduler.Every().Day().At("00:00").Run(scraper.Scrape)
	<-exitCh
}
