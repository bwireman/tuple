package main

import (
	"encoding/json"
	"log"
	"net/http"

	pilot "github.com/bwireman/tuple/pilot/pkg"
)

var p = pilot.NewPilot()
var versions = map[string]map[string]string{}

func handlerWrapper(path string, APIVersion string, handler func(http.ResponseWriter, *http.Request)) (string, func(http.ResponseWriter, *http.Request)) {
	fullPath := "/" + APIVersion + path
	log.Println("Registered: ", fullPath)
	return fullPath, func(rw http.ResponseWriter, rq *http.Request) {
		log.Println(rq.Method, " on ", rq.RequestURI)
		handler(rw, rq)
	}
}

func main() {
	port := ":5001"
	apiVersion := "v0-1"
	versions["versions"] = map[string]string{"v0-1": "/v0-1"}

	http.HandleFunc("/", summary)
	http.HandleFunc(handlerWrapper("/", apiVersion, root))
	http.HandleFunc(handlerWrapper("/register", apiVersion, registerNode))
	http.HandleFunc(handlerWrapper("/launch", apiVersion, launchContainer))

	log.Print("Listening on ", port)
	err := http.ListenAndServe(port, nil)
	log.Fatal(err.Error())
}

func summary(rw http.ResponseWriter, rq *http.Request) {
	b, _ := json.Marshal(versions)
	rw.Write(b)
}

func root(rw http.ResponseWriter, rq *http.Request) {
	b, err := p.Serialize()

	resp := b
	if err != nil {
		resp = []byte(err.Error())
	}

	rw.Write(resp)
}

func registerNode(rw http.ResponseWriter, rq *http.Request) {
	if rq.Method == "POST" {
		defer rq.Body.Close()

		var nr pilot.NodeRegistry

		if err := json.NewDecoder(rq.Body).Decode(&nr); err != nil {
			log.Println(err.Error())
			rw.Write([]byte(err.Error()))
			return
		}

		p.RegisterNode(&nr)
	}

	rw.Write([]byte("200 OK"))
}

func launchContainer(rw http.ResponseWriter, rq *http.Request) {
	if rq.Method == "POST" {
		defer rq.Body.Close()

		var c pilot.Container

		if err := json.NewDecoder(rq.Body).Decode(&c); err != nil {
			log.Println(err.Error())
			rw.Write([]byte(err.Error()))
			return
		}

		err := p.LaunchContainer(&c)

		if err != nil {
			log.Println(err.Error())
			rw.Write([]byte("500 Error"))
		}
	}

	rw.Write([]byte("200 OK"))
}
