package capstoneLogi

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/twmb/franz-go/pkg/kgo"
)

type LogFormat struct {
	// New unified event format from frontend (see capstoneLogi.ts)
	Type       string `json:"type"`       // checkpoint | insert | delete | run | submission
	SRN        string `json:"srn"`        // globally unique student ID
	QuestionID int    `json:"questionID"` // global question ID
	Ts         int64  `json:"ts"`         // epoch ms
	// Optional fields depending on type
	Content       string `json:"content,omitempty"`
	Offset        int    `json:"offset,omitempty"`
	NumCharacters int    `json:"numCharacters,omitempty"`
	IsPaste       bool   `json:"isPaste,omitempty"`
}

type LogiRequest struct {
	Logs []LogFormat `json:"logs" binding:"required"`
}

var kafkaClient *kgo.Client
var kafkaCtx context.Context

func InitProducer() error {
	brokersEnv := os.Getenv("KAFKA_BROKERS")
	var seeds []string
	if brokersEnv == "" {
		seeds = []string{"kafka-pubsub:9092"}
	} else {
		seeds = strings.Split(brokersEnv, ",")
	}
	var err error
	kafkaClient, err = kgo.NewClient(
		kgo.SeedBrokers(seeds...),
		kgo.AllowAutoTopicCreation(),
		kgo.WithLogger(kgo.BasicLogger(os.Stdout, kgo.LogLevelDebug, nil)),
	)
	if err != nil {
		return err
	}

	kafkaCtx = context.Background()
	go func() {
		record := &kgo.Record{Topic: "capstone-logi", Value: []byte("hello")}
		err := kafkaClient.ProduceSync(kafkaCtx, record).FirstErr()
		if err != nil {
			log.Println("Kafka test produce failed:", err)
		} else {
			log.Println("Kafka test produce succeeded")
		}
	}()
	return nil
}

func HandleLogi(c *gin.Context) {
	var request LogiRequest
	err := c.BindJSON(&request)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "yeverything galat",
		})
		return
	}

	filename := request.Logs[0].SRN // assuming this batch of logs comes from a single user

	f, err := os.OpenFile("./capstone-logi-logs/"+filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "error opening file",
		})
		return
	}
	defer f.Close()

	for _, ev := range request.Logs {
		// CSV columns: srn,questionID,type,ts,offset,numCharacters,isPaste,content
		tsStr := strconv.FormatInt(ev.Ts, 10)
		offsetStr := fmt.Sprint(ev.Offset)
		numCharsStr := fmt.Sprint(ev.NumCharacters)
		isPasteStr := fmt.Sprint(ev.IsPaste)
		contentQuoted := strconv.Quote(ev.Content)

		line := fmt.Sprintf("%s,%d,%s,%s,%s,%s,%s,%s\n",
			ev.SRN,
			ev.QuestionID,
			ev.Type,
			tsStr,
			offsetStr,
			numCharsStr,
			isPasteStr,
			contentQuoted,
		)

		_, err := f.WriteString(line)
		if err != nil {
			log.Println(err)
		}

		// forward to kafka too, apart from just writing to file
		payload, jerr := json.Marshal(ev)
		if jerr != nil {
			log.Println("json marshal error:", jerr)
			continue
		}
		record := &kgo.Record{Topic: "capstone-logi", Value: payload}
		// kafkaClient.Produce(kafkaCtx, record, func(_ *kgo.Record, err error) {
		// 	log.Println("Kafka publishing done")
		// 	if err != nil {
		// 		fmt.Printf("Kafka publishing screwed up")
		// 		fmt.Printf("record had a produce error: %v\n", err)
		// 	}
		// })
		fmt.Println("Going to start kafka publishing")
		if err := kafkaClient.ProduceSync(kafkaCtx, record).FirstErr(); err != nil {
			fmt.Printf("record had a produce error while synchronously producing: %v\n", err)
		}

	}

}
