package scraper

import (
	"crypto/tls"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"scraper/backend/util"
	"strings"
	"time"

	"github.com/antchfx/htmlquery"
	"github.com/gocolly/colly/v2"
	"github.com/gocolly/colly/v2/debug"
	"github.com/gocolly/colly/v2/extensions"
	"github.com/gocolly/colly/v2/proxy"
	"github.com/gocolly/colly/v2/queue"
	"github.com/gocolly/redisstorage"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"golang.org/x/net/html"
)

// App specific config
const (
	allowed1 = ""
	allowed2 = ""
	MAX_SIZE = 50
)

var panickRecover = func() {
	if err := recover(); err != nil {
		log.Println("Error: ", err)
	}
}
var defaultCollection *mongo.Collection = GetDefaultCollection()

func createCollector() *colly.Collector {
	rp, err := proxy.RoundRobinProxySwitcher("socks5://127.0.0.1:1337", "socks5://127.0.0.1:1338")
	if err != nil {
		log.Fatal(err)
	}

	redis := os.Getenv("REDIS_HOST")
	redispass := os.Getenv("REDIS_PASS")
	sc := colly.NewCollector(
		colly.Debugger(&debug.LogDebugger{}),
		colly.AllowedDomains(allowed1, allowed2),
		colly.MaxDepth(2),
		colly.Async(true),
	)
	sc.SetProxyFunc(rp)
	sc.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 10, RandomDelay: 20 * time.Second})
	sc.WithTransport(&http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		Proxy:           http.ProxyFromEnvironment,
		DialContext: (&net.Dialer{
			Timeout:   120 * time.Second,
			KeepAlive: 120 * time.Second,
			DualStack: true,
		}).DialContext,
		MaxIdleConns:          100,
		IdleConnTimeout:       120 * time.Second,
		TLSHandshakeTimeout:   30 * time.Second,
		ExpectContinueTimeout: 10 * time.Second,
		DisableKeepAlives:     true,
	})
	min5, _ := time.ParseDuration("10m")
	sc.SetRequestTimeout(min5)

	// Extensions
	extensions.RandomUserAgent(sc)
	extensions.Referer(sc)

	// TODO: Use redis storage
	// Db
	if redis != "" {
		storage := &redisstorage.Storage{
			Address:  redis,
			Password: redispass,
			DB:       0,
			Prefix:   "job01",
		}
		err := sc.SetStorage(storage)
		if err != nil {
			panic(err)
		}
	}
	return sc
}

// Publishing jobs
type job struct {
	Link        string
	Name        string
	Salary      string
	Company     string
	JobColor    string
	DateCreated string
	Category    string
}

func DateToday() string {
	t := time.Now().UTC()
	td := fmt.Sprintf("%d-%d-%d", t.Month(), t.Day(), t.Year())
	return td
}

func DateYesterday() string {
	t := time.Now().UTC()
	y := t.Add(time.Hour * -24)
	td := fmt.Sprintf("%d-%d-%d", y.Month(), y.Day(), y.Year())
	return td
}

func collector1(cl *colly.Collector, baseUrl string) {
	detailCollector := cl.Clone()
	cl.Visit(baseUrl)
	cl.OnXML("//div[@class=\"jobcategories-wrapper\"]", func(x *colly.XMLElement) {
		nodes, _ := htmlquery.QueryAll(x.DOM.(*html.Node), "//div[contains(@class, \"active\")]/following-sibling::div[@class=\"title \"]")
		for _, node := range nodes {
			link := htmlquery.InnerText(htmlquery.FindOne(node, "//a/@href"))
			log.Println(x.Request.AbsoluteURL(link))
			detailCollector.Visit(x.Request.AbsoluteURL(link))
		}
	})
	detailCollector.OnXML("//a[@class=\"item\" and @type=\"nextItem\"]", func(x *colly.XMLElement) {
		newUrl := x.Request.AbsoluteURL(x.Attr("href"))
		if newUrl != "" {
			cl.Visit(newUrl)
		}
	})
	detailCollector.OnXML("//*[@id=\"job-browse-card\"]", func(x *colly.XMLElement) {
		nodes, _ := htmlquery.QueryAll(x.DOM.(*html.Node), "//div[contains(@class,\"job-browse-card-element\")]")
		jobs := []interface{}{}
		category := x.Request.Ctx.Get("category")
		for _, node := range nodes {
			defer panickRecover()
			link := htmlquery.InnerText(htmlquery.FindOne(node, "//a[@class=\"jobTitleLink-v2\"]/@href"))
			j := &job{
				x.Request.AbsoluteURL(link),
				htmlquery.InnerText(htmlquery.FindOne(node, "//a[@class=\"jobTitleLink-v2\"]")),
				htmlquery.InnerText(htmlquery.FindOne(node, "//a[@class=\"jobTitleLink-v2\"]/following-sibling::div")),
				htmlquery.InnerText(htmlquery.FindOne(node, "//span[@class=\"company-browse-info\"]")),
				"orange",
				DateToday(),
				category,
			}
			util.LogWhenDev("LINK", link)
			jobBson, _ := bson.Marshal(j)
			jobs = append(jobs, jobBson)
		}
		InsertIntoCollection(jobs, collection)
	})
	detailCollector.OnRequest(func(r *colly.Request) {
		c := strings.Split(r.URL.String(), "/")
		categoryIndex := len(c) - 1
		r.Ctx.Put("category", c[categoryIndex])
	})

	cl.OnError(func(r *colly.Response, err error) {
		if err != nil {
			util.LogWhenDev("ERROR", fmt.Sprintf("%s", err))
		}
	})
	cl.OnRequest(func(r *colly.Request) {
		util.LogWhenDev("VISITING", r.URL.String())
	})
	cl.OnScraped(func(r *colly.Response) {
		util.LogWhenDev("Scraping Done", "")
	})
	// cl.Wait()
}

type queueCollector struct {
	qc *colly.Collector
	q  *queue.Queue
}

func DeletePreviousData() {
	log.Println("::::Starting job delete previous data::::", time.Now())
	filter := struct{ DateCreated string }{DateCreated: DateYesterday()}
	DeleteMany(filter, collection)
}

func scrapeAll() {
	maxSize := 10000
	collector := createCollector()
	q1, _ := queue.New(
		8,
		&queue.InMemoryQueueStorage{MaxSize: maxSize})
	q2, _ := queue.New(
		8,
		&queue.InMemoryQueueStorage{MaxSize: maxSize})
	queues := []queueCollector{
		{
			qc: collector,
			q:  q1,
		}, {
			qc: collector.Clone(),
			q:  q2,
		},
	}

	// TODO: Change prod setup
	collector1(queues[0].qc, "")
	collector1(queues[1].qc, "")
}

func Scrape() {
	scrapeAll()
}
