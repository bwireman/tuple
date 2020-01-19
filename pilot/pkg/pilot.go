package pilot

import (
	"encoding/json"

	uuid "github.com/satori/go.uuid"
)

// Pilot
type Pilot struct {
	UUID  string       `json:"uuid"`
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
