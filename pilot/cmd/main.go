package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	pilot "github.com/bwireman/tuple/pilot/pkg"
)

var p = pilot.NewPilot()

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
	apiVersion := "v0.1"
	http.HandleFunc(handlerWrapper("/", apiVersion, root))
	http.HandleFunc(handlerWrapper("/register", apiVersion, registerNode))
	fmt.Println("Listening on ", port)
	err := http.ListenAndServe(port, nil)
	log.Fatal(err.Error())
}

func root(rw http.ResponseWriter, rq *http.Request) {
	b, err := p.Serialize()

	resp := b
	if err != nil {
		resp = []byte(err.Error())
	}

	log.Println(string(resp))
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
}
