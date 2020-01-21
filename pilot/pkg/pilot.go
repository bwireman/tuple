package pilot

import (
	"bytes"
	"log"
	"encoding/json"
	"errors"
	"net/http"

	uuid "github.com/satori/go.uuid"
)

var (
	ErrorNoNodes = errors.New("No Nodes registered")
)

// Pilot
type Pilot struct {
	UUID  string          `json:"uuid"`
	Nodes []*NodeRegistry `json:"nodes"`
}

func NewPilot() *Pilot {
	return &Pilot{
		UUID:  uuid.Must(uuid.NewV4(), nil).String(),
		Nodes: []*NodeRegistry{},
	}
}

func (p *Pilot) RegisterNode(nr *NodeRegistry) {
	p.Nodes = append(p.Nodes, nr)
}

func (p *Pilot) Serialize() ([]byte, error) {
	return json.Marshal(p)
}

func (p *Pilot) LaunchContainer(c *Container) error {
	if len(p.Nodes) < 1 {
		return ErrorNoNodes
	}

	counts := []int{}
	for i := 0; i < len(p.Nodes); i++ {
		counts = append(counts, 0)
	}

	for i := 0; i < c.Count; i++ {
		counts[i%len(p.Nodes)]++
	}

	for i, n := range p.Nodes {
		c.Count = counts[i]

		b, err := json.Marshal(c)

		if err != nil {
			return err
		}

		containerBuffer := bytes.NewBuffer(b)
		path := n.Path + "/" + n.APIVersion + "/launch"
		log.Println(path)

		_, err = http.Post(path, "application/json", containerBuffer)

		if err != nil {
			return err
		}
	}

	return nil
}
