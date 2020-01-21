package pilot

type Container struct {
	Image string `json:"image"`
	Tag   string `json:"tag"`
	Name  string `json:"name"`
	Count int `json:"count"`
}
