package pilot

type NodeRegistry struct {
	UUID string `json:"uuid"`
	Path string `json:"node_path"`
	APIVersion string `json:"api_version"`
}